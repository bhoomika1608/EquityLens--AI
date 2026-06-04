"""
sidebar.py — Streamlit sidebar component for EquityLens AI.

Renders:
  - App branding (with active LLM provider badge)
  - URL input fields
  - Process button
  - System status indicator
  - Index stats
"""

import streamlit as st
from src.config import app_config, vector_config, llm_config
from src.utils.rag_pipeline import vector_store_exists
from src.utils.history_manager import get_history_stats


def render_sidebar() -> tuple[list[str], bool]:
    """
    Render the application sidebar.

    Returns:
        (urls, process_clicked) — list of non-empty URLs and whether
        the Process button was clicked this run.
    """
    with st.sidebar:
        # ── Logo / Branding ──
        provider = llm_config.provider_name
        st.markdown(
            f"""
            <div class="sidebar-logo">
                <div class="sidebar-logo-text">📊 EquityLens AI</div>
                <div style="font-size:0.72rem;color:#6b6b8a;margin-top:4px;">v2.1.0 · Research Intelligence</div>
                <div style="margin-top:8px;">
                    <span style="background:rgba(67,97,238,0.15);border:1px solid rgba(67,97,238,0.3);color:#818cf8;font-size:0.68rem;font-weight:700;padding:2px 8px;border-radius:10px;letter-spacing:0.05em;">⚡ {provider}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Status Indicator ──
        has_index = vector_store_exists()
        if has_index:
            st.markdown(
                '<span class="status-dot status-ready"></span>'
                '<span style="font-size:0.82rem;color:#10b981;font-weight:600;">Index Ready</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span class="status-dot status-warn"></span>'
                '<span style="font-size:0.82rem;color:#f59e0b;font-weight:600;">No Index — Add URLs Below</span>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sidebar-section-header">📰 Article URLs</div>', unsafe_allow_html=True)
        st.caption("Add up to 5 news article URLs for analysis")

        urls: list[str] = []
        for i in range(app_config.max_urls):
            url = st.text_input(
                f"URL {i + 1}",
                placeholder="https://example.com/article",
                key=f"url_input_{i}",
                label_visibility="collapsed" if i > 0 else "visible",
            )
            if url and url.strip():
                urls.append(url.strip())

        process_clicked = st.button(
            "⚡ Process & Build Index",
            use_container_width=True,
            type="primary",
        )

        # ── History Stats ──
        stats = get_history_stats()
        if stats["total_sessions"] > 0:
            st.markdown('<div class="sidebar-section-header">📈 Session Stats</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.metric("Sessions", stats["total_sessions"])
            col2.metric("Avg Confidence", f"{stats['avg_confidence']}%")

        # ── Settings ──
        st.markdown('<div class="sidebar-section-header">⚙️ Settings</div>', unsafe_allow_html=True)
        st.caption(f"Provider: `{llm_config.provider_name}`")
        st.caption(f"Model: `{llm_config.model_name}`")
        st.caption(f"Chunk size: `{vector_config.chunk_size}` tokens")
        st.caption(f"Top-K retrieval: `{vector_config.k_retrieval}` docs")

        # ── Links ──
        st.divider()
        st.markdown(
            """
            <div style="font-size:0.72rem;color:#6b6b8a;text-align:center;">
                Built with LangChain · OpenAI · FAISS<br>
                <a href="https://github.com" style="color:#4361ee;text-decoration:none;">GitHub</a> ·
                <a href="#" style="color:#4361ee;text-decoration:none;">Docs</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return urls, process_clicked
