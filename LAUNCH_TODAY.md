# CIPHER — Launch Day Playbook
# Kebron Isaias | linkedin.com/in/kebron-isaias-0716aa2b7
# Date: Today. Do all 3 steps.

---

## STEP 1 — PUSH TO GITHUB (do this first, ~10 minutes)

### A. Create the repo on GitHub
1. Go to https://github.com/new
2. Repository name: **cipher**
3. Description: **9 AI agents that orchestrate Kali Linux from your browser. Plain English. Zero cost. Legal by design.**
4. Set to **Public**
5. Do NOT check "Add README" or "Add .gitignore" — we have ours
6. Click **Create repository**
7. Copy your repo URL (will look like: https://github.com/kebronisaias/cipher.git)

### B. Run these commands in your terminal (inside the cipher folder)

```bash
# Go into the cipher folder
cd cipher

# Initialize git
git init

# Set your identity
git config user.name "Kebron Isaias"
git config user.email "your-email@gmail.com"

# Stage everything
git add .

# Check what's being committed (optional sanity check)
git status

# First commit — this is your founding commit, make it count
git commit -m "feat: CIPHER v1.0 — world's first civilian AI security swarm

9 specialized agents: GHOST (recon), SPECTER (OSINT), SCANNER (vulns),
BREACH (exploitation), FORGE (script gen), MIRROR (AI-vs-AI), NEURON
(self-upgrade), LEDGER (reports), COMMANDER (orchestration).

Multi-provider AI: Anthropic, Gemini, OpenAI, Groq, Mistral.
Switch providers from browser dashboard — no restart needed.
Legal by design: cryptographic scope enforcement.
17/17 tests passing.

Built with zero budget. Brutal by capability."

# Add your GitHub remote — REPLACE with your actual URL
git remote add origin https://github.com/Daylyt-kb/cipher.git

# Push
git branch -M main
git push -u origin main
```

### C. After push — add topics to your repo
Go to your repo on GitHub → click the ⚙ gear next to "About" → add these topics:
```
cybersecurity  ai-agents  penetration-testing  python  kali-linux
osint  ethical-hacking  red-team  ai-security  open-source
```

---

## STEP 2 — DEPLOY LANDING PAGE TO NETLIFY (~5 minutes)

### Option A: Drag and drop (fastest)
1. Go to https://app.netlify.com
2. Click "Add new site" → "Deploy manually"
3. Drag the **landing/** folder (just that folder) into the box
4. Your site deploys instantly
5. Click "Domain settings" → "Add a custom domain" if you have one
   OR use the free netlify.app subdomain they give you

### Option B: Connect GitHub (recommended — auto-deploys on push)
1. Go to https://app.netlify.com → "Add new site" → "Import from Git"
2. Connect GitHub → pick the cipher repo
3. Build settings:
   - Base directory: `landing`
   - Publish directory: `landing`
   - Build command: (leave empty)
4. Click Deploy

### After deploy:
- Your landing page URL is your public face
- Update the LinkedIn link in index.html: www.linkedin.com/in/kebron-isaias-0716aa2b7
- Replace "Daylyt-kb" in index.html with your GitHub username
- Enable Netlify Forms (Settings → Forms) for the waitlist to work

---

## STEP 3 — POST ON HACKER NEWS

Post at: https://news.ycombinator.com/submit
Best time: **Tuesday–Thursday, 9:00–11:00 AM EST**
(If reading this on a different day — post now anyway, don't wait)

Account requirement: Must be at least 2 weeks old. Create one now if needed.

---

### COPY THIS EXACTLY — HACKER NEWS POST

**TITLE** (copy exactly, no changes):
```
Show HN: CIPHER – 9 AI agents that orchestrate Kali Linux tools from your browser
```

**BODY** (copy and paste everything below the line):

---

I built CIPHER – a multi-agent AI security swarm that runs on your laptop, costs nothing to start, and understands plain English.

**The problem I was solving:** Every AI security tool is built for enterprise teams with $50K budgets. 61% of small businesses get breached every year. Zero tools exist for developers, students, or anyone without a dedicated security team.

**The architecture:**

9 specialized agents work in parallel via a pub/sub message bus:

- **GHOST** – maps the attack surface: DNS, port scan (nmap or socket fallback), technology fingerprint, subdomains, security headers
- **SPECTER** – passive OSINT: certificate transparency (crt.sh), robots.txt, email harvesting via theHarvester, Google dork generation
- **SCANNER** – vulnerability detection: nikto, nuclei, SSL/TLS check, exposed file paths (.env, .git, phpinfo, actuator)
- **BREACH** – controlled exploitation: 14 canary payloads across 7 categories (SQLi, XSS, SSRF, open redirect, cmd injection, path traversal, XXE). Non-destructive only. SHA-256 signed audit trail per action.
- **FORGE** – when no tool covers a gap, FORGE generates a Python script via LLM, validates it through AST analysis, sandbox-tests it, then deploys it
- **MIRROR** – AI-vs-AI red teaming: 10 OWASP LLM Top 10 payloads against AI-powered endpoints (prompt injection, tool-call exfiltration, memory poisoning)
- **NEURON** – hourly CVE ingest from NVD API, stored locally
- **LEDGER** – plain English pentest reports with CVSS scores and remediation steps
- **COMMANDER** – understands plain English, builds mission plans, delegates to agents

**Multi-provider AI:** works with Anthropic, Gemini (free), OpenAI, Groq (free), Mistral. You paste the key in a browser Settings tab — CIPHER detects the provider automatically and switches without restarting.

**Legal enforcement is architectural, not a checkbox:** scope is SHA-256 signed before any agent fires. Out-of-scope targets throw a `PermissionError` — you literally can't scan unauthorized systems. Every BREACH action has an immutable timestamped audit log.

**FORGE is the part I haven't seen elsewhere.** Most security tools are capped by their tool registry. FORGE isn't. When it detects a gap, it writes the script, runs it through Python's `ast` module to catch dangerous patterns, sandbox-tests it in a subprocess, then runs it against the authorized target. The system's capability isn't fixed.

**Honest limitations:**
- Without Kali tools installed, many agents fall back to pure Python (socket scans, urllib)
- FORGE's AST validator is good but not bulletproof — a real Docker sandbox is the right move
- MIRROR's 10 payloads are a starting point
- No persistent storage — all state is in-memory per session

17/17 tests passing. MIT licensed.

GitHub: https://github.com/Daylyt-kb/cipher

```bash
git clone https://github.com/Daylyt-kb/cipher
cd cipher && ./install.sh
python3 web_ui.py   # opens at localhost:7734
```

Happy to answer questions about the agent architecture, the FORGE AST validation approach, or the BREACH canary payload design.

---

**After you post:**
- Check HN every 30 minutes for the first 4 hours
- Reply to EVERY comment — even short ones get a full response
- If someone finds a bug: "Good catch — fixing now" and actually fix it
- If someone is harsh: thank them for the feedback, don't argue
- Don't post the link anywhere else for the first 2 hours — let organic HN momentum build

---

## REDDIT POSTS (post AFTER HN — 2 days later)

### POST 1 → r/netsec
**Best time:** Tuesday or Wednesday, 10AM–2PM EST
**Rule:** Comment on 5 existing posts in r/netsec before posting. Real comments.

**Title:**
```
I built a multi-agent security scanner that writes its own exploit scripts when existing tools have gaps
```

**Body:**
```
Been building CIPHER — a swarm of 9 specialized AI agents that each handle a different phase of a pentest.

The piece I want feedback on is the FORGE agent. When it detects a scenario no existing Kali tool handles, it:
1. Describes the gap to an LLM
2. Gets back a Python script
3. Runs it through Python's ast module (catches os.system, eval, shell=True, etc.)
4. Sandbox-tests in subprocess with timeout
5. Executes against the authorized target

The design intent: the system's capability shouldn't be capped by the tool registry at install time.

Other agents in the swarm:
- GHOST: nmap wrapper + socket fallback, whatweb, security headers (fixed an ANSI escape code bug where whatweb --color was outputting "0m" as a fake technology name)
- SPECTER: crt.sh, robots.txt, theHarvester
- SCANNER: nikto, nuclei, SSL check, exposed path detection
- BREACH: 14 canary payloads across SQLi/XSS/SSRF/CMDi/path traversal/XXE — non-destructive, SHA-256 signed audit log per action
- MIRROR: OWASP LLM Top 10 test suite for AI-powered endpoints
- COMMANDER: plain English → mission plan, wired to Anthropic/Gemini/Groq/OpenAI/Mistral

Legal enforcement is in the architecture: scope is cryptographically signed, out-of-scope throws PermissionError.

Honest weaknesses:
- AST validator is not bulletproof (a proper Docker sandbox is the right answer)
- Degrades gracefully without Kali tools but loses a lot of capability
- BREACH's 14 canary payloads are a starting point, not comprehensive

Code: https://github.com/Daylyt-kb/cipher
FORGE logic specifically: agents/specter_scanner_forge.py
BREACH agent: agents/breach.py

Two questions:
1. Is AST-based validation the right approach or should everything run in Docker from day one?
2. What BREACH categories am I obviously missing?
```

---

### POST 2 → r/hacking
**Best time:** 2 days after r/netsec post
**Rule:** Same — comment genuinely on existing posts first

**Title:**
```
Open source tool: AI agent that red-teams other AI systems for prompt injection (OWASP LLM Top 10)
```

**Body:**
```
One agent in a security project I'm building is called MIRROR — it specifically tests AI-powered applications.

Background: 88% of organizations running AI agents in production reported security incidents last year. There's almost no open tooling to test them like a pentester would.

What MIRROR tests (10 payloads across OWASP LLM Top 10):
- LLM01 Prompt Injection: system prompt override, role confusion, indirect injection via document content, token smuggling, nested context attacks, multilingual bypass
- LLM02 Insecure output handling: JSON format injection
- LLM06 Sensitive data disclosure: probes what PII the model exposes
- LLM08 Excessive agency: does the AI perform requested actions without refusing?

Usage — works against any HTTP AI endpoint:

    from agents.mirror import MirrorAgent
    mirror = MirrorAgent()
    results = mirror.run(
        "https://your-ai-app.com/api/chat",
        scope=None,
        config={
            "payload_template": {"message": "{payload}"},
            "response_path": "response"
        }
    )

MIRROR agent file: https://github.com/Daylyt-kb/cipher/blob/main/agents/mirror.py

Genuine questions:
- Which LLM attack vectors am I missing that matter most in practice?
- Is looking for leaked terms in the response the right detection approach, or is there a better method?
- Has anyone dealt with AI systems that randomize output enough to make string-matching unreliable?
```

---

### POST 3 → r/Python
**Best time:** 1 week after HN post
**Audience:** Developers, softer crowd — lead with the code

**Title:**
```
How I'm using Python's ast module to validate LLM-generated security scripts before executing them
```

**Body:**
```
Building a security tool (CIPHER) that generates Python scripts on the fly when no existing tool handles a scenario. The hard problem: how do you safely execute code you didn't write?

Current approach using Python's ast module:

    import ast

    BLOCKED_CALLS = {"eval", "exec", "compile", "open", "__import__"}
    BLOCKED_ATTRS = {"system", "popen", "run"}  # os.system etc

    def validate(code: str) -> tuple[bool, str]:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in BLOCKED_CALLS:
                    return False, f"Blocked call: {func.id}"
                if isinstance(func, ast.Attribute) and func.attr in BLOCKED_ATTRS:
                    return False, f"Blocked attribute: {func.attr}"
        return True, "OK"

Then the validated script runs in a subprocess with timeout and output capture.

Problems I've hit:
1. LLMs sometimes wrap output in ```python blocks — need to strip before ast.parse
2. Obfuscated calls like getattr(os, "system") bypass naive AST checking
3. The validator blocks legitimate subprocess usage that the script actually needs

The right answer is probably Docker isolation, but I wanted to get something working first.

Full implementation: https://github.com/Daylyt-kb/cipher/blob/main/agents/specter_scanner_forge.py

Questions:
- Has anyone built something more robust than AST-based validation for LLM-generated code?
- Is there a sandboxing library that handles this better than hand-rolled AST walks?
- RestrictedPython — has anyone used it in production? Thoughts?
```

---

## YOUR BUILD-IN-PUBLIC TWITTER/X THREAD
Post same day as HN. Tag it #buildinpublic #cybersecurity #python

**Tweet 1:**
I just open-sourced CIPHER — a 9-agent AI security swarm I built with zero budget.

It runs on your laptop. Speaks plain English. Legal by design.

Here's the full architecture 🧵

**Tweet 2:**
The problem: AI security tools cost $50K+ and need a dedicated security team.

61% of small businesses get breached every year.
359 million businesses worldwide.
Near 0% served by existing tools.

That's the gap.

**Tweet 3:**
9 agents. Each a specialist:

🔍 GHOST — maps every open door
🌐 SPECTER — hunts what the internet already knows  
🛡️ SCANNER — finds the weaknesses
💥 BREACH — proves they're real (canary payloads only)
⚡ FORGE — writes scripts when no tool exists
🤖 MIRROR — hacks other AI systems
🧠 NEURON — learns new CVEs hourly
📋 LEDGER — plain English reports
🎯 COMMANDER — understands you

**Tweet 4:**
The FORGE agent is the part I haven't seen elsewhere.

When no Kali tool covers a scenario:
→ Describes the gap to an LLM
→ Gets back a Python script
→ Validates through AST analysis
→ Sandbox tests it
→ Deploys against the authorized target

Your capability isn't capped by the tool list.

**Tweet 5:**
Legal is architecture, not a policy.

Scope is SHA-256 signed. Out-of-scope targets throw PermissionError — not a warning. You literally cannot scan unauthorized systems.

BREACH agent: immutable audit log. SHA-256 per action. Every canary payload is non-destructive.

**Tweet 6:**
Zero budget. Built alone. Open source.

⭐ https://github.com/Daylyt-kb/cipher

Find bugs → open an issue
Break it → tell me how  
Use it → I want to know what you scan

Next up: Docker sandbox for FORGE, live CVE feed pipeline

linkedin.com/in/kebron-isaias-0716aa2b7

