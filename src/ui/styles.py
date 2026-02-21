"""
CSS and styling utilities for FinMind UI
"""

import streamlit as st


def inject_css():
    """Inject custom CSS for FinMind theme (dark mode, fonts, colors)."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');

    * {
        margin: 0;
        padding: 0;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: #0a0e17;
        color: #e8f0fe;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #0f141f;
        border-right: 1px solid #1e2d42;
    }

    [data-testid="stMainBlockContainer"] {
        background: #0a0e17;
        padding: 2rem 2.5rem;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    code, pre {
        font-family: 'DM Mono', monospace;
        background: #111925;
        border: 1px solid #1e2d42;
    }

    /* Buttons */
    button {
        background: #111925 !important;
        border: 1px solid #1e2d42 !important;
        color: #8899aa !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        font-family: inherit !important;
    }

    button:hover {
        background: #1a2535 !important;
        border-color: #00d4aa !important;
        color: #00d4aa !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, #00d4aa, #0099ff) !important;
        color: #0a0e17 !important;
        border: none !important;
        font-weight: 600 !important;
    }

    /* Inputs */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] select {
        background: #111925 !important;
        color: #e8f0fe !important;
        border: 1px solid #1e2d42 !important;
        border-radius: 6px !important;
    }

    /* Tabs */
    [data-testid="stTabs"] [role="tablist"] {
        border-bottom: 1px solid #1e2d42;
    }

    [data-testid="stTabs"] [role="tab"] {
        color: #8899aa;
        border-bottom: 2px solid transparent;
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #00d4aa;
        border-bottom-color: #00d4aa;
    }

    /* Metrics & info boxes */
    [data-testid="metric-container"] {
        background: #111925;
        border: 1px solid #1e2d42;
        border-radius: 10px;
        padding: 1rem;
    }

    /* Success / Error / Info messages */
    [data-testid="stAlert"] {
        background: rgba(0, 212, 170, 0.1);
        border: 1px solid rgba(0, 212, 170, 0.2);
        color: #00d4aa;
        border-radius: 8px;
    }

    /* Horizontal rule */
    hr {
        border: none;
        border-top: 1px solid #1e2d42;
        margin: 1.5rem 0;
    }

    /* Streamlit container / columns */
    [data-testid="stVerticalBlock"] > div {
        background: transparent;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #111925;
    }

    ::-webkit-scrollbar-thumb {
        background: #1e2d42;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #2a4070;
    }
    </style>
    """, unsafe_allow_html=True)
