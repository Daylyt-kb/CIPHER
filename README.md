# CIPHER — The World's First Civilian AI Security Swarm

> *9 specialized AI agents. Zero budget. Runs on your laptop. Legal by design.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94?logo=kali-linux)](https://www.kali.org/)

CIPHER is an AI security swarm that runs in your terminal. Tell it what you want to test in plain English — it deploys specialist agents, pulls the right Kali tools, writes custom scripts when needed, and returns a clean report.

**No cloud required. No server bills. No expertise needed.**

---

## What makes CIPHER different

Every existing AI security tool requires enterprise procurement, a dedicated security team, or a $50K contract. CIPHER runs on your laptop for free.

| | Traditional Pentest | Existing AI Tools | CIPHER |
|---|---|---|---|
| Cost | $10K–$100K | $500+/month | Free |
| Setup | Days | Hours | 1 command |
| Requires expertise | Yes | Yes | No |
| Plain English interface | No | Partial | Yes |
| Runs offline | No | No | Yes |
| Script generation | No | No | Yes (FORGE) |
| AI-vs-AI testing | No | No | Yes (MIRROR) |

---

## The Swarm

CIPHER deploys 9 specialized agents in parallel:

| Agent | Name | Role |
|-------|------|------|
| 🔍 | **GHOST** | Network recon — maps every open door |
| 🌐 | **SPECTER** | OSINT — hunts what the internet already knows |
| 🛡️ | **SCANNER** | Vulnerability detection — finds the weaknesses |
| 💥 | **BREACH** | Controlled exploitation — proves it's real |
| ⚡ | **FORGE** | Script generation — writes code when no tool exists |
| 🤖 | **MIRROR** | AI-vs-AI — tests your AI agents for attacks |
| 🧠 | **NEURON** | Self-upgrade — learns new CVEs and techniques 24/7 |
| 📋 | **LEDGER** | Reports — translates findings to plain English |
| 🎯 | **COMMANDER** | Brain — understands you and orchestrates everything |

---

## Install

```bash
git clone https://github.com/Daylyt-kb/cipher.git
cd cipher
chmod +x install.sh && ./install.sh
```

That's it. CIPHER works with whatever Kali tools you have installed. Missing tools are skipped gracefully.

---

## Usage

### Interactive shell (recommended)
```bash
python3 cipher.py --interactive
```

Then just talk:
```
cipher> scan mywebsite.com
cipher> osint check company.com  
cipher> forge a script to enumerate all admin panels
cipher> full test 192.168.1.0/24
```

### Direct scan
```bash
# Recon only (port scan + technology fingerprint)
python3 cipher.py -t mysite.com -m recon --authorized

# OSINT sweep
python3 cipher.py -t mydomain.com -m osint --authorized

# Full swarm (recon + OSINT + vuln scan)
python3 cipher.py -t mysite.com -m full --authorized

# Check what tools you have
python3 cipher.py --check-tools
```

### With AI (optional — richer analysis)
```bash
export ANTHROPIC_API_KEY='your-key-here'
python3 cipher.py --interactive
```

Get a free Anthropic API key at [console.anthropic.com](https://console.anthropic.com) — the free tier is enough for many scans.

---

## What CIPHER checks

**GHOST (Recon)**
- DNS resolution & reverse DNS
- WHOIS / registrar info
- Port scan (nmap or socket fallback)
- Technology fingerprint (Apache, Nginx, WordPress, PHP, etc.)
- Security headers (HSTS, CSP, X-Frame-Options)
- Subdomain enumeration

**SPECTER (OSINT)**
- Email harvesting via theHarvester
- Certificate transparency (crt.sh)
- robots.txt hidden paths
- Google dork generation
- GitHub exposure hints

**SCANNER (Vulnerabilities)**
- Nikto web server scan
- SSL/TLS issues
- Nuclei template scan
- Exposed sensitive files (.env, .git, phpinfo, swagger)
- Spring Boot actuator exposure

**FORGE (Script Generation)**
- Writes custom Python scripts when no tool covers a gap
- AST-validated before execution
- Saved to `./cipher_output/scripts/`

---

## Legal

CIPHER is **legal-by-design**. Every scan requires explicit authorization.

- The `--authorized` flag is a legal confirmation
- Consent records are saved with timestamps
- Scope validation blocks out-of-scope targets
- No action runs against unauthorized targets — this is architecture, not a checkbox

**Only test systems you own or have written permission to test.**  
Unauthorized scanning is illegal under the CFAA (USA), Computer Misuse Act (UK), and equivalent laws worldwide.

---

## Output

Reports are saved to `./cipher_output/`:
- `mission_[id]_report.json` — full structured data
- `mission_[id]_report.md` — human-readable Markdown report

---

## What's built

- [x] GHOST — network recon agent
- [x] SPECTER — OSINT agent  
- [x] SCANNER — vulnerability detection agent
- [x] BREACH — controlled exploitation (14 canary payloads, audit trail)
- [x] FORGE — live script generation agent
- [x] MIRROR — AI-vs-AI red team (OWASP LLM Top 10)
- [x] NEURON — self-upgrade loop (SQLite, NVD CVE feed, MITRE ATT&CK, ExploitDB)
- [x] LEDGER — plain English report generator
- [x] COMMANDER — universal AI orchestration (Anthropic/Gemini/Groq/OpenAI/Mistral)
- [x] Web UI — browser interface at localhost:7734
- [x] Telegram bot — zero-cost mobile interface (telegram_bot.py)
- [x] Multi-provider AI — switch providers from Settings tab, no restart
- [x] 26/26 tests passing

## Coming next

- [ ] Docker sandbox for FORGE scripts (replaces AST-only validation)
- [ ] WebSocket terminal (replaces HTTP polling in web UI)
- [ ] MSSP white-label API
- [ ] Playbook marketplace

---

## 🤝 Support the Mission

CIPHER was built by one person with zero budget. If you find value in this project, here is how you can help us reach our goal of **100 stars**:

1. **Star the Repo**: It helps others find the tool.
2. **Open an Issue**: Found a bug? Have a feature request? Let us know.
3. **Contribute**: Check the `Coming next` list and submit a PR.

```bash
Fork → Build → PR
```

---

## 🏗️ Author

Built with conviction by **Kebron Isaias** — [LinkedIn](https://www.linkedin.com/in/kebron-isaias-0716aa2b7) · [GitHub](https://github.com/Daylyt-kb)

---

*CIPHER — The security swarm the world needed but nobody built.*

*CIPHER — The security swarm the world needed but nobody built.*

