"""
tools/catalog.py
================
Prompt templates and AI bio generation logic.

This module contains:
  - PLATFORM_GUIDANCE  : Per-platform tone instructions injected into prompts
  - BIO_SYSTEM_PROMPT  : The system prompt used for all AI calls
  - build_prompt()     : Assembles the final user prompt for a given bio length
  - BioGenerator       : Orchestrates OpenAI / Gemini calls to produce all 3 bios
"""

from __future__ import annotations

from typing import Optional

from config import Config


# ─────────────────────────────────────────────
# Platform-Specific Tone Guidance
# ─────────────────────────────────────────────

PLATFORM_GUIDANCE: dict[str, str] = {
    "website": (
        "This bio is for a professional website's About page. "
        "Use a warm yet authoritative third-person voice. "
        "Lead with impact, establish credibility, and end with a personal touch. "
        "Avoid jargon; aim for clear, engaging prose."
    ),
    "linkedin": (
        "This bio is for a LinkedIn profile summary (About section). "
        "Write in the first person. Open with a compelling hook about the person's "
        "passion or key value proposition. Use conversational but professional language. "
        "Highlight achievements and invite connection or collaboration."
    ),
    "speaker": (
        "This bio is for a conference or event speaker profile. "
        "Use third person. Lead with the most impressive credential or biggest claim to fame. "
        "Emphasise speaking topics, thought-leadership, and audience impact. "
        "Keep it energetic and use active, vivid language."
    ),
}

# ─────────────────────────────────────────────
# System Prompt
# ─────────────────────────────────────────────

BIO_SYSTEM_PROMPT = """You are an expert professional copywriter specialising in writing compelling, 
authentic personal bios for professionals across all industries.

Your writing:
- Is tailored precisely to the platform and audience
- Balances credibility with personality
- Avoids clichés ("passionate", "results-driven", "synergy", etc.)
- Uses specific, concrete language
- Matches the requested word count closely (within ±10%)

You always respond with ONLY the bio text. No preamble, no labels, no markdown formatting.
"""

# ─────────────────────────────────────────────
# Bio Length Specifications
# ─────────────────────────────────────────────

BIO_LENGTHS: dict[str, dict] = {
    "short": {
        "label":    "Short Bio",
        "words":    50,
        "guidance": (
            "Write a punchy, memorable bio in approximately 50 words. "
            "Cover: who they are, what they do, and one standout achievement or value. "
            "Every word must earn its place."
        ),
    },
    "medium": {
        "label":    "Medium Bio",
        "words":    150,
        "guidance": (
            "Write a well-rounded bio in approximately 150 words. "
            "Include: professional identity, key experience, notable achievements, "
            "and a closing sentence about current focus or mission."
        ),
    },
    "long": {
        "label":    "Long Bio",
        "words":    300,
        "guidance": (
            "Write a comprehensive bio in approximately 300 words. "
            "Cover: professional background and journey, specific accomplishments "
            "(with numbers/outcomes where plausible), areas of expertise, "
            "thought-leadership or unique perspective, and a human/personal closing."
        ),
    },
}


# ─────────────────────────────────────────────
# Prompt Builder
# ─────────────────────────────────────────────

