# 📊 EquityLens AI – Equity Research Assistant

## 🚀 Overview

EquityLens AI is an AI-powered equity research application that helps users analyze financial news articles and generate research-based insights.

The application uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant information from financial news articles and answer user queries with source-backed responses.

Instead of relying only on the language model's knowledge, EquityLens AI grounds its responses using content extracted directly from financial news sources.

---

## 🎯 Key Features

* Input multiple financial news article URLs
* Automatic article content extraction
* Intelligent text chunking and preprocessing
* Semantic search using embeddings
* RAG-based question answering
* Source citations for transparency
* Confidence score for generated responses
* Research history tracking
* PDF report generation
* Interactive dashboard built with Streamlit
* Dark mode support

---

## 🧠 How It Works

1. User enters financial news article URLs
2. Article content is extracted and processed
3. Text is divided into smaller chunks
4. Embeddings are generated for each chunk
5. Embeddings are stored in a FAISS vector database
6. User asks a research question
7. Relevant chunks are retrieved using semantic search
8. The LLM generates an answer using retrieved context
9. Results are displayed along with source references and confidence scores

---

## 🏗️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### LLM Framework

* LangChain

### Language Models

* OpenAI / xAI Grok

### Embeddings

* HuggingFace Sentence Transformers
* all-MiniLM-L6-v2

### Vector Database

* FAISS

### PDF Generation

* ReportLab

### Environment Management

* python-dotenv

---

## 📂 Project Structure

```text
equitylens-ai/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── src/
│   ├── components/
│   ├── config/
│   └── utils/
│
├── data/
│   ├── history/
│   └── vector_store/
│
├── tests/
│
└── Dockerfile
```

## 💡 Example Usage

### Step 1

Paste one or more financial news article URLs.

### Step 2

Click **Process Articles** to build the knowledge base.

### Step 3

Ask questions such as:

* What are the major risks discussed?
* Which companies are mentioned?
* What is the expected impact on revenue?
* What investment opportunities are highlighted?

### Step 4

The system returns:

* AI-generated answer
* Source references
* Confidence score
* Downloadable research report

---

## 🔍 Architecture (Conceptual)

```text
User
   ↓
Streamlit UI
   ↓
URL Loader
   ↓
Text Splitter
   ↓
Embeddings
   ↓
FAISS Vector Store
   ↓
Retriever
   ↓
LLM
   ↓
Answer + Sources + Confidence Score
```

---

## ⚠️ Limitations

* Requires an OpenAI or Grok API key
* Retrieval quality depends on article content
* Some paywalled articles may not be processed correctly
* Local FAISS storage is not designed for large-scale deployment

---

## 🚀 Future Improvements

* Support PDF and document uploads
* Integration with Pinecone or Weaviate
* Real-time streaming responses
* Advanced financial metrics dashboard
* Stock comparison module
* Multi-source research reports

---

## 🧠 Key Concepts Demonstrated

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Embeddings
* Prompt Engineering
* Financial News Analysis
* LLM-based Question Answering
* Streamlit Application Development

---

## 👨‍💻 Author

Bhoomika Suri

Developed as an AI-powered financial research assistant to explore the application of LLMs and RAG systems in equity research workflows.
