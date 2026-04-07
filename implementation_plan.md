# CIPHER Launch Implementation Plan — CORRECTED
# For: AntigravityAI execution
# Project owner: Kebron Isaias
# GitHub: https://github.com/Daylyt-kb/cipher
# LinkedIn: https://www.linkedin.com/in/kebron-isaias-0716aa2b7

---

## STATUS: FILE EDITS ALREADY APPLIED
The following replacements have already been made in the files:
- `YOUR_USERNAME` → `Daylyt-kb` (in landing/index.html — 6 occurrences)
- `YOUR_GITHUB_USERNAME` → `Daylyt-kb` (in landing/index.html)
- `YOUR_HANDLE` → `Daylyt-kb` (in README.md)
- `your-email@gmail.com` → `kebronisaias0@gmail.com` (in landing/index.html)
- `YOUR_USERNAME` → `Daylyt-kb` (in LAUNCH_TODAY.md — 8 occurrences)
NO FURTHER FILE EDITS NEEDED before push.

---

## TASK 1 — GITHUB PUSH
Working directory: `C:\Users\Kebro\Documents\cipher\cipher_final`
Run these commands IN ORDER, one at a time:

```bash
cd C:\Users\Kebro\Documents\cipher\cipher_final

git init

git config user.name "Kebron Isaias"
git config user.email "kebronisaias0@gmail.com"

git add .

git commit -m "feat: CIPHER v1.0 — world's first civilian AI security swarm

9 agents: GHOST, SPECTER, SCANNER, BREACH, FORGE, MIRROR, NEURON, LEDGER, COMMANDER
Multi-provider AI: Anthropic, Gemini, OpenAI, Groq, Mistral
Legal by design: cryptographic scope enforcement
17/17 tests passing | Built by Kebron Isaias"

git remote add origin https://github.com/Daylyt-kb/cipher.git

git branch -M main

git push -u origin main
```

Pre-condition: The repo https://github.com/Daylyt-kb/cipher must exist on GitHub first.
Create it at https://github.com/new → name: cipher → Public → NO readme → Create.

After push, add these topics via GitHub UI (repo → ⚙ About → Topics):
cybersecurity, ai-agents, penetration-testing, python, kali-linux,
osint, ethical-hacking, red-team, ai-security, open-source

Verification: GET https://github.com/Daylyt-kb/cipher → expect HTTP 200, public repo

---

## TASK 2 — NETLIFY DEPLOY
Deploy the `landing/` subfolder only, NOT the full project.

Method A (manual drag-drop — fastest):
1. Go to https://app.netlify.com → "Add new site" → "Deploy manually"
2. Drag the folder at: `C:\Users\Kebro\Documents\cipher\cipher_final\landing\`
3. Site deploys in ~30 seconds
4. Note the assigned URL (e.g. https://cipher-security.netlify.app)

Method B (GitHub integration — recommended for auto-deploy):
1. https://app.netlify.com → "Add new site" → "Import from Git"
2. Connect GitHub → select repo: Daylyt-kb/cipher
3. Set:
   - Base directory: `landing`
   - Publish directory: `landing`
   - Build command: (leave empty)
4. Deploy

Site name target: `cipher-security` (set in Site settings → Site name)

After deploy, enable Netlify Forms:
Site settings → Forms → Enable form detection → ON
This activates the waitlist form on the landing page.

Verification: GET https://cipher-security.netlify.app → expect HTTP 200, page contains "CIPHER"

---

## TASK 3 — GROQ KEY SETUP (do this BEFORE revoking old keys)

1. Go to https://console.groq.com → sign up with kebronisaias0@gmail.com
2. Create new API key → copy it (starts with `gsk_`)
3. Test it works:
```bash
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer gsk_YOUR_GROQ_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"say CIPHER ONLINE"}],"max_tokens":10}'
```
Expect: response contains "CIPHER ONLINE" or similar

4. Set environment variable for local use:
   On Windows (CMD): `setx GROQ_API_KEY "gsk_YOUR_GROQ_KEY"`
   On WSL/bash: Add `export GROQ_API_KEY="gsk_YOUR_GROQ_KEY"` to ~/.bashrc

---

## TASK 4 — KEY REVOCATION (do this AFTER Groq key confirmed working)

Revoke Gemini key:
1. https://aistudio.google.com/app/apikey
2. Find key starting with AIzaSyAS4k4w... → Delete

Revoke Anthropic key:
1. https://console.anthropic.com/settings/keys
2. Find key starting with sk-ant-api03-E-tozL4... → Revoke

DO NOT store the old keys anywhere. DO NOT create a LAUNCH_LOG.md with credentials.
Security hygiene: never log API keys in files, even temporarily.

---

## TASK 5 — X (TWITTER) POST
Post this thread in sequence. Each tweet is one post, reply to the previous one.

Tweet 1 (main post):
```
I just open-sourced CIPHER — a 9-agent AI security swarm built with zero budget.

Runs on your laptop. Speaks plain English. Legal by design.

Architecture thread 🧵
```

Tweet 2 (reply to tweet 1):
```
The problem: AI security tools cost $50K+ and need a dedicated security team.

61% of small businesses get breached every year.
359 million businesses worldwide.
Near 0% served by existing tools.

That's the gap CIPHER closes.
```

Tweet 3 (reply to tweet 2):
```
9 agents, each a specialist:

