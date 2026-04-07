"""
CIPHER Web UI — Local Browser Interface
Run this on your laptop, open http://localhost:7734 in your browser.
No cloud. No hosting. Zero cost.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from flask import Flask, render_template_string, request, jsonify, Response
    FLASK = True
except ImportError:
    FLASK = False
    print("Flask not installed. Run: pip install flask")
    sys.exit(1)

from agents.ghost import GhostAgent
from agents.specter_scanner_forge import SpecterAgent, ScannerAgent, ForgeAgent
from agents.neuron_ledger import LedgerAgent
from agents.mirror import MirrorAgent
from agents.commander import Commander
from core.bus import MessageBus
from core.scope import ScopeValidator

app = Flask(__name__)

# In-memory mission store (no database needed)
missions = {}
active_mission = {"id": None, "log": [], "status": "idle"}
from core.ai_provider import AIProvider, PROVIDERS

config = {
    "api_key": os.environ.get("GROQ_API_KEY") or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY") or "",
    "provider": "",
    "model": "",
}

# Auto-detect provider if key exists in env
if config["api_key"]:
    for pid, pinfo in PROVIDERS.items():
        if pid in ["anthropic", "gemini", "groq", "openai"]:
             # Simple heuristic for boot
             if pid == "anthropic" and config["api_key"].startswith("sk-ant"): config["provider"] = pid
             elif pid == "groq" and config["api_key"].startswith("gsk_"): config["provider"] = pid
             elif pid == "gemini" and config["api_key"].startswith("AIza"): config["provider"] = pid
             elif pid == "openai" and config["api_key"].startswith("sk-"): config["provider"] = pid
    
    if config["provider"]:
        config["model"] = PROVIDERS[config["provider"]]["default_model"]

def get_ai():
    return AIProvider(config["api_key"], config["provider"], config["model"])

# ─────────────────────────────────────────────────────────────────────────────
# HTML TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CIPHER — AI Security Swarm</title>
<style>
  :root {
    --bg: #0a0a0a;
    --surface: #111;
    --surface2: #1a1a1a;
    --border: #222;
    --red: #e24b4a;
    --red-dim: #7a2020;
    --green: #3d9a3d;
    --amber: #c17a10;
    --blue: #2a6db5;
    --text: #e0e0e0;
    --muted: #666;
    --mono: 'Courier New', monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; min-height: 100vh; }

  /* TOP NAV */
  .nav { display: flex; align-items: center; gap: 12px; padding: 12px 24px; border-bottom: 1px solid var(--border); background: var(--surface); }
  .nav-logo { font-family: var(--mono); font-size: 18px; font-weight: bold; color: var(--red); letter-spacing: 2px; }
  .nav-tag { font-size: 10px; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; }
  .nav-status { margin-left: auto; display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--muted); }
  .status-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

  /* LAYOUT */
  .layout { display: grid; grid-template-columns: 320px 1fr; height: calc(100vh - 49px); }
  .sidebar { border-right: 1px solid var(--border); padding: 20px; overflow-y: auto; background: var(--surface); }
  .main { display: flex; flex-direction: column; overflow: hidden; }

  /* SIDEBAR */
  .section-label { font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }

  /* INPUT FORM */
  .form-group { margin-bottom: 14px; }
  label { display: block; font-size: 11px; color: var(--muted); margin-bottom: 5px; letter-spacing: 0.5px; }
  input[type=text], select, textarea {
    width: 100%; background: var(--surface2); border: 1px solid var(--border); border-radius: 6px;
    color: var(--text); padding: 8px 10px; font-size: 13px; outline: none;
    transition: border-color .15s;
  }
  input[type=text]:focus, select:focus, textarea:focus { border-color: var(--red-dim); }

  /* CONSENT CHECKBOX */
  .consent-box { background: var(--surface2); border: 1px solid var(--red-dim); border-radius: 6px; padding: 10px; margin-bottom: 14px; }
  .consent-box label { color: #e0a0a0; font-size: 11px; line-height: 1.5; display: flex; gap: 8px; align-items: flex-start; cursor: pointer; }
  .consent-box input[type=checkbox] { margin-top: 2px; flex-shrink: 0; accent-color: var(--red); }

  /* BUTTONS */
  .btn { width: 100%; padding: 10px; border-radius: 6px; font-size: 13px; font-weight: 700; cursor: pointer; transition: all .15s; border: none; letter-spacing: 0.5px; }
  .btn-primary { background: var(--red); color: white; }
  .btn-primary:hover { background: #c53d3c; }
  .btn-primary:disabled { background: var(--red-dim); opacity: .5; cursor: not-allowed; }
  .btn-secondary { background: transparent; border: 1px solid var(--border); color: var(--muted); margin-top: 6px; }
  .btn-secondary:hover { border-color: var(--text); color: var(--text); }

  /* AGENTS */
  .agents-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 16px; }
  .agent-chip { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 7px 8px; font-size: 11px; }
  .agent-chip.active { border-color: var(--green); }
  .agent-name { font-weight: 700; color: var(--text); font-family: var(--mono); font-size: 10px; }
  .agent-role { color: var(--muted); font-size: 10px; margin-top: 1px; }
  .agent-chip.active .agent-name { color: var(--green); }

  /* MAIN AREA */
  .terminal { flex: 1; overflow-y: auto; padding: 20px; font-family: var(--mono); font-size: 12px; line-height: 1.7; }
  .terminal-line { margin-bottom: 2px; }
  .terminal-line.cmd { color: var(--red); }
  .terminal-line.info { color: var(--text); }
  .terminal-line.success { color: var(--green); }
  .terminal-line.warning { color: var(--amber); }
  .terminal-line.error { color: var(--red); }
  .terminal-line.muted { color: var(--muted); }

  /* CHAT INPUT */
  .chat-area { border-top: 1px solid var(--border); padding: 14px 20px; display: flex; gap: 10px; background: var(--surface); }
  .chat-input { flex: 1; background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; color: var(--text); padding: 10px 14px; font-size: 13px; outline: none; }
  .chat-input:focus { border-color: var(--red-dim); }
  .chat-send { padding: 10px 18px; background: var(--red); color: white; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; }
  .chat-send:hover { background: #c53d3c; }

  /* RESULTS PANEL */
  .results { border-top: 1px solid var(--border); padding: 14px 20px; max-height: 300px; overflow-y: auto; }
  .finding { padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; font-size: 12px; border-left: 3px solid transparent; }
  .finding.critical { background: #1a0505; border-color: var(--red); }
  .finding.high { background: #1a0a05; border-color: #e87040; }
  .finding.medium { background: #1a1505; border-color: var(--amber); }
  .finding.low { background: #051a10; border-color: var(--green); }
  .finding.info { background: var(--surface2); border-color: var(--border); }
  .finding-sev { font-size: 9px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px; }
  .finding-title { color: var(--text); }
  .finding-tool { font-size: 10px; color: var(--muted); margin-top: 2px; }

  /* TABS */
  .tabs { display: flex; border-bottom: 1px solid var(--border); background: var(--surface); padding: 0 20px; }
  .tab { padding: 10px 16px; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; color: var(--muted); cursor: pointer; border-bottom: 2px solid transparent; transition: all .15s; }
  .tab.active { color: var(--text); border-color: var(--red); }
  .tab-panel { display: none; flex: 1; overflow: auto; }
  .tab-panel.active { display: flex; flex-direction: column; }

  /* BANNER */
  .cipher-banner { font-family: var(--mono); color: var(--red); font-size: 11px; line-height: 1.3; padding: 20px; white-space: pre; }
  .welcome-msg { padding: 0 20px 10px; color: var(--muted); font-size: 12px; line-height: 1.7; }

  /* REPORT */
  .report-area { padding: 20px; font-size: 13px; line-height: 1.7; white-space: pre-wrap; font-family: var(--mono); color: var(--text); }
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-logo">CIPHER</div>
  <div class="nav-tag">AI Security Swarm · v0.1</div>
  <div class="nav-status">
    <div class="status-dot"></div>
    <span id="status-text">Ready</span>
  </div>
</nav>

<div class="layout">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="section-label">Mission Control</div>

    <div class="form-group">
      <label>Target (domain or IP you own)</label>
      <input type="text" id="target" placeholder="mysite.com or 192.168.1.1">
    </div>

    <div class="form-group">
      <label>Scan Mode</label>
      <select id="mode">
        <option value="recon">Recon — surface mapping</option>
        <option value="osint">OSINT — open source intel</option>
        <option value="scan">Scan — vulnerability detection</option>
        <option value="full">Full Swarm — everything</option>
        <option value="breach">Breach — full exploitation</option>
        <option value="ai-audit">AI Audit — MIRROR agent</option>
      </select>
    </div>

    <div class="consent-box">
      <label>
        <input type="checkbox" id="authorized">
        I confirm I own this target or have written authorization to test it.
        Unauthorized scanning is illegal.
      </label>
    </div>

    <button class="btn btn-primary" id="launch-btn" onclick="launchMission()">
      ⚡ Deploy Swarm
    </button>
    <button class="btn btn-secondary" onclick="clearTerminal()">Clear Terminal</button>

    <div style="margin-top: 20px; margin-bottom: 10px;">
      <div class="section-label">Agent Status</div>
      <div class="agents-grid" id="agents-grid">
        <div class="agent-chip" id="agent-ghost"><div class="agent-name">GHOST</div><div class="agent-role">Recon</div></div>
        <div class="agent-chip" id="agent-specter"><div class="agent-name">SPECTER</div><div class="agent-role">OSINT</div></div>
        <div class="agent-chip" id="agent-scanner"><div class="agent-name">SCANNER</div><div class="agent-role">Vuln Scan</div></div>
        <div class="agent-chip" id="agent-forge"><div class="agent-name">FORGE</div><div class="agent-role">Scripts</div></div>
        <div class="agent-chip" id="agent-mirror"><div class="agent-name">MIRROR</div><div class="agent-role">AI-vs-AI</div></div>
        <div class="agent-chip" id="agent-ledger"><div class="agent-name">LEDGER</div><div class="agent-role">Reports</div></div>
      </div>
    </div>

    <div style="margin-top: 16px;">
      <div class="section-label">Quick Commands</div>
      <button class="btn btn-secondary" style="margin-bottom:4px" onclick="quickSend('check security headers')">Check headers</button>
      <button class="btn btn-secondary" style="margin-bottom:4px" onclick="quickSend('enumerate subdomains')">Find subdomains</button>
      <button class="btn btn-secondary" style="margin-bottom:4px" onclick="quickSend('forge a port scan script')">Generate script</button>
      <button class="btn btn-secondary" onclick="quickSend('fetch latest CVEs')">Latest CVEs</button>
    </div>
  </aside>

  <!-- MAIN -->
  <main class="main">
    <div class="tabs">
      <div class="tab active" onclick="showTab('terminal')">Terminal</div>
      <div class="tab" onclick="showTab('findings')">Findings <span id="findings-count"></span></div>
      <div class="tab" onclick="showTab('report')">Report</div>
      <div class="tab" onclick="showTab('commander')">Commander</div>
      <div class="tab" onclick="showTab('settings')">⚙ Settings</div>
    </div>

    <!-- TERMINAL TAB -->
    <div class="tab-panel active" id="tab-terminal">
      <div class="terminal" id="terminal">
        <div class="cipher-banner">  ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ 
 ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
 ██║     ██║██████╔╝███████║█████╗  ██████╔╝
 ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
 ╚██████╗██║██║     ██║  ██║███████╗██║  ██║
  ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝</div>
        <div class="welcome-msg">The World's First Civilian AI Security Swarm. Legal by design.<br>Enter a target, confirm authorization, and deploy the swarm.</div>
      </div>
    </div>

    <!-- FINDINGS TAB -->
    <div class="tab-panel" id="tab-findings">
      <div class="results" id="findings-list" style="max-height:100%">
        <div style="color: var(--muted); font-size: 12px; padding: 20px;">
          Run a scan to see findings here.
        </div>
      </div>
    </div>

    <!-- REPORT TAB -->
    <div class="tab-panel" id="tab-report">
      <div class="report-area" id="report-content">
        No report generated yet. Run a full scan first.
      </div>
    </div>


    <!-- SETTINGS TAB -->
    <div class="tab-panel" id="tab-settings" style="display:none; flex-direction:column; overflow-y:auto">
      <div style="padding:20px; border-bottom: 1px solid var(--color-border, #222)">
        <div style="font-size:15px; font-weight:700; margin-bottom:5px">AI Provider Settings</div>
        <div style="font-size:12px; color:var(--muted, #666)">Paste any API key — CIPHER detects the provider automatically. Switch anytime, no restart needed.</div>
      </div>
      <div style="padding:20px">
        <div style="display:flex; gap:8px; margin-bottom:12px">
          <input type="password" id="raw-key" placeholder="Paste API key (Gemini, Anthropic, OpenAI, Groq...)" style="flex:1; background:#1a1a1a; border:1px solid #333; color:#e0e0e0; padding:9px 12px; border-radius:6px; font-family:monospace; font-size:12px">
          <button onclick="setRawKey()" style="padding:9px 16px; background:#e24b4a; color:#fff; border:none; border-radius:6px; font-weight:700; cursor:pointer">Set Key</button>
        </div>
        <div id="raw-status" style="font-size:12px; font-family:monospace; color:#5cb85c; margin-bottom:20px"></div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px" id="provider-cards"></div>
        <div style="margin-top:20px; font-size:11px; color:#666; line-height:1.7">
          <strong style="color:#aaa">Free providers:</strong><br>
          • Groq — <a href="https://console.groq.com" target="_blank" style="color:#5a9adc">console.groq.com</a> (Llama 3.3 70B, fast)<br>
          • Gemini — <a href="https://aistudio.google.com" target="_blank" style="color:#5a9adc">aistudio.google.com</a> (Gemini 1.5 Flash/Pro)<br>
          <strong style="color:#aaa">Paid providers:</strong><br>
          • Anthropic — <a href="https://console.anthropic.com" target="_blank" style="color:#5a9adc">console.anthropic.com</a><br>
          • OpenAI — <a href="https://platform.openai.com" target="_blank" style="color:#5a9adc">platform.openai.com</a>
        </div>
      </div>
    </div>
    <!-- COMMANDER TAB -->
    <div class="tab-panel" id="tab-commander" style="display:none; flex-direction:column">
      <div class="terminal" id="commander-log" style="flex:1">
        <div class="terminal-line muted">Commander shell — talk in plain English.</div>
        <div class="terminal-line muted">Examples: "scan mysite.com" / "osint target.com" / "forge a script to check SSL"</div>
        <br>
      </div>
      <div class="chat-area">
        <input class="chat-input" id="chat-input" placeholder="Tell Commander what to do..." onkeydown="if(event.key==='Enter')sendToCommander()">
        <button class="chat-send" onclick="sendToCommander()">Send</button>
      </div>
    </div>
  </main>
</div>

<script>
let allFindings = [];
let missionRunning = false;

function log(msg, type='info') {
  const t = document.getElementById('terminal');
  const div = document.createElement('div');
  div.className = 'terminal-line ' + type;
  div.textContent = '[' + new Date().toLocaleTimeString() + '] ' + msg;
  t.appendChild(div);
  t.scrollTop = t.scrollHeight;
}

function clearTerminal() {
  document.getElementById('terminal').innerHTML = '<div class="terminal-line muted">Terminal cleared.</div>';
}

function showTab(name) {
  document.querySelectorAll('.tab').forEach((t,i) => {
    const names = ['terminal','findings','report','commander'];
    t.classList.toggle('active', names[i] === name);
  });
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.remove('active');
    p.style.display = 'none';
  });
  const panel = document.getElementById('tab-' + name);
  panel.style.display = 'flex';
  panel.classList.add('active');
}

function setAgentActive(name, active) {
  const el = document.getElementById('agent-' + name);
  if (el) el.classList.toggle('active', active);
}

function quickSend(msg) {
  document.getElementById('chat-input').value = msg;
  showTab('commander');
  sendToCommander();
}

async function launchMission() {
  const target = document.getElementById('target').value.trim();
  const mode = document.getElementById('mode').value;
  const authorized = document.getElementById('authorized').checked;

  if (!target) { log('Error: No target specified.', 'error'); return; }
  if (!authorized) { log('Error: You must confirm authorization before scanning.', 'error'); return; }
  if (missionRunning) { log('Mission already running...', 'warning'); return; }

  missionRunning = true;
  allFindings = [];
  document.getElementById('launch-btn').disabled = true;
  document.getElementById('launch-btn').textContent = '⏳ Running...';
  document.getElementById('findings-list').innerHTML = '';
  document.getElementById('findings-count').textContent = '';

  showTab('terminal');
  log(`Mission start: ${mode.toUpperCase()} on ${target}`, 'cmd');
  log('Validating scope and authorization...', 'muted');

  const agents = {
    recon: ['ghost'],
    osint: ['specter'],
    scan: ['scanner'],
    full: ['ghost', 'specter', 'scanner'],
    'ai-audit': ['mirror']
  };

  const agentList = agents[mode] || ['ghost'];
  agentList.forEach(a => setAgentActive(a, false));

  try {
    const resp = await fetch('/api/mission', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({target, mode, authorized})
    });
    const data = await resp.json();

    if (data.error) {
      log('Error: ' + data.error, 'error');
    } else {
      // Stream the mission log
      await streamMission(data.mission_id, agentList);
    }
  } catch(e) {
    log('Connection error: ' + e.message, 'error');
  }

  missionRunning = false;
  document.getElementById('launch-btn').disabled = false;
  document.getElementById('launch-btn').textContent = '⚡ Deploy Swarm';
  agentList.forEach(a => setAgentActive(a, false));
}

async function streamMission(missionId, agentList) {
  // Poll for updates
  let done = false;
  let lastLine = 0;
  agentList.forEach(a => setAgentActive(a, true));

  while (!done) {
    try {
      const resp = await fetch(`/api/mission/${missionId}/status`);
      const data = await resp.json();

      // Show new log lines
      const lines = data.log || [];
      for (let i = lastLine; i < lines.length; i++) {
        const entry = lines[i];
        log(entry.msg, entry.type || 'info');
        lastLine = i + 1;
      }

      // Show findings
      if (data.findings && data.findings.length > allFindings.length) {
        const newFindings = data.findings.slice(allFindings.length);
        newFindings.forEach(addFinding);
        allFindings = data.findings;
        document.getElementById('findings-count').textContent = `(${allFindings.length})`;
      }

      if (data.status === 'complete') {
        done = true;
        log(`Mission complete. ${allFindings.length} findings. Report saved.`, 'success');
        if (data.report) {
          document.getElementById('report-content').textContent = data.report;
        }
      } else if (data.status === 'error') {
        done = true;
        log('Mission error: ' + (data.error || 'unknown'), 'error');
      }

      if (!done) await new Promise(r => setTimeout(r, 800));
    } catch(e) {
      await new Promise(r => setTimeout(r, 1000));
    }
  }
}

function addFinding(f) {
  const list = document.getElementById('findings-list');
  const sev = f.severity || 'info';
  const div = document.createElement('div');
  div.className = 'finding ' + sev;
  div.innerHTML = `
    <div class="finding-sev">${sev}</div>
    <div class="finding-title">${f.title || ''}</div>
    <div class="finding-tool">Tool: ${f.tool || 'unknown'}</div>
  `;
  list.appendChild(div);
}

async function sendToCommander() {
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';

  const log_el = document.getElementById('commander-log');
  const you = document.createElement('div');
  you.className = 'terminal-line cmd';
  you.textContent = '> ' + msg;
  log_el.appendChild(you);

  try {
    const resp = await fetch('/api/commander', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: msg})
    });
    const data = await resp.json();
    const reply = document.createElement('div');
    reply.className = 'terminal-line info';
    reply.style.whiteSpace = 'pre-wrap';
    reply.textContent = 'Commander: ' + (data.response || data.error || 'no response');
    log_el.appendChild(reply);
    log_el.scrollTop = log_el.scrollHeight;
  } catch(e) {
    const err = document.createElement('div');
    err.className = 'terminal-line error';
    err.textContent = 'Error: ' + e.message;
    log_el.appendChild(err);
  }
}

async function refreshAIStatus(){
  try{
    const r = await fetch('/api/ai-status');
    const d = await r.json();
    buildProviderCards(d.all_providers, d.provider);
    const statusEl = document.getElementById('ai-status');
    if(statusEl){
      statusEl.textContent = d.configured ? d.provider_name + ' · ' + (d.model||'').split('-').slice(0,2).join('-') : 'No AI key — add in Settings';
      statusEl.style.color = d.configured ? '#5cb85c' : '#e24b4a';
    }
  }catch(e){}
}
function buildProviderCards(providers, activeProvider){
  const grid = document.getElementById('provider-cards');
  if(!providers || !grid) return;
  grid.innerHTML = Object.entries(providers).map(([id,info])=>`
    <div style="background:#111; border:1px solid ${id===activeProvider?'#3d9a3d':'#222'}; border-radius:8px; padding:14px">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px">
        <span style="font-weight:700; font-size:13px">${info.name}</span>
        <span style="font-size:10px; padding:2px 8px; border-radius:10px; background:${info.free_tier?'#0a2a0a':'#1a1a2a'}; color:${info.free_tier?'#5cb85c':'#7a9adc'}; border:1px solid ${info.free_tier?'#2d5a2d':'#3a4a7a'}">${info.free_tier?'FREE':'PAID'}</span>
      </div>
      <div style="font-size:11px; color:#666; margin-bottom:8px">${info.models.slice(0,2).join(', ')}</div>
      <div style="display:flex; gap:6px; margin-bottom:8px">
        <input type="password" id="key-${id}" placeholder="${info.key_prefix}..." style="flex:1; background:#1a1a1a; border:1px solid #333; color:#e0e0e0; padding:6px 8px; border-radius:5px; font-family:monospace; font-size:11px">
        <button onclick="setKeyFor('${id}')" style="padding:6px 10px; background:#e24b4a; color:#fff; border:none; border-radius:5px; font-size:11px; cursor:pointer">Set</button>
        <button onclick="testKeyFor('${id}')" style="padding:6px 10px; background:#1a1a1a; color:#aaa; border:1px solid #333; border-radius:5px; font-size:11px; cursor:pointer">Test</button>
      </div>
      <div id="ps-${id}" style="font-size:11px; color:#777; font-family:monospace">${id===activeProvider?'✓ Active':'—'}</div>
      <div style="font-size:10px; color:#555; margin-top:5px">Get key: <a href="${info.docs}" target="_blank" style="color:#5a9adc">${info.docs.replace('https://','')}</a></div>
    </div>`).join('');
}
async function setKeyFor(provider){
  const key=(document.getElementById('key-'+provider)||{}).value||'';
  if(!key){document.getElementById('ps-'+provider).textContent='⚠ Paste key first';return;}
  const r=await fetch('/api/set-key',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key,provider})});
  const d=await r.json();
  document.getElementById('ps-'+provider).textContent=d.ok?'✓ Set: '+d.model:'✗ '+d.error;
  document.getElementById('key-'+provider).value='';
  refreshAIStatus();
}
async function testKeyFor(provider){
  const key=(document.getElementById('key-'+provider)||{}).value||'';
  const el=document.getElementById('ps-'+provider);
  el.textContent='Testing...';
  const r=await fetch('/api/test-key',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:key||null,provider})});
  const d=await r.json();
  el.textContent=d.ok?'✓ Working: '+d.response.slice(0,35):'✗ '+d.error;
}
async function setRawKey(){
  const key=document.getElementById('raw-key').value.trim();
  if(!key)return;
  const r=await fetch('/api/set-key',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key})});
  const d=await r.json();
  document.getElementById('raw-status').textContent=d.ok?'✓ '+d.provider_name+' detected — using '+d.model:'✗ '+d.error;
  document.getElementById('raw-key').value='';
  refreshAIStatus();
}
refreshAIStatus(); setInterval(refreshAIStatus,20000);

</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/mission", methods=["POST"])
def start_mission():
    data = request.get_json()
    target = data.get("target", "").strip()
    mode = data.get("mode", "recon")
    authorized = data.get("authorized", False)

    if not target:
        return jsonify({"error": "No target specified"}), 400
    if not authorized:
        return jsonify({"error": "Authorization required"}), 403

    mission_id = f"m_{int(time.time())}_{target.replace('.', '_')}"
    missions[mission_id] = {
        "id": mission_id,
        "target": target,
        "mode": mode,
        "status": "running",
        "log": [],
        "findings": [],
        "report": "",
        "error": ""
    }

    # Run mission in background thread
    thread = threading.Thread(
        target=run_mission_background,
        args=(mission_id, target, mode),
        daemon=True
    )
    thread.start()

    return jsonify({"mission_id": mission_id})


@app.route("/api/mission/<mission_id>/status")
def mission_status(mission_id):
    m = missions.get(mission_id)
    if not m:
        return jsonify({"error": "Mission not found"}), 404
    return jsonify({
        "status": m["status"],
        "log": m["log"],
        "findings": m["findings"],
        "report": m["report"],
        "error": m["error"]
    })


@app.route("/api/commander", methods=["POST"])
def commander_chat():
    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message"}), 400

    bus = MessageBus()
    cmd = Commander(api_key=config["api_key"])
    agents = {
        "ghost": GhostAgent(bus),
        "specter": SpecterAgent(bus),
        "scanner": ScannerAgent(bus),
        "forge": ForgeAgent(bus, api_key=config["api_key"]),
        "ledger": LedgerAgent(bus),
    }

    try:
        response = cmd.process(message, agents, bus)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_mission_background(mission_id: str, target: str, mode: str):
    """Run a mission in background, posting progress to mission store."""
    m = missions[mission_id]

    def log(msg, t="info"):
        m["log"].append({"msg": msg, "type": t, "ts": datetime.now().isoformat()})

    def add_findings(findings):
        m["findings"].extend(findings)

    try:
        bus = MessageBus()
        results = {}
        ai = get_ai()

        # GHOST
        if mode in ("recon", "full", "breach"):
            log("[GHOST] Mapping attack surface...", "cmd")
            result = GhostAgent(bus).run(target, None)
            results["recon"] = result
            add_findings(result.get("findings", []))
            log(f"[GHOST] {result.get('summary', 'Complete')}", "success")

        # SPECTER
        if mode in ("osint", "full"):
            log("[SPECTER] Running OSINT sweep...", "cmd")
            result = SpecterAgent(bus).run(target, None)
            results["osint"] = result
            add_findings(result.get("findings", []))
            log(f"[SPECTER] {result.get('summary', 'Complete')}", "success")

        # SCANNER
        if mode in ("scan", "full", "breach"):
            log("[SCANNER] Hunting vulnerabilities...", "cmd")
            result = ScannerAgent(bus).run(target, None)
            results["scan"] = result
            add_findings(result.get("findings", []))
            log(f"[SCANNER] {result.get('summary', 'Complete')}", "success")

        # BREACH — controlled exploitation
        if mode in ("breach", "full"):
            log("[BREACH] Starting controlled exploitation...", "cmd")
            log("[BREACH] Non-destructive canary payloads only. Audit trail active.", "muted")
            try:
                from agents.breach import BreachAgent
                from core.scope import ScopeValidator
                scope = ScopeValidator(target)
                scanner_findings = results.get("scan", {}).get("findings", [])
                breach_result = BreachAgent(bus, api_key=ai.api_key).run(
                    target, scope,
                    scanner_findings=scanner_findings,
                    require_approval=False
                )
                results["breach"] = breach_result
                add_findings(breach_result.get("findings", []))
                log(f"[BREACH] {breach_result.get('summary', 'Complete')}", "success")
                if breach_result.get("audit_file"):
                    log(f"[BREACH] Audit trail: {breach_result['audit_file']}", "muted")
            except Exception as be:
                log(f"[BREACH] Error: {be}", "error")

        # MIRROR — AI-vs-AI red team
        if mode == "ai-audit":
            log("[MIRROR] AI red team ready.", "cmd")
            log("[MIRROR] Enter the AI endpoint URL in Commander tab to test.", "warning")
            log("[MIRROR] Example: 'mirror https://your-chatbot.com/api/chat'", "muted")

        # LEDGER report
        log("[LEDGER] Generating report...", "cmd")
        report = LedgerAgent(bus).generate(target, results, mission_id, ai.api_key)

        output_dir = Path("./cipher_output")
        output_dir.mkdir(exist_ok=True)
        report_file = output_dir / f"{mission_id}_report.md"
        with open(report_file, "w") as f:
            f.write(report.get("markdown", ""))

        m["report"] = report.get("markdown", "")
        m["risk_level"] = report.get("risk_level", "")
        m["status"] = "complete"
        log(f"Mission complete. Report: {report_file}", "success")

    except Exception as e:
        m["status"] = "error"
        m["error"] = str(e)
        m["log"].append({"msg": f"Mission failed: {e}", "type": "error"})




@app.route("/api/ai-status")
def ai_status():
    ai = get_ai()
    s = ai.status()
    s["all_providers"] = PROVIDERS
    return jsonify(s)

@app.route("/api/set-key", methods=["POST"])
def set_key():
    data = request.get_json()
    key = (data.get("key") or "").strip()
    explicit_provider = data.get("provider","")
    if not key:
        return jsonify({"ok":False,"error":"No key"}), 400
    detected = explicit_provider or AIProvider.detect_from_key(key)
    info = PROVIDERS.get(detected, {})
    config["api_key"] = key
    config["provider"] = detected
    config["model"] = info.get("default_model","")
    return jsonify({"ok":True,"provider":detected,"provider_name":info.get("name",detected),"model":config["model"]})

@app.route("/api/test-key", methods=["POST"])
def test_key():
    data = request.get_json()
    key = data.get("key") or config["api_key"]
    provider = data.get("provider","")
    if not key:
        return jsonify({"ok":False,"error":"No key"}), 400
    detected = provider or AIProvider.detect_from_key(key)
    ai = AIProvider(key, detected)
    try:
        resp = ai.complete("Reply: CIPHER ONLINE", max_tokens=20)
        if resp.startswith("[AI]"):
            return jsonify({"ok":False,"error":resp})
        return jsonify({"ok":True,"response":resp,"provider":detected})
    except Exception as e:
        return jsonify({"ok":False,"error":str(e)[:150]})

def main():
    print("\n" + "="*50)
    print("  CIPHER Web UI")
    print("  http://localhost:7734")
    print("="*50)
    if config["api_key"]:
        print(f"  AI Mode: ON (Brain activated)")
    else:
        print("  AI Mode: OFF (set API_KEY for AI analysis)")
    print("  Legal: Only scan targets you own or have authorization for")
    print("="*50 + "\n")
    app.run(host="127.0.0.1", port=7734, debug=False)


if __name__ == "__main__":
    main()


@app.route("/api/neuron/stats")
def neuron_stats():
    try:
        from agents.neuron import NeuronAgent
        n = NeuronAgent()
        return jsonify(n.stats())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/neuron/cves")
def neuron_cves():
    try:
        from agents.neuron import NeuronAgent
        n = NeuronAgent()
        cves = n.get_critical_cves(days_back=30, limit=20)
        return jsonify({"cves": cves, "count": len(cves)})
    except Exception as e:
        return jsonify({"error": str(e), "cves": []}), 500


@app.route("/api/neuron/search")
def neuron_search():
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return jsonify({"error": "No keyword"}), 400
    try:
        from agents.neuron import NeuronAgent
        n = NeuronAgent()
        return jsonify(n.search(keyword))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/neuron/fetch", methods=["POST"])
def neuron_fetch():
    """Trigger a manual NEURON knowledge refresh."""
    try:
        from agents.neuron import NeuronAgent
        n = NeuronAgent()
        stats = n.fetch_latest(limit_cves=20)
        return jsonify({"ok": True, "stats": stats})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
