"""
styles.py — Global CSS injection for the EquityLens AI Streamlit app.

This module injects a complete design system:
  - Custom fonts (Inter via Google Fonts)
  - Dark mode color tokens
  - Glassmorphism card components
  - Animated gradient hero section
  - Professional metric badges
  - Sidebar styling
  - Responsive typography
"""

import streamlit as st


def inject_global_css() -> None:
    """Inject the full CSS design system into the Streamlit page."""
    st.markdown(
        """
<style>
/* ═══════════════════════════════════════════
   FONTS
═══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════
   COLOR TOKENS
═══════════════════════════════════════════ */
:root {
    --bg-primary:    #0f0f1a;
    --bg-secondary:  #1a1a2e;
    --bg-card:       rgba(26, 26, 46, 0.85);
    --bg-card-hover: rgba(36, 36, 66, 0.95);
    --accent-blue:   #4361ee;
    --accent-purple: #7c3aed;
    --accent-teal:   #06b6d4;
    --accent-green:  #10b981;
    --accent-amber:  #f59e0b;
    --accent-red:    #ef4444;
    --text-primary:  #e8e8f0;
    --text-secondary:#a0a0b8;
    --text-muted:    #6b6b8a;
    --border:        rgba(99, 102, 241, 0.2);
    --border-bright: rgba(99, 102, 241, 0.5);
    --gradient-hero: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    --gradient-blue: linear-gradient(135deg, #4361ee, #7c3aed);
    --gradient-teal: linear-gradient(135deg, #06b6d4, #10b981);
    --shadow-card:   0 4px 24px rgba(0, 0, 0, 0.4);
    --shadow-glow:   0 0 20px rgba(67, 97, 238, 0.15);
    --radius-sm:     8px;
    --radius-md:     12px;
    --radius-lg:     16px;
    --radius-xl:     24px;
}

/* ═══════════════════════════════════════════
   BASE RESET
═══════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* Hide default Streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* Main content area */
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
.block-container {
    padding: 1.5rem 2.5rem 3rem !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* ═══════════════════════════════════════════
   HERO HEADER BANNER
═══════════════════════════════════════════ */
.hero-banner {
    background: linear-gradient(135deg, #0f0f1a 0%, #16213e 40%, #1a1a2e 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-glow);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(67,97,238,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(124,58,237,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #e8e8f0 0%, #a0a0b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.02em;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin: 0 0 1.2rem 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(67,97,238,0.15);
    border: 1px solid rgba(67,97,238,0.3);
    color: #818cf8;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-right: 8px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ═══════════════════════════════════════════
   GLASSMORPHISM CARDS
═══════════════════════════════════════════ */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--shadow-card);
    transition: all 0.25s ease;
}
.glass-card:hover {
    border-color: var(--border-bright);
    box-shadow: var(--shadow-glow), var(--shadow-card);
    transform: translateY(-1px);
}
.glass-card-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ═══════════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════════ */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: all 0.2s ease;
}
.metric-card:hover { border-color: var(--border-bright); transform: translateY(-2px); }
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-blue);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
}
.metric-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-weight: 500;
    margin-top: 4px;
}

/* ═══════════════════════════════════════════
   CONFIDENCE SCORE RING
═══════════════════════════════════════════ */
.confidence-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 0.75rem 0;
}
.confidence-ring {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    flex-shrink: 0;
}
.confidence-high   { background: rgba(16,185,129,0.15); border: 2px solid #10b981; color: #10b981; }
.confidence-medium { background: rgba(245,158,11,0.15); border: 2px solid #f59e0b; color: #f59e0b; }
.confidence-low    { background: rgba(239,68,68,0.15);  border: 2px solid #ef4444; color: #ef4444; }
.confidence-text { font-size: 0.85rem; color: var(--text-secondary); }
.confidence-text strong { color: var(--text-primary); font-weight: 600; }

/* ═══════════════════════════════════════════
   SOURCE CHIPS
═══════════════════════════════════════════ */
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.25);
    color: #67e8f9;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 4px 10px;
    border-radius: 6px;
    margin: 3px;
    word-break: break-all;
    transition: all 0.15s;
}
.source-chip:hover { background: rgba(6,182,212,0.18); border-color: rgba(6,182,212,0.5); }

/* ═══════════════════════════════════════════
   ANSWER BLOCK
═══════════════════════════════════════════ */
.answer-block {
    background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.9));
    border: 1px solid rgba(67,97,238,0.3);
    border-left: 4px solid #4361ee;
    border-radius: var(--radius-md);
    padding: 1.5rem 1.75rem;
    font-size: 0.97rem;
    line-height: 1.75;
    color: var(--text-primary);
    margin: 0.75rem 0;
}

/* ═══════════════════════════════════════════
   HISTORY TIMELINE
═══════════════════════════════════════════ */
.history-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    position: relative;
    transition: all 0.2s;
}
.history-item:hover { border-color: var(--border-bright); }
.history-item::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--gradient-blue);
    border-radius: 4px 0 0 4px;
}
.history-question { font-weight: 600; font-size: 0.9rem; color: var(--text-primary); }
.history-meta { font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }

/* ═══════════════════════════════════════════
   STATUS INDICATORS
═══════════════════════════════════════════ */
.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
}
.status-ready  { background: #10b981; box-shadow: 0 0 6px #10b981; }
.status-warn   { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }
.status-error  { background: #ef4444; box-shadow: 0 0 6px #ef4444; }

/* ═══════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p { font-size: 0.85rem; color: var(--text-secondary); }
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 1rem;
}
.sidebar-logo-text {
    font-size: 1.4rem;
    font-weight: 800;
    background: var(--gradient-blue);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sidebar-section-header {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.75rem 0 0.4rem;
    border-top: 1px solid var(--border);
    margin-top: 0.5rem;
}

/* ═══════════════════════════════════════════
   BUTTONS (Streamlit override)
═══════════════════════════════════════════ */
.stButton > button {
    background: var(--gradient-blue) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 12px rgba(67,97,238,0.3) !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(67,97,238,0.45) !important;
}

/* ═══════════════════════════════════════════
   TEXT INPUTS
═══════════════════════════════════════════ */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextArea"] > div > div > textarea {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTextInput"] > div > div > input:focus,
[data-testid="stTextArea"] > div > div > textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(67,97,238,0.2) !important;
}

/* ═══════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════ */
[data-testid="stProgress"] > div {
    background: var(--bg-secondary) !important;
    border-radius: 100px !important;
}
[data-testid="stProgress"] > div > div {
    background: var(--gradient-blue) !important;
    border-radius: 100px !important;
}

/* ═══════════════════════════════════════════
   TABS
═══════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: var(--text-secondary) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--accent-blue) !important;
}

/* ═══════════════════════════════════════════
   DIVIDERS
═══════════════════════════════════════════ */
hr { border-color: var(--border) !important; }

/* ═══════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--border-bright);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }

/* ═══════════════════════════════════════════
   ALERTS / INFO BOXES
═══════════════════════════════════════════ */
.stAlert { border-radius: var(--radius-md) !important; }

/* ═══════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )
