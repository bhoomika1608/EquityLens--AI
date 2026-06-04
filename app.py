"""
app.py — EquityLens AI: Main Streamlit Application Entry Point

This is the production-grade rewrite of the original main.py.

Architecture:
  - RAG Pipeline  (src/utils/rag_pipeline.py)   — URL loading, embedding, FAISS indexing
  - History       (src/utils/history_manager.py) — JSON-backed session persistence
  - PDF Export    (src/utils/pdf_export.py)       — Downloadable research reports
  - Config        (src/config/settings.py)        — Centralised env-driven configuration
  - Components    (src/components/)               — Modular UI building blocks
  - CSS           (src/components/styles.py)      — Full dark-mode design system

Run:
    streamlit run app.py
"""

import sys
import streamlit as st

# ── Page config must be the FIRST Streamlit call ──
st.set_page_config(
    page_title="EquityLens AI — Equity Research Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": "https://github.com",
        "About": "EquityLens AI v2.0 — RAG-powered equity research tool.",
    },
)

# ── Local imports (after set_page_config) ──
from src.config import validate_config, app_config, llm_config
from src.components.styles import inject_global_css
from src.components.sidebar import render_sidebar
from src.components.result_display import render_answer, render_history
from src.utils.rag_pipeline import build_vector_store, query_vector_store, vector_store_exists
from src.utils.history_manager import save_session
from src.utils.logger import get_logger

logger = get_logger(__name__)


# ─────────────────────────────────────────────
# CSS Injection
# ─────────────────────────────────────────────
inject_global_css()


# ─────────────────────────────────────────────
# API Key Validation Gate
# ─────────────────────────────────────────────
is_valid, config_errors = validate_config()

if not is_valid:
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">⚠️ Configuration Required</div>
            <div class="hero-subtitle">Set your OpenAI API key to get started</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.error("\n".join(config_errors))
    st.markdown(
        """
        ### 🔑 How to set your API key

        1. Copy `.env.example` to `.env`
        2. Replace `your_openai_api_key_here` with your actual key from [platform.openai.com](https://platform.openai.com)
        3. Restart the app: `streamlit run app.py`

        ```bash
        cp .env.example .env
        # Edit .env and add your key
        streamlit run app.py
        ```
        """
    )
    st.stop()


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
urls, process_clicked = render_sidebar()


# ─────────────────────────────────────────────
# Hero Banner
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">📊 EquityLens AI</div>
        <div class="hero-subtitle">Institutional-Grade Equity Research Powered by Retrieval-Augmented Generation</div>
        <span class="hero-badge">🤖 LLM</span>
        <span class="hero-badge">🔍 RAG</span>
        <span class="hero-badge">📈 Finance</span>
        <span class="hero-badge">⚡ FAISS</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# Main Tabs
# ─────────────────────────────────────────────
tab_research, tab_history, tab_about = st.tabs(
    ["🔬 Research", "📚 History", "ℹ️ About"]
)