def build_prompt(
    name: str,
    role: str,
    industry: str,
    experience: str,
    platform: str,
    length_key: str,
    tone_context: str = "",
) -> str:
    """
    Assemble the user-turn prompt for a specific bio length.

    Args:
        name:         Full name of the person.
        role:         Professional title/role.
        industry:     Industry or domain.
        experience:   Short experience summary provided by the user.
        platform:     One of 'website', 'linkedin', 'speaker'.
        length_key:   One of 'short', 'medium', 'long'.
        tone_context: Optional web-research context from Tavily.

    Returns:
        The complete prompt string to send to the AI model.
    """
    spec      = BIO_LENGTHS[length_key]
    tone_note = PLATFORM_GUIDANCE.get(platform, PLATFORM_GUIDANCE["website"])

    # Build the prompt section by section
    sections = [
        f"Write a professional bio for the following person.\n",
        "=== PERSON DETAILS ===",
        f"Name:        {name}",
        f"Role/Title:  {role}",
        f"Industry:    {industry}",
        f"Experience:  {experience}",
        "",
        "=== PLATFORM ===",
        tone_note,
        "",
        "=== BIO REQUIREMENTS ===",
        spec["guidance"],
        f"Target word count: ~{spec['words']} words.",
    ]

    # Inject tone research if available
    if tone_context.strip():
        sections += [
            "",
            "=== ADDITIONAL CONTEXT (from web research) ===",
            tone_context,
            "Use the above to calibrate tone and style where relevant.",
        ]

    sections += [
        "",
        "Write ONLY the bio text. No titles, labels, or extra commentary.",
    ]

    return "\n".join(sections)


# ─────────────────────────────────────────────
# Bio Generator
# ─────────────────────────────────────────────

class BioGenerator:
    """
    Uses the configured AI provider (OpenAI or Gemini) to generate
    short, medium, and long professional bios.

    Usage:
        gen  = BioGenerator(config=config)
        bios = gen.generate_all(name=..., role=..., industry=..., ...)
    """

    def __init__(self, config: Config):
        self._config   = config
        self._provider = config.active_provider

        if self._provider == "openai":
            self._client = self._init_openai()
        else:
            self._client = self._init_gemini()

    # ── Initialisation ──────────────────────────────────────────────────

    def _init_openai(self):
        """Initialise and return an OpenAI client."""
        try:
            from openai import OpenAI  # type: ignore
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        return OpenAI(api_key=self._config.openai_api_key)

    def _init_gemini(self):
        """Initialise and return a Gemini GenerativeModel client."""
        try:
            import google.generativeai as genai  # type: ignore
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )
        genai.configure(api_key=self._config.gemini_api_key)
        return genai.GenerativeModel(
            model_name=self._config.gemini_model,
            system_instruction=BIO_SYSTEM_PROMPT,
        )

    # ── Public API ──────────────────────────────────────────────────────

    def generate_all(
        self,
        name: str,
        role: str,
        industry: str,
        experience: str,
        platform: str = "website",
        tone_context: str = "",
    ) -> dict[str, str]:
        """
        Generate short, medium, and long bios.

        Returns:
            dict with keys 'short', 'medium', 'long' mapping to bio strings.
        """
        bios: dict[str, str] = {}

        for length_key in ("short", "medium", "long"):
            label  = BIO_LENGTHS[length_key]["label"]
            words  = BIO_LENGTHS[length_key]["words"]
            print(f"  ⏳ Generating {label} (~{words} words)…", end=" ", flush=True)

            prompt = build_prompt(
                name=name,
                role=role,
                industry=industry,
                experience=experience,
                platform=platform,
                length_key=length_key,
                tone_context=tone_context,
            )

            bio = self._call_ai(prompt)
            bios[length_key] = bio.strip()
            print("✅")

        return bios

    # ── AI Call Routing ─────────────────────────────────────────────────

    def _call_ai(self, prompt: str) -> str:
        """Route the prompt to the active AI provider and return the response text."""
        if self._provider == "openai":
            return self._call_openai(prompt)
        return self._call_gemini(prompt)

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI Chat Completions and return the message content."""
        response = self._client.chat.completions.create(
            model=self._config.openai_model,
            temperature=self._config.temperature,
            messages=[
                {"role": "system", "content": BIO_SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
        )
        return response.choices[0].message.content or ""

    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini GenerateContent and return the response text."""
        import google.generativeai as genai  # type: ignore

        generation_config = genai.GenerationConfig(
            temperature=self._config.temperature,
            max_output_tokens=1024,
        )
        response = self._client.generate_content(
            prompt,
            generation_config=generation_config,
        )
        return response.text or ""
