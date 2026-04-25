"""
tools/search.py
===============
Tavily API integration for researching industry-specific tone and style norms.

If a Tavily API key is provided, this module fetches real-world writing style
references (e.g., how bios are typically written for a given industry/platform)
and returns a condensed context string that is injected into the AI prompts.
"""

from __future__ import annotations

import textwrap
from typing import Optional

# Guard import – tavily-python is optional
try:
    from tavily import TavilyClient  # type: ignore
    _TAVILY_AVAILABLE = True
except ImportError:
    _TAVILY_AVAILABLE = False


# ─────────────────────────────────────────────
# Query Templates
# ─────────────────────────────────────────────

TONE_QUERIES = {
    "website": (
        "professional bio writing style examples for {industry} industry website about page"
    ),
    "linkedin": (
        "LinkedIn summary writing tips {industry} professionals tone and style 2024"
    ),
    "speaker": (
        "speaker bio writing best practices {industry} conference professional tone"
    ),
}


# ─────────────────────────────────────────────
# TavilySearchTool
# ─────────────────────────────────────────────

class TavilySearchTool:
    """
    Wraps the Tavily search API to fetch tone/style context.

    Usage:
        tool = TavilySearchTool(api_key="tvly-xxx")
        context = tool.research_tone(industry="Finance", platform="linkedin")
    """

    def __init__(self, api_key: str):
        if not _TAVILY_AVAILABLE:
            raise ImportError(
                "tavily-python is not installed. Run: pip install tavily-python"
            )
        if not api_key:
            raise ValueError("Tavily API key must not be empty.")

        self._client = TavilyClient(api_key=api_key)

    # ── Public API ──────────────────────────────────────────────────────

    def research_tone(
        self,
        industry: str,
        platform: str = "website",
        max_results: int = 3,
    ) -> str:
        """
        Search for tone/style norms for the given industry and platform.

        Args:
            industry:    The professional industry (e.g., "Tech", "Finance").
            platform:    One of 'website', 'linkedin', 'speaker'.
            max_results: Number of search results to fetch.

        Returns:
            A condensed string of tone guidance extracted from search results,
            or an empty string if nothing useful was found.
        """
        query_template = TONE_QUERIES.get(platform, TONE_QUERIES["website"])
        query = query_template.format(industry=industry)

        try:
            response = self._client.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
                include_answer=True,        # Ask Tavily for a synthesised answer
                include_raw_content=False,
            )
        except Exception as exc:
            print(f"  ⚠️  Tavily search error: {exc}")
            return ""

        return self._extract_context(response)

    # ── Private Helpers ─────────────────────────────────────────────────

    def _extract_context(self, response: dict) -> str:
        """
        Extract and condense useful tone guidance from the Tavily response.

        Prefers the synthesised 'answer' field; falls back to snippet snippets.
        """
        parts: list[str] = []

        # 1. Use the synthesised answer if available
        answer = response.get("answer", "").strip()
        if answer:
            parts.append(f"Web research summary:\n{self._truncate(answer, 400)}")

        # 2. Append snippets from individual results
        results = response.get("results", [])
        for result in results[:2]:            # limit to first 2 for brevity
            content = result.get("content", "").strip()
            title   = result.get("title",   "").strip()
            if content:
                snippet = self._truncate(content, 200)
                parts.append(f"Source – {title}:\n{snippet}")

        if not parts:
            return ""

        context = "\n\n".join(parts)
        return (
            "─── Tone Research (from web) ───\n"
            + context
            + "\n─────────────────────────────────"
        )

    @staticmethod
    def _truncate(text: str, max_chars: int) -> str:
        """Truncate text to max_chars and append ellipsis if needed."""
        text = " ".join(text.split())         # normalise whitespace
        if len(text) <= max_chars:
            return text
        return textwrap.shorten(text, width=max_chars, placeholder=" …")