# ═════════════════════════════════════════════
# TAB 1: RESEARCH
# ═════════════════════════════════════════════
with tab_research:

    # ── Step 1: Process URLs ──
    if process_clicked:
        if not urls:
            st.warning("⚠️ Please enter at least one article URL in the sidebar before processing.")
        else:
            st.markdown(
                '<div class="glass-card-title">⚙️ Building Research Index</div>',
                unsafe_allow_html=True,
            )
            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(message: str, percent: int) -> None:
                progress_bar.progress(percent / 100)
                status_text.markdown(
                    f'<span style="color:#a0a0b8;font-size:0.85rem;">⏳ {message}</span>',
                    unsafe_allow_html=True,
                )

            try:
                with st.spinner(""):
                    build_vector_store(urls=urls, progress_callback=update_progress)

                progress_bar.progress(1.0)
                status_text.empty()
                st.success(
                    f"✅ Index built from **{len(urls)} article(s)**. "
                    "You can now ask questions below.",
                    icon="🎉",
                )
                logger.info("Index built successfully from %d URLs", len(urls))

            except ValueError as exc:
                st.error(f"⚠️ Content loading failed: {exc}")
                logger.error("URL loading error: %s", exc)
            except Exception as exc:
                st.error(f"❌ Unexpected error building index: {exc}")
                logger.exception("Unexpected error during indexing")

    # ── Step 2: Query ──
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        # Check if index exists before showing the query box
        index_ready = vector_store_exists()

        if not index_ready:
            st.markdown(
                """
                <div class="glass-card" style="text-align:center;padding:3rem;">
                    <div style="font-size:3rem;margin-bottom:1rem;">🚀</div>
                    <div style="font-size:1.1rem;font-weight:600;color:#e8e8f0;margin-bottom:0.5rem;">
                        Start Your Research
                    </div>
                    <div style="color:#a0a0b8;font-size:0.9rem;max-width:400px;margin:0 auto;">
                        Add news article URLs in the sidebar and click 
                        <strong>"Process & Build Index"</strong> to begin AI-powered research.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="glass-card-title">💬 Ask a Research Question</div>',
                unsafe_allow_html=True,
            )

            question = st.text_area(
                "Research question",
                placeholder=(
                    "e.g. What are the key risk factors mentioned? "
                    "Which companies are highlighted? "
                    "What is the impact on inflation?"
                ),
                height=100,
                label_visibility="collapsed",
            )

            col_btn, col_hint = st.columns([1, 3])
            with col_btn:
                ask_clicked = st.button("🔍 Analyse", type="primary", use_container_width=True)
            with col_hint:
                st.caption("The AI will retrieve relevant passages and synthesise a cited answer.")

            if ask_clicked:
                if not question or not question.strip():
                    st.warning("Please enter a research question.")
                else:
                    with st.spinner("🤔 Analysing sources…"):
                        try:
                            result = query_vector_store(question.strip())
                            logger.info("Query succeeded for: %r", question[:60])

                            # Persist to history
                            save_session(
                                urls=urls or [],
                                question=question.strip(),
                                answer=result["answer"],
                                sources=result["sources"],
                                confidence=result["confidence"],
                            )

                            # Display results
                            st.divider()
                            render_answer(
                                question=question.strip(),
                                answer=result["answer"],
                                sources=result["sources"],
                                confidence=result["confidence"],
                                urls=urls or [],
                            )

                        except FileNotFoundError as exc:
                            st.error(f"⚠️ {exc}")
                        except Exception as exc:
                            st.error(f"❌ Query failed: {exc}")
                            logger.exception("Query error")


# ═════════════════════════════════════════════
# TAB 2: HISTORY
# ═════════════════════════════════════════════
with tab_history:
    st.markdown(
        '<div class="glass-card-title">📚 Research History</div>',
        unsafe_allow_html=True,
    )
    render_history()


# ═════════════════════════════════════════════
# TAB 3: ABOUT
# ═════════════════════════════════════════════
with tab_about:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown(
            """
            <div class="glass-card">
                <div class="glass-card-title">🏗️ How It Works</div>
                <ol style="color:#a0a0b8;font-size:0.9rem;line-height:2;">
                    <li>Paste 1–5 financial news article URLs</li>
                    <li>Click <strong style="color:#e8e8f0;">Process & Build Index</strong></li>
                    <li>EquityLens extracts, chunks, and embeds article text</li>
                    <li>Vectors are stored in a local FAISS index</li>
                    <li>Ask any research question</li>
                    <li>The RAG pipeline retrieves the most relevant passages</li>
                    <li>GPT synthesises a cited, grounded answer</li>
                    <li>Download your report as PDF or TXT</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="glass-card">
                <div class="glass-card-title">🧠 Technology Stack</div>
                <table style="width:100%;font-size:0.85rem;color:#a0a0b8;border-collapse:collapse;">
                    <tr><td style="padding:6px 0;"><strong style="color:#e8e8f0;">LLM</strong></td><td>OpenAI GPT-3.5-turbo-instruct</td></tr>
                    <tr><td style="padding:6px 0;"><strong style="color:#e8e8f0;">Embeddings</strong></td><td>OpenAI text-embedding-ada-002</td></tr>
                    <tr><td style="padding:6px 0;"><strong style="color:#e8e8f0;">Vector DB</strong></td><td>FAISS (local, blazing-fast)</td></tr>
                    <tr><td style="padding:6px 0;"><strong style="color:#e8e8f0;">Framework</strong></td><td>LangChain (community edition)</td></tr>
                    <tr><td style="padding:6px 0;"><strong style="color:#e8e8f0;">Web Scraping</strong></td><td>UnstructuredURLLoader</td></tr>
                    <tr><td style="padding:6px 0;"><strong style="color:#e8e8f0;">UI</strong></td><td>Streamlit + custom CSS</td></tr>
                    <tr><td style="padding:6px 0;"><strong style="color:#e8e8f0;">Export</strong></td><td>ReportLab (PDF), plain text</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="glass-card-title">📊 RAG Architecture</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#a0a0b8;line-height:2;">
                    User<br>
                    &nbsp;↓<br>
                    URL Loader<br>
                    &nbsp;↓<br>
                    Text Splitter<br>
                    <span style="color:#6b6b8a;">(1000 tokens, 200 overlap)</span><br>
                    &nbsp;↓<br>
                    OpenAI Embeddings<br>
                    <span style="color:#6b6b8a;">(ada-002)</span><br>
                    &nbsp;↓<br>
                    FAISS Index<br>
                    <span style="color:#6b6b8a;">(k=4 retrieval)</span><br>
                    &nbsp;↓<br>
                    RetrievalQA Chain<br>
                    &nbsp;↓<br>
                    GPT Answer + Sources<br>
                    &nbsp;↓<br>
                    PDF / TXT Export
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="glass-card-title">👩‍💻 Author</div>
                <div style="font-size:0.9rem;color:#e8e8f0;font-weight:600;">Bhoomika Suri</div>
                <div style="font-size:0.82rem;color:#a0a0b8;margin-top:4px;">AI/ML Engineer</div>
                <div style="font-size:0.78rem;color:#6b6b8a;margin-top:8px;">
                    Built to demonstrate LLM engineering, RAG pipelines,<br>
                    prompt engineering, and financial AI applications.
                </div>
                <div style="margin-top:12px;font-size:0.78rem;color:#4361ee;">
                    v{app_config.version} · EquityLens AI
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
