"""
GHOST — Network Recon Agent
Maps the entire attack surface. First deployed on every mission.
Uses whatever tools are available — degrades gracefully if tools are missing.
"""

import subprocess
import socket
import json
import re
from datetime import datetime


class GhostAgent:
    def __init__(self, bus=None):
        self.bus = bus
        self.name = "GHOST"

    def run(self, target: str, scope) -> dict:
        """
        Full recon sweep on a target.
        Returns structured findings dict.
        """
        findings = []
        raw_output = {}
        start_time = datetime.now()

        print(f"  [GHOST] Starting recon on: {target}")

        # ── 1. DNS Resolution ──
        dns = self._dns_lookup(target)
        raw_output["dns"] = dns
        if dns.get("ips"):
            findings.append({
                "type": "dns",
                "title": f"DNS resolved: {', '.join(dns['ips'])}",
                "severity": "info",
                "tool": "dns/socket",
                "data": dns
            })
            print(f"  [GHOST] DNS: {', '.join(dns['ips'])}")

        # ── 2. WHOIS ──
        whois = self._whois(target)
        raw_output["whois"] = whois
        if whois.get("registrar"):
            findings.append({
                "type": "whois",
                "title": f"Registrar: {whois['registrar']}",
                "severity": "info",
                "tool": "whois",
                "data": whois
            })

        # ── 3. Port Scan (nmap) ──
        ports = self._nmap_scan(target)
        raw_output["ports"] = ports
        for port in ports.get("open_ports", []):
            sev = "high" if port["port"] in (22, 23, 3306, 5432, 6379, 27017) else "info"
            findings.append({
                "type": "open_port",
                "title": f"Port {port['port']}/{port['protocol']} open — {port.get('service', 'unknown')}",
                "severity": sev,
                "tool": "nmap",
                "data": port
            })
        print(f"  [GHOST] Found {len(ports.get('open_ports', []))} open ports")

        # ── 4. Technology Fingerprint ──
        tech = self._tech_detect(target)
        raw_output["technologies"] = tech
        for t in tech.get("technologies", []):
            findings.append({
                "type": "technology",
                "title": f"Technology detected: {t}",
                "severity": "info",
                "tool": "whatweb/curl",
                "data": {"technology": t}
            })

        # ── 5. HTTP Headers Analysis ──
        headers = self._check_headers(target)
        raw_output["headers"] = headers
        for issue in headers.get("issues", []):
            findings.append({
                "type": "missing_header",
                "title": issue["title"],
                "severity": issue["severity"],
                "tool": "curl",
                "data": issue
            })

        # ── 6. Subdomain enumeration (basic) ──
        subs = self._enumerate_subdomains(target)
        raw_output["subdomains"] = subs
        if subs.get("found"):
            findings.append({
                "type": "subdomains",
                "title": f"Found {len(subs['found'])} subdomains",
                "severity": "info",
                "tool": "amass/dig",
                "data": subs
            })
            print(f"  [GHOST] Subdomains: {len(subs['found'])} found")

        duration = (datetime.now() - start_time).seconds

        # Emit to bus
        if self.bus:
            self.bus.emit("recon_complete", {
                "target": target,
                "findings": findings,
                "raw": raw_output
            })

            # Trigger scanner if high-severity ports found
            high_sev = [f for f in findings if f.get("severity") in ("high", "critical")]
            if high_sev:
                self.bus.emit("high_severity_recon", {
                    "target": target,
                    "count": len(high_sev),
                    "findings": high_sev
                })

        summary_parts = []
        if dns.get("ips"):
            summary_parts.append(f"{len(dns['ips'])} IP(s) resolved")
        if ports.get("open_ports"):
            summary_parts.append(f"{len(ports['open_ports'])} ports open")
        if subs.get("found"):
            summary_parts.append(f"{len(subs['found'])} subdomains")
        if headers.get("issues"):
            summary_parts.append(f"{len(headers['issues'])} header issues")

        summary = " | ".join(summary_parts) if summary_parts else "Recon complete"

        return {
            "agent": "GHOST",
            "target": target,
            "timestamp": start_time.isoformat(),
            "duration_seconds": duration,
            "findings": findings,
            "raw": raw_output,
            "summary": summary,
            "finding_count": len(findings)
        }

    def _dns_lookup(self, target: str) -> dict:
        """DNS resolution using Python socket (no tools needed)."""
        result = {"target": target, "ips": [], "hostnames": []}
        try:
            # Clean the target
            domain = target.replace("https://", "").replace("http://", "").split("/")[0]
            info = socket.getaddrinfo(domain, None)
            ips = list(set([r[4][0] for r in info]))
            result["ips"] = ips
            result["domain"] = domain

            # Reverse DNS
            for ip in ips[:2]:
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                    result["hostnames"].append(hostname)
                except Exception:
                    pass
        except Exception as e:
            result["error"] = str(e)
        return result

    def _whois(self, target: str) -> dict:
        """WHOIS lookup using system whois command."""
        result = {"raw": "", "registrar": "", "creation_date": "", "expiry_date": ""}
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]

        try:
            proc = subprocess.run(
                ["whois", domain],
                capture_output=True, text=True, timeout=15
            )
            raw = proc.stdout

            # Parse key fields
            for line in raw.splitlines():
                ll = line.lower()
                if "registrar:" in ll and not result["registrar"]:
                    result["registrar"] = line.split(":", 1)[-1].strip()
                elif "creation date" in ll or "created:" in ll:
                    result["creation_date"] = line.split(":", 1)[-1].strip()
                elif "expir" in ll and ("date" in ll or "on" in ll):
                    result["expiry_date"] = line.split(":", 1)[-1].strip()

            result["raw"] = raw[:2000]  # truncate
        except FileNotFoundError:
            result["error"] = "whois not installed"
        except subprocess.TimeoutExpired:
            result["error"] = "whois timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def _nmap_scan(self, target: str) -> dict:
        """Port scan using nmap. Falls back to basic socket scan."""
        result = {"open_ports": [], "method": "nmap"}
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]

        try:
            proc = subprocess.run(
                ["nmap", "-sV", "--open", "-T4",
                 "-p", "21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443,27017",
                 "--script", "banner",
                 domain],
                capture_output=True, text=True, timeout=120
            )
            output = proc.stdout

            # Parse nmap output
            for line in output.splitlines():
                # Match: 80/tcp   open  http    Apache httpd 2.4.41
                m = re.match(
                    r'(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)',
                    line.strip()
                )
                if m:
                    result["open_ports"].append({
                        "port": int(m.group(1)),
                        "protocol": m.group(2),
                        "service": m.group(3),
                        "version": m.group(4).strip()
                    })

        except FileNotFoundError:
            result["method"] = "socket_fallback"
            result["note"] = "nmap not found — using basic socket scan"
            result["open_ports"] = self._socket_scan(domain)
        except subprocess.TimeoutExpired:
            result["error"] = "nmap timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def _socket_scan(self, host: str) -> list:
        """Basic port scan using Python sockets (no tools needed)."""
        common_ports = [
            (21, "ftp"), (22, "ssh"), (23, "telnet"),
            (25, "smtp"), (53, "dns"), (80, "http"),
            (110, "pop3"), (143, "imap"), (443, "https"),
            (3306, "mysql"), (3389, "rdp"), (5432, "postgresql"),
            (6379, "redis"), (8080, "http-alt"), (8443, "https-alt"),
            (27017, "mongodb")
        ]
        open_ports = []
        for port, service in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append({
                        "port": port,
                        "protocol": "tcp",
                        "service": service,
                        "version": ""
                    })
                sock.close()
            except Exception:
                pass
        return open_ports

    def _tech_detect(self, target: str) -> dict:
        """Detect web technologies via whatweb or curl headers."""
        result = {"technologies": [], "server": "", "cms": ""}
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]
        url = f"https://{domain}" if not target.startswith("http") else target

        # Try whatweb first
        try:
            proc = subprocess.run(
                ["whatweb", "--no-errors", "--color=never", "-a", "1", url],
                capture_output=True, text=True, timeout=20
            )
            output = proc.stdout
            # Strip ANSI escape codes (e.g. \x1b[0m → "0m" artifacts)
            output = re.sub(r'\x1b\[[0-9;]*m', '', output)
            if output:
                # Extract technologies from whatweb output
                techs = re.findall(r'\[([^\[\]]+?)\]', output)
                cleaned = []
                for t in techs:
                    t = t.split("[")[0].strip()
                    # Skip ANSI artifacts, version numbers alone, empty strings
                    if t and len(t) < 50 and not re.match(r'^[\d;m]+$', t):
                        cleaned.append(t)
                result["technologies"] = cleaned[:10]
                if result["technologies"]:
                    return result
        except FileNotFoundError:
            pass
        except Exception:
            pass

        # Fallback: curl headers
        try:
            proc = subprocess.run(
                ["curl", "-sI", "--max-time", "10", url],
                capture_output=True, text=True, timeout=15
            )
            headers_raw = proc.stdout.lower()

            if "apache" in headers_raw:
                result["technologies"].append("Apache")
            if "nginx" in headers_raw:
                result["technologies"].append("Nginx")
            if "cloudflare" in headers_raw:
                result["technologies"].append("Cloudflare")
            if "wordpress" in headers_raw:
                result["technologies"].append("WordPress")
            if "php" in headers_raw:
                result["technologies"].append("PHP")
            if "asp.net" in headers_raw:
                result["technologies"].append("ASP.NET")
            if "express" in headers_raw:
                result["technologies"].append("Express.js")

            # Extract Server header
            for line in proc.stdout.splitlines():
                if line.lower().startswith("server:"):
                    result["server"] = line.split(":", 1)[-1].strip()
                    break
        except Exception as e:
            result["error"] = str(e)

        return result

    def _check_headers(self, target: str) -> dict:
        """Check for missing security headers."""
        result = {"issues": [], "headers_found": []}
        url = f"https://{target}" if not target.startswith("http") else target

        security_headers = {
            "strict-transport-security": {
                "title": "Missing HSTS header — site vulnerable to downgrade attacks",
                "severity": "high",
                "recommendation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains"
            },
            "content-security-policy": {
                "title": "Missing Content-Security-Policy — XSS risk elevated",
                "severity": "medium",
                "recommendation": "Implement CSP header to prevent XSS attacks"
            },
            "x-frame-options": {
                "title": "Missing X-Frame-Options — clickjacking possible",
                "severity": "medium",
                "recommendation": "Add: X-Frame-Options: DENY"
            },
            "x-content-type-options": {
                "title": "Missing X-Content-Type-Options — MIME sniffing risk",
                "severity": "low",
                "recommendation": "Add: X-Content-Type-Options: nosniff"
            },
            "permissions-policy": {
                "title": "Missing Permissions-Policy header",
                "severity": "low",
                "recommendation": "Add Permissions-Policy to restrict browser features"
            },
        }

        try:
            proc = subprocess.run(
                ["curl", "-sI", "--max-time", "10", "-L", url],
                capture_output=True, text=True, timeout=15
            )
            headers_raw = proc.stdout.lower()

            for header, info in security_headers.items():
                if header in headers_raw:
                    result["headers_found"].append(header)
                else:
                    result["issues"].append({
                        "title": info["title"],
                        "severity": info["severity"],
                        "recommendation": info["recommendation"],
                        "missing_header": header
                    })
        except Exception as e:
            result["error"] = str(e)

        return result

    def _enumerate_subdomains(self, target: str) -> dict:
        """Enumerate subdomains using amass or basic DNS bruteforce."""
        result = {"found": [], "method": ""}
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]

        # Strip subdomains to get base domain
        parts = domain.split(".")
        if len(parts) > 2:
            base_domain = ".".join(parts[-2:])
        else:
            base_domain = domain

        # Try amass
        try:
            proc = subprocess.run(
                ["amass", "enum", "-passive", "-d", base_domain, "-timeout", "1"],
                capture_output=True, text=True, timeout=90
            )
            if proc.stdout.strip():
                result["found"] = [
                    s.strip() for s in proc.stdout.splitlines()
                    if s.strip() and base_domain in s
                ][:20]
                result["method"] = "amass"
                return result
        except FileNotFoundError:
            pass
        except Exception:
            pass

        # Fallback: common subdomain wordlist via DNS
        result["method"] = "dns_bruteforce"
        common_subs = [
            "www", "mail", "api", "dev", "staging", "test",
            "admin", "vpn", "ftp", "smtp", "pop", "imap",
            "static", "cdn", "assets", "app", "portal",
            "dashboard", "docs", "blog", "shop", "store"
        ]
        for sub in common_subs:
            try:
                hostname = f"{sub}.{base_domain}"
                socket.getaddrinfo(hostname, None)
                result["found"].append(hostname)
            except Exception:
                pass

        return result
