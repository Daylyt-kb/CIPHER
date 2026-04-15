# CIPHER — The World's First Civilian AI Security Swarm

> *9 specialized AI agents. Zero budget. Runs on your laptop. Legal by design.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94?logo=kali-linux)](https://www.kali.org/)
[![Tests](https://img.shields.io/badge/tests-26%2F26%20passing-brightgreen)](tests/)
[![Ollama](https://img.shields.io/badge/Ollama-local%20models-black)](https://ollama.com)

CIPHER is an AI security swarm that runs in your terminal and browser. Tell it what you want to test in plain English — it deploys 9 specialist agents, pulls the right Kali tools, writes custom scripts when no tool exists, and returns a plain English report.

**No cloud required. No server bills. No expertise needed. Works fully offline with Ollama.**

---

## AI Providers — Cloud & Local

CIPHER works with **any** of these. Switch from the browser Settings tab — no restart, no code changes.

### 🖥️ Local (Free · Private · No API key needed)

| Provider | Setup | Models | Privacy |
|----------|-------|--------|---------|
| **Ollama** | `curl -fsSL https://ollama.com/install.sh \| sh` | llama3.2, mistral, codellama, deepseek-r1, phi3, qwen2.5 | 100% local |
| **LM Studio** | Download at lmstudio.ai → Load model → Start server | Any GGUF model | 100% local |

```bash
# Quickstart with Ollama (recommended for privacy)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
ollama serve
# Then run CIPHER — it auto-detects Ollama
python3 cipher.py --interactive
```

### ☁️ Cloud (API key required)

| Provider | Free Tier | Key Prefix | Get Key |
|----------|-----------|------------|---------|
| **Groq** | ✅ Free | `gsk_` | [console.groq.com](https://console.groq.com) |
| **Google Gemini** | ✅ Free | `AIzaSy` | [aistudio.google.com](https://aistudio.google.com) |
| **Anthropic Claude** | No | `sk-ant-` | [console.anthropic.com](https://console.anthropic.com) |
| **OpenAI** | No | `sk-` | [platform.openai.com](https://platform.openai.com) |
| **Mistral** | No | `MIST` | [console.mistral.ai](https://console.mistral.ai) |

```bash
# Free cloud option — Groq (fastest, no credit card)
export GROQ_API_KEY="gsk_your_key_here"
python3 cipher.py --interactive

# Or set in the web UI Settings tab — no restart needed
python3 web_ui.py
# → open localhost:7734 → Settings → paste any key
```

> **No key at all?** CIPHER still runs. Recon, OSINT, and scanning work without AI — the AI brain enhances report analysis and FORGE script generation.

---

## The Swarm — 9 Agents

| Agent | Name | Role |
|-------|------|------|
| 🔍 | **GHOST** | Network recon — DNS, ports, tech stack, subdomains, security headers |
| 🌐 | **SPECTER** | OSINT — cert transparency, robots.txt, emails, Google dorks |
| 🛡️ | **SCANNER** | Vulnerability detection — nikto, nuclei, SSL, exposed files |
| 💥 | **BREACH** | Controlled exploitation — 14 canary payloads, SHA-256 audit trail |
| ⚡ | **FORGE** | Script generation — writes Python when no tool covers a gap |
| 🤖 | **MIRROR** | AI-vs-AI red team — OWASP LLM Top 10 against AI endpoints |
| 🧠 | **NEURON** | Self-upgrade — hourly CVE feeds, MITRE ATT&CK, local SQLite |
| 📋 | **LEDGER** | Reports — CVSS scores, plain English, developer remediation |
| 🎯 | **COMMANDER** | Brain — understands plain English, orchestrates everything |

---

## What makes CIPHER different

| | Traditional Pentest | Existing AI Tools | CIPHER |
|---|---|---|---|
| Cost | $10K–$100K | $500+/month | **Free** |
| Local models | No | No | **Yes (Ollama)** |
| Runs fully offline | No | No | **Yes** |
| Setup | Days | Hours | **1 command** |
| Requires expertise | Yes | Yes | **No** |
| Script generation | No | No | **Yes (FORGE)** |
| AI-vs-AI testing | No | No | **Yes (MIRROR)** |
| Plain English | No | Partial | **Yes** |

---

## Install

```bash
git clone https://github.com/Daylyt-kb/CIPHER.git
cd CIPHER
chmod +x install.sh && ./install.sh
```

CIPHER works with whatever Kali tools you have. Missing tools are skipped gracefully — it falls back to pure Python implementations.

---

## Usage

### Browser UI (recommended)
```bash
python3 web_ui.py
# Open http://localhost:7734
```

Set your AI provider in the Settings tab. Enter a target. Deploy the swarm.

### Interactive shell
```bash
python3 cipher.py --interactive
```

```
cipher> scan mywebsite.com
cipher> osint check company.com
cipher> forge a script to enumerate all subdomains
cipher> full test 192.168.1.0/24
```

### Direct scan
```bash
# Surface recon
python3 cipher.py -t mysite.com -m recon --authorized

# Full swarm
python3 cipher.py -t mysite.com -m full --authorized

# AI-vs-AI audit (for AI-powered apps)
python3 cipher.py -t myapp.com -m ai-audit --authorized

# Check installed tools
python3 cipher.py --check-tools
```

### Telegram bot (zero hosting cost)
```bash
# Get token from @BotFather on Telegram
export TELEGRAM_BOT_TOKEN="your-token"
python3 telegram_bot.py
# Users can now scan via /scan, /osint, /full commands
```

---

## What CIPHER checks

**GHOST (Recon)**
- DNS resolution, reverse DNS, WHOIS
- Port scan (nmap or socket fallback)
- Technology fingerprint (Apache, Nginx, WordPress, PHP, Cloudflare...)
- Security headers (HSTS, CSP, X-Frame-Options, Permissions-Policy)
- Subdomain enumeration (amass or DNS bruteforce)

**SPECTER (OSINT)**
- Certificate transparency via crt.sh
- Email harvesting via theHarvester
- robots.txt disallowed paths
- Google dork generation
- GitHub exposure hints

**SCANNER (Vulnerabilities)**
- Nikto web server scan
- SSL/TLS audit
- Nuclei template scan (high/critical)
- Exposed files: `.env`, `.git`, `phpinfo.php`, `/actuator`, `/swagger-ui`

**BREACH (Exploitation)**
- 14 non-destructive canary payloads
- SQL injection, XSS, SSRF, open redirect, command injection, path traversal, XXE
- Immutable SHA-256 signed audit trail
- Subdomain takeover detection

**FORGE (Script Generation)**
- Generates Python/Bash scripts for gaps no tool covers
- AST-validated before execution
- Saved to `./cipher_output/scripts/`

**MIRROR (AI Red Team)**
- Tests AI-powered apps for OWASP LLM Top 10
- Prompt injection, tool-call exfiltration, memory poisoning, jailbreaks
- Works against any HTTP endpoint

**NEURON (Intelligence)**
- Hourly CVE ingest from NVD API (free, no key)
- MITRE ATT&CK techniques from GitHub
- ExploitDB RSS feed
- Local SQLite — data never leaves your machine

---

## Legal

CIPHER is **legal-by-design**. Authorization is enforced at the architecture level.

- Scope is SHA-256 signed — out-of-scope targets throw `PermissionError`, not a warning
- Consent records saved with timestamps for every session
- BREACH agent uses non-destructive canary payloads only
- High-risk actions require explicit Commander approval

**Only test systems you own or have written permission to test.**

---

## Output

Reports saved to `./cipher_output/`:
- `mission_[id]_report.md` — human-readable with CVSS scores
- `mission_[id]_report.json` — structured data for integrations
- `audit/` — SHA-256 signed audit trail for each BREACH action

---

## What's built

- [x] GHOST, SPECTER, SCANNER, BREACH, FORGE, MIRROR, NEURON, LEDGER, COMMANDER
- [x] Web UI — browser interface at localhost:7734 (`web_ui.py`)
- [x] Telegram bot — zero-cost mobile interface (`telegram_bot.py`)
- [x] Ollama support — fully local, fully private, zero cost
- [x] Multi-provider AI — Anthropic, Gemini, OpenAI, Groq, Mistral, Ollama, LM Studio
- [x] NEURON — live CVE/ATT&CK/ExploitDB feeds → local SQLite
- [x] 26/26 tests passing

## Coming next

- [ ] Docker sandbox for FORGE (replaces AST-only validation)
- [ ] WebSocket real-time terminal (replaces HTTP polling)
- [ ] MSSP white-label API
- [ ] Multi-target batch scanning
- [ ] Playbook marketplace

---

## Contributing

Built by one person with zero budget. All contributions welcome.

```
Fork → Build → PR
```

Found a bug? Open an issue.  
Built something cool with CIPHER? PR it.  
Star the repo if this helped you.

---

## Author

**Kebron Isaias** — Builder · Security Enthusiast · Zero Budget Founder

Building enterprise-grade security tools that work for everyone, not just companies with $50K budgets.

[LinkedIn](https://www.linkedin.com/in/kebron-isaias-0716aa2b7) · [GitHub](https://github.com/Daylyt-kb) · [Live Demo](https://cipher-ss.netlify.app)

---

*CIPHER — The security swarm the world needed but nobody built.*