🔍 GHOST — maps every open door
🌐 SPECTER — hunts public intel
🛡️ SCANNER — finds weaknesses
💥 BREACH — proves they're real
⚡ FORGE — writes scripts when no tool exists
🤖 MIRROR — hacks other AI systems
🧠 NEURON — learns new CVEs hourly
📋 LEDGER — plain English reports
🎯 COMMANDER — understands you
```

Tweet 4 (reply to tweet 3):
```
The FORGE agent is the piece I haven't seen elsewhere.

When no Kali tool covers a scenario:
→ Describes the gap to an LLM
→ Gets back a Python script
→ Validates through AST analysis
→ Sandbox tests it
→ Deploys against the authorized target

Capability isn't capped by the tool list.
```

Tweet 5 (reply to tweet 4):
```
Legal is architecture, not policy.

Scope is SHA-256 signed. Out-of-scope targets throw PermissionError — not a warning.

BREACH agent: every action has an immutable, SHA-256-signed audit log.
All payloads are non-destructive canaries.
```

Tweet 6 (reply to tweet 5):
```
Zero budget. Built alone. Open source.

⭐ https://github.com/Daylyt-kb/cipher

Find bugs → open an issue
Break it → tell me how
Use it → I want to know

Next: Docker sandbox for FORGE, live CVE pipeline

Built by Kebron Isaias
linkedin.com/in/kebron-isaias-0716aa2b7
```

---

## TASK 6 — LINKEDIN PROFILE UPDATE
Go to https://www.linkedin.com/in/kebron-isaias-0716aa2b7 → Edit profile

Update the Headline to:
```
Building CIPHER — AI Security Swarm | Python | Cybersecurity | Open Source
```

Update the About section to:
```
I build things with zero budget and a lot of conviction.

Currently: CIPHER — the world's first civilian AI security swarm. 9 specialized agents (GHOST, SPECTER, SCANNER, BREACH, FORGE, MIRROR, NEURON, LEDGER, COMMANDER) that orchestrate Kali Linux tools from a browser. Plain English interface. Legal by design. Multi-provider AI (Anthropic, Gemini, Groq, OpenAI, Mistral).

Built alone. Zero budget. 17/17 tests passing.

Open source: github.com/Daylyt-kb/cipher

I'm interested in: cybersecurity, AI agents, Python, open source, and building tools that give small businesses enterprise-grade security at zero cost.

If you're a developer, security researcher, MSSP, or just someone who wants their website tested — reach out.
```

Add to Featured section:
- Add the GitHub link: https://github.com/Daylyt-kb/cipher
- Add the Netlify landing page: https://cipher-security.netlify.app

Note: "LinkedIn Upgrade" in the original plan = profile CONTENT update only. No subscription purchase needed or requested.

---

## TASK 7 — HACKER NEWS POST
Post at: https://news.ycombinator.com/submit
WHEN: Tuesday or Wednesday, 9:00–11:00 AM EST only. Do not post outside this window.
If today is not Tuesday/Wednesday OR outside 9–11AM EST: schedule for next applicable window.

Title (copy exactly):
```
Show HN: CIPHER – 9 AI agents that orchestrate Kali Linux tools from your browser
```

Body: Copy from `LAUNCH_TODAY.md` → Step 3 → the full body between the `---` markers.

After posting: monitor replies every 30 minutes for 4 hours. Reply to every comment.

---

## TASK 8 — CIPHER LOGO
The logo has been designed and rendered. It is an SVG with:
- Dark background (#080808)
- Red (#e24b4a) hexagonal frame representing the 6 core agent groups
- Central targeting crosshair with center dot
- "CIPHER" wordmark in Share Tech Mono, 52px, letter-spacing 14
- "AI SECURITY SWARM" tagline
- "LEGAL BY DESIGN" sub-tagline
- "9 AGENTS" badge top right
- Corner bracket accents

To use as an image:
1. Save the SVG file (cipher_logo.svg) from the cipher_final folder
2. Use it as profile picture on X (Twitter) by exporting to PNG at 400x400
3. Use it as the og:image in landing/index.html by hosting it on Netlify and updating the meta tag

To convert SVG to PNG on Windows:
- Open cipher_logo.svg in Chrome → right-click → "Save as" PNG, or
- Use https://svgtopng.com — upload, download 400x400 PNG

---

## VERIFICATION CHECKLIST
After each task, verify:

- [ ] GitHub: https://github.com/Daylyt-kb/cipher → public, has code, has topics
- [ ] Netlify: https://cipher-security.netlify.app → loads, shows CIPHER landing page
- [ ] Groq key: curl test returns CIPHER ONLINE
- [ ] Old keys: Gemini and Anthropic keys revoked
- [ ] X thread: 6-tweet thread posted, thread intact
- [ ] LinkedIn: headline + about updated, GitHub featured
- [ ] HN post: posted at correct time window

---

## WHAT NOT TO DO
- Do NOT create LAUNCH_LOG.md with API keys — never store credentials in plaintext files
- Do NOT post the HN link on Reddit or Twitter within the first 2 hours after HN post
- Do NOT commit the .env file or any file containing API keys
- Do NOT push the cipher_output/ folder contents (scan results, consent records)
- Do NOT purchase LinkedIn Premium — update content only
- Do NOT post the HN thread outside the Tuesday/Wednesday 9-11AM EST window

