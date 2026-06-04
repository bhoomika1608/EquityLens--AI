"""
result_display.py — Components for rendering research results in EquityLens AI.

Includes:
  - Answer block with confidence ring
  - Source citations panel
  - Research history timeline
  - Stats metrics row
"""

from datetime import datetime, timezone

import streamlit as st

from src.utils.history_manager import load_history, clear_history, get_history_stats
from src.utils.pdf_export import generate_pdf_report


# ─────────────────────────────────────────────
# Confidence helpers
# ─────────────────────────────────────────────

def _confidence_class(score: int) -> str:
    if score >= 75:
        return "confidence-high"
    elif score >= 50:
        return "confidence-medium"
    return "confidence-low"


def _confidence_label(score: int) -> str:
    if score >= 75:
        return "High"
    elif score >= 50:
        return "Medium"
    return "Low"


# ─────────────────────────────────────────────
# Answer Panel
# ─────────────────────────────────────────────

def render_answer(
    question: str,
    answer: str,
    sources: list[str],
    confidence: int,
    urls: list[str],
) -> None:
    """
    Render the full research result panel.

    Args:
        question:   The user's research question.
        answer:     LLM-generated answer text.
        sources:    List of source URLs cited in the answer.
        confidence: Integer confidence score (0–100).
        urls:       Input article URLs that were analysed.
    """

    # ── Section header ──
    st.markdown(
        '<div class="glass-card-title">🔍 Research Result</div>',
        unsafe_allow_html=True,
    )

    # ── Question echo ──
    st.markdown(
        f'<div style="font-size:0.82rem;color:#a0a0b8;margin-bottom:0.5rem;">'
        f'<b>Question:</b> {question}</div>',
        unsafe_allow_html=True,
    )

    # ── Confidence ring ──
    css_class = _confidence_class(confidence)
    label = _confidence_label(confidence)
    st.markdown(
        f"""
        <div class="confidence-container">
            <div class="confidence-ring {css_class}">{confidence}%</div>
            <div class="confidence-text">
                <strong>{label} Confidence</strong><br>
                The AI is {confidence}% confident this answer is grounded in the source material.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Answer block ──
    st.markdown(
        f'<div class="answer-block">{answer}</div>',
        unsafe_allow_html=True,
    )

    # ── Sources ──
    if sources:
        st.markdown(
            '<div class="glass-card-title" style="margin-top:1rem;">📎 Source Citations</div>',
            unsafe_allow_html=True,
        )
        chips_html = "".join(
            f'<span class="source-chip">🔗 {src}</span>' for src in sources
        )
        st.markdown(
            f'<div style="display:flex;flex-wrap:wrap;gap:4px;">{chips_html}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No specific source URLs were cited for this answer.", icon="ℹ️")

    # ── Export buttons ──
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        try:
            pdf_bytes = generate_pdf_report(
                question=question,
                answer=answer,
                sources=sources,
                confidence=confidence,
                urls=urls,
            )
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name=f"equitylens_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except ImportError:
            st.caption("Install `reportlab` for PDF export")

    with col2:
        report_text = (
            f"EquityLens AI Research Report\n"
            f"{'='*40}\n"
            f"Question: {question}\n\n"
            f"Answer:\n{answer}\n\n"
            f"Confidence: {confidence}%\n\n"
            f"Sources:\n" + "\n".join(f"- {s}" for s in sources) +
            f"\n\nAnalysed URLs:\n" + "\n".join(f"- {u}" for u in urls)
        )
        st.download_button(
            label="📝 Download TXT",
            data=report_text,
            file_name=f"equitylens_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ─────────────────────────────────────────────
# Research History
# ─────────────────────────────────────────────

def render_history() -> None:
    """Render the full research history timeline."""
    history = load_history()

    if not history:
        st.markdown(
            """
            <div class="glass-card" style="text-align:center;padding:2.5rem;">
                <div style="font-size:2rem;margin-bottom:0.75rem;">📭</div>
                <div style="color:#a0a0b8;font-size:0.9rem;">No research history yet.</div>
                <div style="color:#6b6b8a;font-size:0.8rem;margin-top:0.4rem;">
                    Process URLs and ask questions to build your history.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Stats row
    stats = get_history_stats()
    cols = st.columns(3)
    with cols[0]:
        st.markdown(
            f'<div class="metric-card"><span class="metric-value">{stats["total_sessions"]}</span>'
            f'<div class="metric-label">Total Sessions</div></div>',
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            f'<div class="metric-card"><span class="metric-value">{stats["total_urls"]}</span>'
            f'<div class="metric-label">URLs Analysed</div></div>',
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            f'<div class="metric-card"><span class="metric-value">{stats["avg_confidence"]}%</span>'
            f'<div class="metric-label">Avg Confidence</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # History items
    for record in history:
        ts_raw = record.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_raw).strftime("%b %d, %Y · %H:%M UTC")
        except ValueError:
            ts = ts_raw

        conf = record.get("confidence", 0)
        conf_class = _confidence_class(conf)

        st.markdown(
            f"""
            <div class="history-item">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div class="history-question">❓ {record.get('question', '')}</div>
                    <div class="confidence-ring {conf_class}" style="width:40px;height:40px;font-size:0.72rem;flex-shrink:0;margin-left:8px;">{conf}%</div>
                </div>
                <div class="history-meta">
                    🕒 {ts} · {len(record.get('urls', []))} URL(s)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("View answer & sources", expanded=False):
            st.markdown(
                f'<div class="answer-block">{record.get("answer", "")}</div>',
                unsafe_allow_html=True,
            )
            srcs = record.get("sources", [])
            if srcs:
                for src in srcs:
                    st.markdown(f"🔗 `{src}`")

    st.divider()
    if st.button("🗑️ Clear All History", type="secondary"):
        clear_history()
        st.success("History cleared.")
        st.rerun()
