# 🚀 RUNNING.md — How to Run EquityLens AI Locally

This guide covers everything you need to go from zero to a running application.

---

## Prerequisites

| Requirement | Version | How to Check |
|---|---|---|
| Python | 3.10+ | `python --version` |
| pip | 23+ | `pip --version` |
| OpenAI API key | — | [platform.openai.com](https://platform.openai.com/api-keys) |

> **Anaconda/Conda users:** All commands work in a conda environment. Activate your env first.

---

## Step 1 — Clone / Open the Project

If you haven't already:
```bash
git clone https://github.com/YOUR_USERNAME/equity-research-llm.git
cd equity-research-llm
```

Or if working from a downloaded zip, just `cd` into the project folder:
```bash
cd path/to/Equity-Research-LLM-main
```

---

## Step 2 — Set Up a Virtual Environment (Recommended)

```bash
# Create venv
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate
```

> Skip this if using Anaconda/conda — your base env is fine.

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output: packages download and install without errors.  
⚠️ If you see errors about `libmagic` on Windows, that's okay — `unstructured` will fall back to basic extraction.

---

## Step 4 — Configure Your API Key

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Mac/Linux
cp .env.example .env
```

Now open `.env` and replace the placeholder:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

> **Where to get a key:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## Step 5 — Run the App

```bash
streamlit run app.py
```

The terminal will show:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open **http://localhost:8501** in your browser. ✅

---

## Step 6 — Using the App

1. **Paste URLs** — Add 1–5 financial news article URLs in the sidebar
2. **Click "Process & Build Index"** — Wait ~20–60 seconds for indexing
3. **Ask a question** — Type any research question and click "Analyse"
4. **View results** — See the AI answer, confidence score, and source citations
5. **Export** — Download your report as PDF or TXT
6. **History** — Click the "History" tab to review all past sessions

---

## Troubleshooting

### ❌ `ModuleNotFoundError`
```bash
# Make sure you're in the right folder and dependencies are installed
pip install -r requirements.txt
```

### ❌ `OPENAI_API_KEY is not set`
- Check that `.env` exists (not `.env.example`)
- Verify the key starts with `sk-`
- Restart the app after editing `.env`

### ❌ `No content could be extracted from URLs`
- The URL must be publicly accessible (no paywall)
- Try a different news source (Reuters, Bloomberg, CNBC, etc.)
- Some sites block automated scrapers — try a different article

### ❌ `faiss-cpu` install error
```bash
pip install faiss-cpu --no-cache-dir
```

### ❌ `libmagic` warning on Windows
This is non-fatal. The app will use fallback text extraction. If you want full magic support:
```bash
pip install python-magic-bin
```

---

## Docker (Alternative)

```bash
# Build and run
docker compose up --build

# Visit http://localhost:8501
```

Make sure your `.env` file exists before running Docker.

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | — | Your OpenAI secret key |
| `LLM_MODEL` | No | `gpt-3.5-turbo-instruct` | LLM model name |

---

## File Locations After Running

| Path | Contents |
|---|---|
| `data/vector_store/faiss_index.pkl` | Built FAISS index (regenerated each time you process URLs) |
| `data/history/research_history.json` | All past Q&A sessions |

---

*Having issues? Open a GitHub issue or check the README for more context.*
