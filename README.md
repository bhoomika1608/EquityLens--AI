# 📊 EquityLens AI — RAG-Powered Equity Research Intelligence

<div align="center">

![EquityLens AI](https://img.shields.io/badge/EquityLens-AI-4361ee?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776ab?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?style=for-the-badge&logo=openai&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-00b4d8?style=for-the-badge)

**An institutional-grade equity research tool powered by Retrieval-Augmented Generation (RAG).**  
*Analyse financial news, ask research questions, and receive cited, AI-synthesised answers — all with a single API key.*

[**🚀 Quick Start**](#-quick-start) · [**🏗️ Architecture**](#️-architecture) · [**✨ Features**](#-features) · [**🚢 Deployment**](#-deployment) · [**📄 Portfolio**](#-portfolio-value)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **RAG Pipeline** | Load → chunk → embed → FAISS index → retrieve → LLM synthesise |
| 💬 **Cited Q&A** | Every answer includes source URLs for full traceability |
| 📊 **Confidence Scores** | AI self-evaluates answer confidence (0–100%) |
| 📚 **Research History** | All sessions persisted locally as JSON with stats |
| 📄 **PDF / TXT Export** | Download polished research reports instantly |
| 🎨 **Dark Mode UI** | Glassmorphism design system with animated gradients |
| ⚙️ **Configurable** | All settings via `.env` — model, chunk size, retrieval K |
| 🐳 **Dockerized** | One-command deployment with Docker Compose |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        EquityLens AI                            │
│                     RAG Architecture v2.0                       │
└─────────────────────────────────────────────────────────────────┘

   User Input (URLs)
         │
         ▼
   UnstructuredURLLoader          ← Web scraping & content extraction
         │
         ▼
   RecursiveCharacterTextSplitter ← 1000-token chunks, 200-token overlap
         │
         ▼
   OpenAI Embeddings              ← text-embedding-ada-002
   (text → 1536-dim vectors)
         │
         ▼
   FAISS Vector Index             ← Local vector database (persisted)
         │
         ▼
   User Question
         │
         ▼
   Semantic Retrieval (k=4)       ← Cosine similarity search
         │
         ▼
   RetrievalQAWithSourcesChain    ← LangChain orchestration
         │
         ▼
   OpenAI GPT-3.5                 ← Answer synthesis
         │
         ▼
   Answer + Sources + Confidence  → Streamlit UI → PDF/TXT Export
```

---

## 📂 Project Structure

```
Equity-Research-LLM-main/
│
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Pinned Python dependencies
├── .env.example                    # Environment variable template
├── .env                            # Your secrets (never committed)
├── .gitignore
├── Dockerfile                      # Production container
├── docker-compose.yml
│
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py             # Centralised app configuration
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py         # Core RAG logic (load→embed→query)
│   │   ├── history_manager.py      # JSON-backed session persistence
│   │   ├── pdf_export.py           # ReportLab PDF generation
│   │   └── logger.py               # Structured logging
│   │
│   └── components/
│       ├── __init__.py
│       ├── styles.py               # Full CSS design system
│       ├── sidebar.py              # Sidebar UI component
│       └── result_display.py      # Answer + history components
│
├── data/
│   ├── vector_store/               # FAISS index (auto-generated)
│   └── history/                    # research_history.json
│
├── .streamlit/
│   └── config.toml                 # Streamlit dark theme
│
├── tests/
│   └── test_rag_pipeline.py        # Unit tests
│
├── README.md
└── RUNNING.md                      # Step-by-step execution guide
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/equity-research-llm.git
cd equity-research-llm
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Open .env and set your OPENAI_API_KEY
```

### 3. Run

```bash
streamlit run app.py
```

Visit **http://localhost:8501** 🎉

---

## 🚢 Deployment

### Streamlit Cloud (Free)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as entry point
4. Add `OPENAI_API_KEY` in **Secrets** settings

### Docker

```bash
# Build & run
docker compose up --build -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

### Render.com

1. Create new **Web Service** → connect GitHub repo
2. Build command: `pip install -r requirements.txt`
3. Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
4. Add `OPENAI_API_KEY` environment variable

### Railway

```bash
railway init
railway up
railway variables set OPENAI_API_KEY=sk-...
```

### AWS EC2

```bash
# SSH into your instance, then:
git clone <repo>
cd equity-research-llm
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
# Configure security group to allow inbound TCP on port 8501
```

---

## 🔧 Configuration

All settings are controlled via `.env`:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | **required** | Your OpenAI API key |
| `LLM_MODEL` | `gpt-3.5-turbo-instruct` | LLM model for Q&A |

Advanced settings in `src/config/settings.py`:

| Setting | Default | Description |
|---|---|---|
| `chunk_size` | `1000` | Tokens per text chunk |
| `chunk_overlap` | `200` | Overlap between chunks |
| `k_retrieval` | `4` | Documents retrieved per query |
| `max_tokens` | `800` | Max LLM response length |

---

## 🧠 Key Concepts

| Concept | Implementation |
|---|---|
| **RAG** | Retrieval-Augmented Generation — grounds LLM answers in real source documents |
| **Embeddings** | Dense vector representations that capture semantic meaning |
| **FAISS** | Facebook AI Similarity Search — millisecond vector retrieval at scale |
| **LangChain** | Orchestration framework connecting LLMs, retrievers, and chains |
| **Prompt Engineering** | `RetrievalQAWithSourcesChain` forces the LLM to cite sources |

---

## ⚠️ Limitations

- Local FAISS is not horizontally scalable (use Pinecone/Weaviate for production)
- OpenAI API costs apply per query
- Web scraping quality depends on article site structure

---

## 🗺️ Roadmap

- [ ] Streaming LLM responses
- [ ] Pinecone cloud vector store integration
- [ ] Multi-PDF document support
- [ ] Stock ticker chart overlays (yfinance)
- [ ] Scheduled news monitoring
- [ ] User authentication

---

## 👩‍💻 Author

**Bhoomika Suri** — AI/ML Engineer

---

## 📄 License

MIT License — see [LICENSE](LICENSE)
