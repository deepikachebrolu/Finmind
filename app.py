"""
FinMind — AI Personal Finance Mentor
Main Streamlit Application Entry Point
"""

import streamlit as st

from src.config import (
    STREAMLIT_PAGE_CONFIG,
    DEFAULT_INCOME,
    DEFAULT_EXPENSES,
    DEFAULT_NEXT_ID,
)
from src.ui.styles import inject_css
from src.ui.sidebar import render_sidebar
from src.ui.pages.chat import render_chat_page
from src.ui.pages.expenses import render_expenses_page
from src.ui.pages.dashboard import render_dashboard_page

# Page config MUST be first Streamlit call
st.set_page_config(**STREAMLIT_PAGE_CONFIG)


def init_state():
    """Initialize session state with default values."""
    defaults = {
        "page": "chat",
        "messages": [],
        "expenses": DEFAULT_EXPENSES.copy(),
        "income": DEFAULT_INCOME,
        "api_key": "",
        "next_id": DEFAULT_NEXT_ID,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def main():
    init_state()
    inject_css()
    render_sidebar()

    page = st.session_state.page
    if page == "chat":
        render_chat_page()
    elif page == "expenses":
        render_expenses_page()
    elif page == "dashboard":
        render_dashboard_page()


if __name__ == "__main__":
    main()
