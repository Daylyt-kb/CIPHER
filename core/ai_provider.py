"""
CIPHER Universal AI Provider
Supports ALL of these — switch anytime, no code changes:

  CLOUD (API key required):
  - Anthropic Claude    — claude-sonnet-4, claude-haiku
  - Google Gemini       — gemini-1.5-flash (FREE tier available)
  - OpenAI GPT          — gpt-4o, gpt-4o-mini
  - Groq                — llama-3.3-70b (FREE, fastest)
  - Mistral AI          — mistral-large, mistral-small

  LOCAL (zero cost, zero API key, data never leaves your machine):
  - Ollama              — llama3.2, mistral, codellama, deepseek-r1, phi3
  - LM Studio           — any GGUF model
  - Jan                 — any local model
  - Any OpenAI-compatible server (set OPENAI_BASE_URL)

For local models: no key needed, no usage costs, full privacy.
"""

import os
import json
import urllib.request
import urllib.error


PROVIDERS = {
    # ── LOCAL (no key, no cost, private) ──────────────────────────────────────
    "ollama": {
        "name": "Ollama (Local · Free · Private)",
        "models": [
            "llama3.2", "llama3.1", "llama3",
            "mistral", "mistral-nemo",
            "codellama", "deepseek-r1",
            "phi3", "phi3.5",
            "gemma2", "gemma2:2b",
            "qwen2.5", "qwen2.5-coder",
            "dolphin-mixtral", "neural-chat",
        ],
        "default_model": "llama3.2",
        "env_key": "OLLAMA_MODEL",
        "key_prefix": "",
        "docs": "https://ollama.com",
        "free_tier": True,
        "local": True,
        "base_url": "http://localhost:11434",
        "setup": "Install: curl -fsSL https://ollama.com/install.sh | sh\nPull model: ollama pull llama3.2\nStart: ollama serve",
        "note": "No API key needed. Completely private.",
    },
    "lmstudio": {
        "name": "LM Studio (Local · Free · Private)",
        "models": ["local-model"],
        "default_model": "local-model",
        "env_key": "LMSTUDIO_MODEL",
        "key_prefix": "",
        "docs": "https://lmstudio.ai",
        "free_tier": True,
        "local": True,
        "base_url": "http://localhost:1234",
        "setup": "1. Download LM Studio at lmstudio.ai\n2. Download any model\n3. Start Local Server tab",
        "note": "Compatible with any GGUF model.",
    },

    # ── CLOUD FREE TIER ───────────────────────────────────────────────────────
    "groq": {
        "name": "Groq (Cloud · Free · Fastest)",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
        "default_model": "llama-3.3-70b-versatile",
        "env_key": "GROQ_API_KEY",
        "key_prefix": "gsk_",
        "docs": "https://console.groq.com",
        "free_tier": True,
        "local": False,
        "note": "Free API key at console.groq.com — fastest inference available.",
    },
    "gemini": {
        "name": "Google Gemini (Cloud · Free Tier)",
        "models": [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash",
        ],
        "default_model": "gemini-1.5-flash",
        "env_key": "GEMINI_API_KEY",
        "key_prefix": "AIzaSy",
        "docs": "https://aistudio.google.com",
        "free_tier": True,
        "local": False,
        "note": "Free API key at aistudio.google.com",
    },

    # ── CLOUD PAID ────────────────────────────────────────────────────────────
    "anthropic": {
        "name": "Anthropic Claude",
        "models": [
            "claude-sonnet-4-20250514",
            "claude-haiku-4-5-20251001",
            "claude-opus-4-6",
        ],
        "default_model": "claude-sonnet-4-20250514",
        "env_key": "ANTHROPIC_API_KEY",
        "key_prefix": "sk-ant-",
        "docs": "https://console.anthropic.com",
        "free_tier": False,
        "local": False,
    },
    "openai": {
        "name": "OpenAI GPT",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        "default_model": "gpt-4o-mini",
        "env_key": "OPENAI_API_KEY",
        "key_prefix": "sk-",
        "docs": "https://platform.openai.com",
        "free_tier": False,
        "local": False,
    },
    "mistral": {
        "name": "Mistral AI",
        "models": ["mistral-large-latest", "mistral-small-latest", "open-mistral-7b"],
        "default_model": "mistral-small-latest",
        "env_key": "MISTRAL_API_KEY",
        "key_prefix": "MIST",
        "docs": "https://console.mistral.ai",
        "free_tier": False,
        "local": False,
    },
}


