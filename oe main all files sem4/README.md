# ✍️ Professional Bio Writer

A Python CLI application that generates **short, medium, and long professional bios** powered by OpenAI or Google Gemini — with optional real-time tone research via Tavily.

---

## 🗂 Project Structure

```
project/
├── app.py                  # Main entry point (CLI + orchestration)
├── config.py               # API key & settings loader
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .env.example            # Template for environment variables
│
├── tools/
│   ├── __init__.py
│   ├── search.py           # Tavily web-research integration
│   └── catalog.py          # Prompt templates + AI bio generation
│
├── data/                   # Reserved for future use (e.g., industry presets)
│
└── outputs/
    └── .gitkeep            # Generated bios are saved here
```

---

## ⚙️ Setup

### 1. Clone / download the project

```bash
git clone https://github.com/your-username/bio-writer.git
cd bio-writer
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you only have one AI provider key, you may skip installing the other SDK.
> Tavily is also optional.

### 4. Configure API keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
OPENAI_API_KEY=sk-...          # Required (OR use Gemini below)
# GEMINI_API_KEY=AIza...       # Alternative to OpenAI
TAVILY_API_KEY=tvly-...        # Optional – enables tone research
```

---

## 🚀 How to Run

### Interactive Mode (recommended for first use)

```bash
python app.py
```

The app will prompt you for:
- Full name
- Professional role/title
- Industry / domain
- Experience summary
- Bio format (website / linkedin / speaker)

---

### CLI Flag Mode (for scripting / automation)

```bash
python app.py \
  --name "Jane Doe" \
  --role "Chief Product Officer" \
  --industry "FinTech" \
  --experience "15 years building financial products used by 10M+ consumers across 3 continents" \
  --format linkedin
```

#### All Available Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--name` | Full name | *(prompted)* |
| `--role` | Job title / role | *(prompted)* |
| `--industry` | Industry or domain | *(prompted)* |
| `--experience` | Experience summary | *(prompted)* |
| `--format` | `website` / `linkedin` / `speaker` | `website` |
| `--output-dir` | Directory to save bios | `outputs/` |
| `--no-search` | Skip Tavily web research | `False` |

---

## 📤 Output

Bios are saved to `outputs/{first_last}_bio.txt`:

```
============================================================
  PROFESSIONAL BIO – JANE DOE
  Format: Linkedin
============================================================

── SHORT BIO (≈50 words) ──────────────────────────────────────────

Jane Doe is a FinTech executive with 15 years of experience…

── MEDIUM BIO (≈150 words) ────────────────────────────────────────

…

── LONG BIO (≈300 words) ──────────────────────────────────────────

…
```

---

## 🧪 Example Run

### Input

```
Full Name:         Arjun Mehta
Role/Title:        AI Research Engineer
Industry:          Artificial Intelligence
Experience:        7 years building NLP systems at Google and two AI startups; 
                   published 4 papers on large language model alignment
Bio Format:        speaker
```

### Output (Short Bio – Speaker)

> Arjun Mehta is an AI Research Engineer with seven years at the forefront of natural language processing. A published researcher on large language model alignment, he has shipped NLP systems at Google and led AI teams at two high-growth startups. Arjun speaks on building AI that is both powerful and responsibly designed.

---

## 🌐 Tavily Web Research

When `TAVILY_API_KEY` is set, the app automatically:
1. Searches for tone and style norms for your industry + platform.
2. Injects that context into the AI prompt.
3. Produces bios that better match how professionals in your field actually write.

To skip this even with a key configured:

```bash
python app.py --no-search
```

---

## 🤖 AI Providers

| Provider | Env Variable | Recommended Model |
|----------|-------------|-------------------|
| OpenAI   | `OPENAI_API_KEY` | `gpt-4o-mini` (default) |
| Google Gemini | `GEMINI_API_KEY` | `gemini-1.5-flash` (default) |

If both keys are set, **OpenAI takes precedence**. You can override models via `.env`:

```env
OPENAI_MODEL=gpt-4o
GEMINI_MODEL=gemini-1.5-pro
```

---

## 🔐 Security Notes

- Never commit your `.env` file. It is already in `.gitignore` (add it if needed).
- `.env.example` is safe to commit — it contains no real keys.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `python-dotenv` | Load `.env` variables |
| `openai` | OpenAI GPT API client |
| `google-generativeai` | Google Gemini API client |
| `tavily-python` | Web search for tone research |

---

## 🛠 Troubleshooting

**`No AI API key found`**
→ Open `.env` and ensure `OPENAI_API_KEY` or `GEMINI_API_KEY` is set correctly.

**`openai` not found / `google-generativeai` not found**
→ Run `pip install -r requirements.txt` inside your virtual environment.

**Tavily returns no results**
→ Check `TAVILY_API_KEY` in `.env`. The app continues without it gracefully.

**Output looks truncated**
→ Try setting `OPENAI_MODEL=gpt-4o` in `.env` for higher-quality, longer responses.

---

## 📄 License

MIT — free to use, modify, and distribute.
