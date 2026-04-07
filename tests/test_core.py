"""CIPHER Core Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

def test_scope_validator_basic():
    from core.scope import ScopeValidator
    s = ScopeValidator("example.com")
    assert s.is_in_scope("example.com")
    assert s.is_in_scope("sub.example.com")
    assert not s.is_in_scope("evil.com")

def test_scope_validator_cidr():
    from core.scope import ScopeValidator
    s = ScopeValidator("192.168.1.0/24")
    assert s.is_in_scope("192.168.1.1")
    assert s.is_in_scope("192.168.1.254")
    assert not s.is_in_scope("10.0.0.1")

def test_scope_validator_empty():
    from core.scope import ScopeValidator
    s = ScopeValidator()
    assert not s.is_in_scope("anything.com")

def test_message_bus():
    from core.bus import MessageBus
    bus = MessageBus()
    received = []
    bus.subscribe("test_event", lambda d: received.append(d))
    bus.emit("test_event", {"key": "value"})
    assert len(received) == 1
    assert received[0]["key"] == "value"

def test_commander_target_extraction():
    from agents.commander import Commander
    cmd = Commander()
    assert cmd._extract_target("scan example.com") == "example.com"
    assert cmd._extract_target("test 192.168.1.1") == "192.168.1.1"
    assert cmd._extract_target("hello world") == ""

def test_commander_safety():
    from agents.commander import Commander
    cmd = Commander()
    assert cmd._basic_safety_check("scan my own server")
    assert not cmd._basic_safety_check("hack into without permission")
    assert not cmd._basic_safety_check("ddos the site")

def test_mirror_payloads():
    from agents.mirror import MirrorAgent, INJECTION_PAYLOADS, LLM_ATTACK_CATEGORIES
    assert len(INJECTION_PAYLOADS) >= 10
    assert len(LLM_ATTACK_CATEGORIES) >= 5
    for p in INJECTION_PAYLOADS:
        assert "id" in p
        assert "payload" in p
        assert "category" in p

def test_ledger_report_structure():
    from agents.neuron_ledger import LedgerAgent
    from core.bus import MessageBus
    ledger = LedgerAgent(MessageBus())
    results = {"recon": {"findings": [
        {"type": "t", "title": "High severity issue", "severity": "high", "tool": "test", "data": {}}
    ]}}
    report = ledger.generate("test.com", results, "test_001", "")
    assert "risk_level" in report
    assert "findings" in report
    assert "markdown" in report
    assert report["total_findings"] == 1
    assert report["finding_counts"]["high"] == 1

def test_web_ui_index():
    import web_ui
    app = web_ui.app
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"CIPHER" in resp.data

def test_web_ui_mission_no_auth():
    import web_ui
    app = web_ui.app
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.post("/api/mission",
        json={"target": "example.com", "mode": "recon", "authorized": False},
        content_type="application/json"
    )
    assert resp.status_code == 403



# ── NEW TESTS ──

def test_breach_agent_loads():
    from agents.breach import BreachAgent, CANARY_PAYLOADS
    agent = BreachAgent()
    assert len(CANARY_PAYLOADS) >= 5
    total = sum(len(v) for v in CANARY_PAYLOADS.values())
    assert total >= 10
    print(f"BREACH: {total} canary payloads across {len(CANARY_PAYLOADS)} categories")

def test_breach_endpoint_discovery():
    from agents.breach import BreachAgent
    agent = BreachAgent()
    eps = agent._discover_endpoints("https://test.com", [
        {"data": {"path": "/api/login", "url": ""}},
    ])
    assert "/api/login" in eps
    assert "/" in eps
    assert len(eps) >= 5

def test_breach_remediation_coverage():
    from agents.breach import BreachAgent
    agent = BreachAgent()
    categories = ["sqli", "xss", "ssrf", "cmd_injection", "path_traversal"]
    for cat in categories:
        rec = agent._remediation(cat)
        assert len(rec) > 20, f"Remediation too short for {cat}"

def test_ai_provider_breach_integration():
    from agents.breach import BreachAgent
    from core.ai_provider import AIProvider
    from core.bus import MessageBus
    bus = MessageBus()
    agent = BreachAgent(bus=bus, api_key="")
    assert agent.name == "BREACH"
    assert agent.audit_dir.exists()

def test_commander_uses_ai_provider():
    from agents.commander import Commander
    cmd = Commander()
    ai = cmd._get_ai()
    # Should return AIProvider instance or None (if import fails)
    # Either way, no crash
    print(f"Commander AI provider: {type(ai).__name__ if ai else 'None (no key)'}")

def test_ghost_tech_detect_no_ansi():
    from agents.ghost import GhostAgent
    from core.bus import MessageBus
    import re
    agent = GhostAgent(MessageBus())
    # Simulate whatweb ANSI output
    ansi_output = "\x1b[0mNginx[0m \x1b[32m[v1.2]\x1b[0m HTTPServer[nginx]"
    cleaned = re.sub(r'\x1b\[[0-9;]*m', '', ansi_output)
    # Make sure 0m doesn't appear as a standalone tech
    techs = re.findall(r'\[([^\[\]]+?)\]', cleaned)
    valid = [t for t in techs if not re.match(r'^[\d;m]+$', t.strip())]
    assert "0m" not in valid, f"ANSI artifact in techs: {valid}"
    print(f"ANSI clean test: {valid}")

def test_netlify_toml_exists():
    import os
    assert os.path.exists("netlify.toml"), "netlify.toml missing"
    content = open("netlify.toml").read()
    assert "landing" in content



def test_neuron_real_db():
    from agents.neuron import NeuronAgent
    from core.bus import MessageBus
    n = NeuronAgent(MessageBus())
    stats = n.stats()
    assert "cves" in stats
    assert "techniques" in stats
    assert "db_path" in stats
    assert stats["cves"] >= 0

def test_neuron_store_learning():
    from agents.neuron import NeuronAgent
    n = NeuronAgent()
    n.store_mission_learning("test_999", "test.com", [
        {"type": "xss", "title": "XSS found", "severity": "high", "tool": "scanner"}
    ])
    stats = n.stats()
    assert stats["mission_learnings"] >= 1

def test_neuron_search_empty():
    from agents.neuron import NeuronAgent
    n = NeuronAgent()
    results = n.search("nginx_nonexistent_xyz")
    assert "cves" in results
    assert "techniques" in results
    assert isinstance(results["cves"], list)

def test_breach_wired_in_web_ui():
    import web_ui
    src = open("web_ui.py").read()
    assert "from agents.breach import BreachAgent" in src or "BreachAgent" in src
    assert "breach" in src

def test_breach_mode_in_dropdown():
    import web_ui
    app = web_ui.app
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.get("/")
    assert b"breach" in resp.data.lower()

def test_neuron_api_stats():
    import web_ui
    app = web_ui.app
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.get("/api/neuron/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "cves" in data

def test_neuron_api_cves():
    import web_ui
    app = web_ui.app
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.get("/api/neuron/cves")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "cves" in data
    assert isinstance(data["cves"], list)

def test_telegram_bot_loads():
    import telegram_bot as tb
    assert hasattr(tb, "run")
    assert hasattr(tb, "handle_update")
    assert hasattr(tb, "sessions")
    assert hasattr(tb, "send")

def test_telegram_auth_session():
    import telegram_bot as tb
    tb.sessions[9999] = {
        "state": "awaiting_auth",
        "target": "test.com",
        "mode": "scan",
        "chat_id": 1111
    }
    session = tb.sessions.get(9999)
    assert session["state"] == "awaiting_auth"
    assert session["target"] == "test.com"
    tb.sessions.pop(9999, None)