class AIProvider:
    """
    Universal AI interface.
    Works with cloud APIs and local models (Ollama, LM Studio).
    Pass any API key and model — it routes automatically.
    For local models: pass provider='ollama' with no key.
    """

    def __init__(self, api_key: str = "", provider: str = "", model: str = ""):
        self.api_key = api_key or self._detect_from_env()
        self.provider = provider or self._detect_provider(self.api_key)
        self.model = model or self._default_model()

        # Auto-detect local providers if running
        if not self.provider:
            self.provider = self._detect_local_provider()
            self.model = self._default_model()

    # ── Public API ─────────────────────────────────────────────────────────────

    def complete(self, prompt: str, system: str = "", max_tokens: int = 1000) -> str:
        """Send a prompt, get a response. Works for all providers."""
        if self.provider == "ollama":
            return self._ollama(prompt, system, max_tokens)
        elif self.provider == "lmstudio":
            return self._lmstudio(prompt, system, max_tokens)
        elif not self.api_key:
            return self._no_key_fallback(prompt)

        try:
            if self.provider == "anthropic":
                return self._anthropic(prompt, system, max_tokens)
            elif self.provider == "gemini":
                return self._gemini(prompt, system, max_tokens)
            elif self.provider == "openai":
                return self._openai(prompt, system, max_tokens)
            elif self.provider == "groq":
                return self._groq(prompt, system, max_tokens)
            elif self.provider == "mistral":
                return self._mistral(prompt, system, max_tokens)
            else:
                return self._openai_compat(prompt, system, max_tokens)
        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "credit" in err.lower() or "billing" in err.lower():
                return f"[AI] API key has no credits. Get free credits at {PROVIDERS.get(self.provider, {}).get('docs', '')}"
            return f"[AI] Error ({self.provider}): {err[:200]}"

    def is_configured(self) -> bool:
        """Returns True if any provider is ready to use."""
        if self.provider in ("ollama", "lmstudio"):
            return True  # Local providers need no key
        return bool(self.api_key and self.provider)

    def is_local(self) -> bool:
        return PROVIDERS.get(self.provider, {}).get("local", False)

    def status(self) -> dict:
        info = PROVIDERS.get(self.provider, {})
        return {
            "configured": self.is_configured(),
            "provider": self.provider,
            "provider_name": info.get("name", "Unknown"),
            "model": self.model,
            "local": info.get("local", False),
            "free": info.get("free_tier", False),
            "key_preview": (
                "local — no key needed" if info.get("local")
                else f"{self.api_key[:8]}...{self.api_key[-4:]}" if self.api_key
                else "not set"
            ),
        }

    # ── Local providers ─────────────────────────────────────────────────────────

    def _ollama(self, prompt: str, system: str, max_tokens: int) -> str:
        """Call Ollama local API — completely private, zero cost."""
        base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body = json.dumps({
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"num_predict": max_tokens}
        }).encode()

        try:
            req = urllib.request.Request(
                f"{base}/api/chat",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            return data["message"]["content"]
        except urllib.error.URLError:
            return (
                "[Ollama] Not running. Start it with: ollama serve\n"
                f"Then pull a model: ollama pull {self.model}"
            )

    def _lmstudio(self, prompt: str, system: str, max_tokens: int) -> str:
        """Call LM Studio local server — OpenAI-compatible."""
        base = os.environ.get("LMSTUDIO_BASE_URL", "http://localhost:1234")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        try:
            return self._openai_compat_call(
                f"{base}/v1/chat/completions", messages, max_tokens, key="lm-studio"
            )
        except urllib.error.URLError:
            return "[LM Studio] Not running. Open LM Studio and start the local server."

    # ── Cloud providers ─────────────────────────────────────────────────────────

    def _anthropic(self, prompt: str, system: str, max_tokens: int) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system:
            kwargs["system"] = system
        r = client.messages.create(**kwargs)
        return r.content[0].text

    def _gemini(self, prompt: str, system: str, max_tokens: int) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        full = f"{system}\n\n{prompt}" if system else prompt
        r = genai.GenerativeModel(self.model).generate_content(
            full,
            generation_config=genai.GenerationConfig(max_output_tokens=max_tokens)
        )
        return r.text

    def _openai(self, prompt: str, system: str, max_tokens: int) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self._openai_compat_call(
            "https://api.openai.com/v1/chat/completions", messages, max_tokens
        )

    def _groq(self, prompt: str, system: str, max_tokens: int) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self._openai_compat_call(
            "https://api.groq.com/openai/v1/chat/completions", messages, max_tokens
        )

    def _mistral(self, prompt: str, system: str, max_tokens: int) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self._openai_compat_call(
            "https://api.mistral.ai/v1/chat/completions", messages, max_tokens
        )

    def _openai_compat(self, prompt: str, system: str, max_tokens: int) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        return self._openai_compat_call(
            f"{base}/chat/completions", messages, max_tokens
        )

    def _openai_compat_call(self, url: str, messages: list,
                             max_tokens: int, key: str = "") -> str:
        body = json.dumps({
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }).encode()
        req = urllib.request.Request(
            url, data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key or self.api_key}",
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]

    # ── Detection logic ──────────────────────────────────────────────────────────

    def _detect_from_env(self) -> str:
        for provider, info in PROVIDERS.items():
            if info.get("local"):
                continue
            key = os.environ.get(info["env_key"], "")
            if key:
                return key
        return ""

    def _detect_provider(self, key: str) -> str:
        if not key:
            return ""
        for provider, info in PROVIDERS.items():
            prefix = info.get("key_prefix", "")
            if prefix and key.startswith(prefix):
                return provider
        for provider, info in PROVIDERS.items():
            env_key = os.environ.get(info.get("env_key", ""), "")
            if env_key and env_key == key:
                return provider
        return "openai"

    def _detect_local_provider(self) -> str:
        """Check if Ollama or LM Studio is running locally."""
        for provider, base_url in [
            ("ollama", "http://localhost:11434"),
            ("lmstudio", "http://localhost:1234"),
        ]:
            try:
                req = urllib.request.Request(
                    f"{base_url}/api/tags" if provider == "ollama" else f"{base_url}/v1/models",
                    headers={"User-Agent": "CIPHER/1.0"}
                )
                with urllib.request.urlopen(req, timeout=1):
                    return provider
            except Exception:
                pass
        return ""

    def _default_model(self) -> str:
        # Check for env-specified model override
        if self.provider == "ollama":
            return os.environ.get("OLLAMA_MODEL", "llama3.2")
        if self.provider == "lmstudio":
            return os.environ.get("LMSTUDIO_MODEL", "local-model")
        return PROVIDERS.get(self.provider, {}).get("default_model", "llama3.2")

    def _no_key_fallback(self, prompt: str) -> str:
        return (
            "[AI Brain: Offline]\n"
            "No AI provider configured. Options:\n\n"
            "FREE LOCAL (no key, private):\n"
            "  ollama serve && ollama pull llama3.2\n"
            "  Then: export CIPHER_PROVIDER=ollama\n\n"
            "FREE CLOUD:\n"
            "  Groq: console.groq.com → set GROQ_API_KEY\n"
            "  Gemini: aistudio.google.com → set GEMINI_API_KEY\n\n"
            "Add key in Settings tab of the web UI."
        )

    @staticmethod
    def detect_from_key(key: str) -> str:
        key = key.strip()
        if key.lower() in ("ollama", "local"):
            return "ollama"
        for provider, info in PROVIDERS.items():
            prefix = info.get("key_prefix", "")
            if prefix and key.startswith(prefix):
                return provider
        return "openai"

    @staticmethod
    def all_providers() -> dict:
        return PROVIDERS
