<div align="center">

# 📊 EquityLens AI

### RAG-Powered Equity Research Intelligence

*Analyse financial news with AI. Get cited, grounded answers in seconds.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=flat-square)](https://python.langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-00b4d8?style=flat-square)](https://faiss.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[**Live Demo**](#-quick-start) · [**Architecture**](#-architecture) · [**Features**](#-features) · [**Deploy**](#-deployment)

</div>

---

## What is EquityLens AI?

EquityLens AI is a **Retrieval-Augmented Generation (RAG)** application that turns raw financial news URLs into institutional-quality research answers — complete with source citations, confidence scores, and downloadable PDF reports.

Paste any news article links → ask research questions → get AI-synthesised answers grounded in the actual article text, not hallucinated from training data.

**Works with xAI Grok or OpenAI.** Uses free local embeddings (no embedding API costs).

---

## Features

| | Feature | Description |
|---|---|---|
| 🔍 | **RAG Pipeline** | URL → chunk → embed → FAISS → retrieve → LLM synthesise |
| 📎 | **Source Citations** | Every answer cites the exact article sections used |
| 📊 | **Confidence Scores** | Visual score (0–100%) showing answer reliability |
| 📚 | **Research History** | All sessions saved locally with searchable timeline |
| 📄 | **PDF Export** | Download branded research reports (ReportLab) |
| 🎨 | **Dark Mode UI** | Glassmorphism design with animated gradients |
| ⚡ | **Grok + OpenAI** | Works with xAI Grok or OpenAI via same codebase |
| 🆓 | **Free Embeddings** | Local HuggingFace model — no embedding API costs |
| 🐳 | **Dockerized** | One-command deploy with Docker Compose |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EquityLens AI v2.1                          │
│                    RAG Architecture Overview                         │
└─────────────────────────────────────────────────────────────────────┘

  INPUT
  ─────
  User pastes 1–5 financial news article URLs
        │
        ▼
  ┌─────────────────────┐
  │  UnstructuredURL    │  ← Web scraping & HTML extraction
  │      Loader         │
  └────────┬────────────┘
           │ raw documents
           ▼
  ┌─────────────────────┐
  │ RecursiveCharacter  │  ← 1000-token chunks, 200-token overlap
  │   TextSplitter      │    Semantic boundary-aware splitting
  └────────┬────────────┘
           │ text chunks
           ▼
  ┌─────────────────────┐
  │  HuggingFace        │  ← all-MiniLM-L6-v2 (runs locally, free)
  │  Embeddings         │    384-dim dense vectors
  └────────┬────────────┘
           │ embedding vectors
           ▼
  ┌─────────────────────┐
  │   FAISS Index       │  ← Local vector database
  │  (persisted .pkl)   │    Cosine similarity search
  └─────────────────────┘

  QUERY
  ─────
  User asks a research question
        │
        ▼
  ┌─────────────────────┐
  │  FAISS Retriever    │  ← Top-4 most relevant chunks
  │    (k=4 docs)       │
  └────────┬────────────┘
           │ relevant context
           ▼
  ┌─────────────────────┐
  │ RetrievalQA Chain   │  ← LangChain orchestration
  │  (with Sources)     │    Forces source citation in prompt
  └────────┬────────────┘
           │ prompt + context
           ▼
  ┌─────────────────────┐
  │  xAI Grok / OpenAI  │  ← OpenAI-compatible API
  │       LLM           │    grok-3-fast-beta or gpt-3.5-turbo
  └────────┬────────────┘
           │ answer + sources
           ▼
  OUTPUT: Answer + Citations + Confidence Score + PDF Report
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **UI** | Streamlit 1.37 + custom CSS | Interactive web interface |
| **LLM** | xAI Grok / OpenAI GPT | Answer generation |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` | Free local semantic vectors |
| **Vector DB** | FAISS (CPU) | Millisecond similarity search |
| **Orchestration** | LangChain 0.2 | Chain management & retrieval |
| **Web Scraping** | UnstructuredURLLoader | Article content extraction |
| **PDF Export** | ReportLab | Downloadable research reports |
| **Config** | python-dotenv | Environment variable management |
| **Container** | Docker + Compose | Deployment packaging |

---

## Project Structure

```
equitylens-ai/
│
├── app.py                        # Streamlit entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Configuration template
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Compose config
│
├── src/
│   ├── config/
│   │   └── settings.py           # Centralised env-driven config
│   │
│   ├── utils/
│   │   ├── rag_pipeline.py       # Core RAG logic
│   │   ├── history_manager.py    # Session persistence (JSON)
│   │   ├── pdf_export.py         # PDF report generation
│   │   └── logger.py             # Structured logging
│   │
│   └── components/
│       ├── styles.py             # Full CSS design system
│       ├── sidebar.py            # Sidebar UI component
│       └── result_display.py     # Answer + history rendering
│
├── data/
│   ├── vector_store/             # FAISS index (auto-generated, gitignored)
│   └── history/                  # Session history (auto-generated, gitignored)
│
├── tests/
│   └── test_rag_pipeline.py      # pytest test suite
│
├── .streamlit/
│   └── config.toml               # Dark theme configuration
│
├── README.md
├── RUNNING.md                    # Step-by-step execution guide
└── PORTFOLIO.md                  # Resume & interview prep
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- An API key from [xAI (Grok)](https://console.x.ai) **or** [OpenAI](https://platform.openai.com/api-keys)

### 1 — Clone & install

```bash
git clone https://github.com/BhoomikaSuri01/equitylens-ai.git
cd equitylens-ai
pip install -r requirements.txt
```

### 2 — Configure

```bash
cp .env.example .env
```

Open `.env` and set your API key:

```bash
# For xAI Grok (recommended — no embedding costs):
GROK_API_KEY=your_grok_api_key_here
LLM_BASE_URL=https://api.x.ai/v1
LLM_MODEL=grok-3-fast-beta
EMBEDDING_PROVIDER=local

# OR for OpenAI:
# OPENAI_API_KEY=your_openai_key_here
# LLM_MODEL=gpt-3.5-turbo-instruct
# EMBEDDING_PROVIDER=openai
```

### 3 — Run

```bash
streamlit run app.py
```

Open **http://localhost:8501** ✅

---

## Usage

1. **Paste URLs** — Add 1–5 financial news article URLs in the sidebar  
2. **Build Index** — Click *"Process & Build Index"* (downloads embedding model on first run ~30s)  
3. **Ask Questions** — Type research questions like:
   - *"What are the key risk factors mentioned?"*
   - *"Which companies are highlighted and why?"*
   - *"What is the projected revenue impact?"*
4. **Export** — Download your report as **PDF** or **TXT**  
5. **Review History** — All past sessions are saved in the *History* tab

---

## Deployment

### Streamlit Cloud (Free — recommended for portfolio)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Set entry point: `app.py`
4. Add secrets under **Settings → Secrets**:
   ```toml
   GROK_API_KEY = "your_key"
   LLM_BASE_URL = "https://api.x.ai/v1"
   LLM_MODEL = "grok-3-fast-beta"
   EMBEDDING_PROVIDER = "local"
   ```

### Docker

```bash
docker compose up --build -d
# App runs at http://localhost:8501
```

### Render / Railway

See [RUNNING.md](RUNNING.md) for full step-by-step instructions for Render, Railway, and AWS EC2.

---

## Configuration Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROK_API_KEY` | ✅ (or OpenAI) | — | xAI Grok API key |
| `OPENAI_API_KEY` | ✅ (or Grok) | — | OpenAI API key |
| `LLM_BASE_URL` | No | `https://api.x.ai/v1` | API endpoint URL |
| `LLM_MODEL` | No | `grok-3-fast-beta` | Model name |
| `EMBEDDING_PROVIDER` | No | `local` | `local` or `openai` |

---

## Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **RAG** | Grounds LLM answers in real retrieved source documents |
| **Semantic Search** | HuggingFace embeddings + FAISS cosine similarity |
| **Prompt Engineering** | `RetrievalQAWithSourcesChain` forces source citation |
| **LLM Integration** | OpenAI-compatible API (Grok/OpenAI) via LangChain |
| **API Abstraction** | Single codebase works with multiple LLM providers |
| **Data Persistence** | FAISS + JSON for stateful research sessions |

---

## Limitations

- Local FAISS is not horizontally scalable (swap for Pinecone/Weaviate in production)
- Article scraping quality depends on the site's HTML structure
- Some paywalled or JavaScript-heavy sites may not extract correctly

---

## Roadmap

- [ ] Streaming token-by-token responses
- [ ] Pinecone cloud vector store integration  
- [ ] Multi-PDF document upload support
- [ ] Stock price chart overlays (yfinance)
- [ ] Query history search & filtering

---

## Author

**Bhoomika Suri** — AI/ML Engineer

> This project demonstrates: LLM engineering · RAG pipelines · prompt engineering · vector databases · API integration · full-stack AI applications

---

## License

MIT — see [LICENSE](LICENSE)
