"""
config.py
=========
Centralised configuration loader for the Professional Bio Writer.
Reads API keys and settings from environment variables (populated via .env).
"""

import os
from dataclasses import dataclass, field
from typing import Literal


# Supported AI provider types
AIProvider = Literal["openai", "gemini"]


@dataclass
class Config:
    """
    Application configuration.
    All values are read from environment variables at instantiation time.
    """

    # ── AI Provider ────────────────────────────────────────────────────
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))

    # ── Tavily (optional web research) ─────────────────────────────────
    tavily_api_key: str = field(default_factory=lambda: os.getenv("TAVILY_API_KEY", ""))

    # ── Model names (can be overridden via env) ─────────────────────────
    openai_model: str = field(
        default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    gemini_model: str = field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    )

    # ── Generation settings ─────────────────────────────────────────────
    temperature: float = field(
        default_factory=lambda: float(os.getenv("TEMPERATURE", "0.75"))
    )

    def is_ai_configured(self) -> bool:
        """Return True if at least one AI provider key is available."""
        return bool(self.openai_api_key or self.gemini_api_key)

    @property
    def active_provider(self) -> AIProvider:
        """
        Return the provider to use.
        OpenAI takes precedence if both keys are present.
        """
        if self.openai_api_key:
            return "openai"
        if self.gemini_api_key:
            return "gemini"
        raise EnvironmentError(
            "No AI API key configured. Set OPENAI_API_KEY or GEMINI_API_KEY in .env"
        )

    @property
    def active_model(self) -> str:
        """Return the model name for the active provider."""
        if self.active_provider == "openai":
            return self.openai_model
        return self.gemini_model

    def __repr__(self) -> str:
        provider = self.active_provider if self.is_ai_configured() else "none"
        tavily   = "yes" if self.tavily_api_key else "no"
        return (
            f"Config(provider={provider!r}, model={self.active_model!r}, "
            f"tavily={tavily})"
        )
