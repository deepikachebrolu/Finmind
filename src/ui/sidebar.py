"""Sidebar navigation and financial snapshot"""

import streamlit as st
from src.logic.budget import compute_budget


def render_sidebar():
    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown("""
<div style="padding:8px 0 20px;border-bottom:1px solid #1e2d42;margin-bottom:20px">
  <div style="display:flex;align-items:center;gap:10px">
    <div style="width:36px;height:36px;background:linear-gradient(135deg,#00d4aa,#0099ff);
         border-radius:10px;display:flex;align-items:center;justify-content:center;
         font-size:18px;box-shadow:0 0 16px rgba(0,212,170,0.3)">💰</div>
    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;letter-spacing:-0.5px">
      Fin<span style="color:#00d4aa">Mind</span>
    </div>
  </div>
  <div style="font-size:11px;color:#4a6070;margin-top:6px;font-family:'DM Mono',monospace;
       letter-spacing:0.5px">AI PERSONAL FINANCE MENTOR</div>
</div>
""", unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────────
        st.markdown("<div style='font-size:10px;color:#4a6070;letter-spacing:1.5px;text-transform:uppercase;font-family:DM Mono,monospace;margin-bottom:8px'>Navigation</div>", unsafe_allow_html=True)

        pages = [
            ("chat",      "💬", "AI Mentor Chat"),
            ("expenses",  "📝", "Expenses & Budget"),
            ("dashboard", "📊", "Dashboard"),
        ]

        for key, icon, label in pages:
            active = st.session_state.page == key
            style = "background:rgba(0,212,170,0.1);border:1px solid rgba(0,212,170,0.2);color:#00d4aa;" if active else "background:transparent;border:1px solid transparent;color:#8899aa;"
            if st.button(f"{icon}  {label}", key=f"nav_{key}",
                         use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown("---")

        # ── Quick Financial Snapshot ───────────────────────────────────────────
        budget = compute_budget(
            st.session_state.expenses,
            st.session_state.income
        )

        st.markdown("<div style='font-size:10px;color:#4a6070;letter-spacing:1.5px;text-transform:uppercase;font-family:DM Mono,monospace;margin-bottom:10px'>Snapshot</div>", unsafe_allow_html=True)

        snap_items = [
            ("Monthly Income",  f"${st.session_state.income:,.0f}", "#ffd700"),
            ("Total Expenses",  f"${budget['total_expenses']:,.0f}",  "#ff6b35" if budget['total_expenses'] > st.session_state.income * 0.8 else "#8899aa"),
            ("Net Savings",     f"${budget['net_savings']:,.0f}",     "#00d4aa" if budget['net_savings'] >= 0 else "#ff4757"),
            ("Savings Rate",    f"{budget['savings_rate']:.1f}%",     "#00d4aa" if budget['savings_rate'] >= 20 else "#ff6b35"),
        ]

        for label, val, color in snap_items:
            st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
     padding:7px 0;border-bottom:1px solid #1a2535">
  <span style="font-size:12px;color:#8899aa">{label}</span>
  <span style="font-family:'DM Mono',monospace;font-size:13px;font-weight:500;color:{color}">{val}</span>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Health Score Ring ──────────────────────────────────────────────────
        score = budget["health_score"]
        score_color = "#00d4aa" if score >= 70 else "#ff6b35" if score >= 40 else "#ff4757"
        score_label = "Excellent" if score >= 85 else "Good" if score >= 70 else "Fair" if score >= 40 else "Needs Work"

        # SVG ring progress
        circumference = 2 * 3.14159 * 28
        offset = circumference * (1 - score / 100)
        st.markdown(f"""
<div style="background:rgba(0,212,170,0.05);border:1px solid rgba(0,212,170,0.15);
     border-radius:12px;padding:14px;text-align:center;margin-top:4px">
  <div style="font-size:10px;color:#4a6070;letter-spacing:1px;text-transform:uppercase;
       font-family:'DM Mono',monospace;margin-bottom:8px">Financial Health</div>
  <svg width="70" height="70" viewBox="0 0 70 70" style="transform:rotate(-90deg)">
    <circle cx="35" cy="35" r="28" fill="none" stroke="#1e2d42" stroke-width="6"/>
    <circle cx="35" cy="35" r="28" fill="none" stroke="{score_color}" stroke-width="6"
      stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}" stroke-linecap="round"/>
  </svg>
  <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
       color:{score_color};margin-top:-44px;padding-bottom:16px">{score}</div>
  <div style="font-size:12px;color:#8899aa">{score_label}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        # ── API Key ────────────────────────────────────────────────────────────
        st.markdown("<div style='font-size:10px;color:#4a6070;letter-spacing:1px;text-transform:uppercase;font-family:DM Mono,monospace;margin-bottom:6px'>OpenAI API Key</div>", unsafe_allow_html=True)
        key = st.text_input("", value=st.session_state.api_key,
                            type="password", placeholder="sk-proj-...",
                            label_visibility="collapsed", key="api_input")
        if key != st.session_state.api_key:
            st.session_state.api_key = key
            st.rerun()

        if st.session_state.api_key:
            st.markdown("<div style='color:#00d4aa;font-size:11px;font-family:DM Mono,monospace'>✓ API key connected</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#ff6b35;font-size:11px;font-family:DM Mono,monospace'>⚠ Add key for live AI</div>", unsafe_allow_html=True)
