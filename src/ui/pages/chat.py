"""AI Mentor Chat Page"""

import streamlit as st
from src.logic.ai_mentor import chat_with_gpt

QUICK_PROMPTS = [
    "Analyze my current budget and spending",
    "What is the best debt payoff strategy for me?",
    "How should I build my emergency fund?",
    "Am I saving enough? What should I change?",
    "Explain my 50/30/20 breakdown",
    "Create a 3-month savings plan for me",
]


def render_chat_page():
    st.markdown("""
<h2 style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;margin-bottom:4px'>
💬 AI Finance Mentor
</h2>
<p style='color:#8899aa;font-size:13px;margin-bottom:16px'>
Powered by GPT-4o · Knows your actual expenses and budget in real-time
</p>
""", unsafe_allow_html=True)

    # ── Quick prompt chips ─────────────────────────────────────────────────────
    st.markdown("<div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px'>", unsafe_allow_html=True)
    cols = st.columns(len(QUICK_PROMPTS))
    for i, (col, prompt) in enumerate(zip(cols, QUICK_PROMPTS)):
        with col:
            if st.button(prompt[:28] + "…" if len(prompt) > 28 else prompt,
                          key=f"qp_{i}", use_container_width=True):
                _send_message(prompt)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Message history ────────────────────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
<div style='background:rgba(0,212,170,0.06);border:1px solid rgba(0,212,170,0.18);
     border-radius:14px;padding:20px 24px;margin-bottom:16px'>
  <div style='font-family:Syne,sans-serif;font-size:16px;font-weight:700;margin-bottom:6px'>
    👋 Your AI Finance Mentor is ready
  </div>
  <div style='color:#8899aa;font-size:13px;line-height:1.6'>
    I have full access to your expense data and budget. Ask me anything — 
    from quick budget checks to deep financial strategy. I'll give you 
    personalized, numbers-backed advice.
  </div>
</div>""", unsafe_allow_html=True)

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
<div style='background:rgba(0,212,170,0.08);border:1px solid rgba(0,212,170,0.2);
     border-radius:14px;padding:14px 18px;margin-bottom:10px;
     border-right:3px solid #0099ff;text-align:right'>
  <div style='font-size:11px;color:#8899aa;font-family:DM Mono,monospace;margin-bottom:5px'>YOU</div>
  <div style='font-size:14px;line-height:1.6'>{msg["content"]}</div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div style='background:#111925;border:1px solid #1e2d42;border-radius:14px;
     padding:16px 18px;margin-bottom:10px;border-left:3px solid #00d4aa'>
  <div style='font-size:11px;color:#00d4aa;font-family:DM Mono,monospace;margin-bottom:5px'>💰 FINMIND AI</div>
  <div style='font-size:14px;line-height:1.7'>{msg["content"]}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Input ─────────────────────────────────────────────────────────────────
    with st.form(key="chat_form", clear_on_submit=True):
        col_inp, col_btn = st.columns([8, 1])
        with col_inp:
            user_input = st.text_input(
                "",
                placeholder="Ask anything about your finances… e.g. 'How do I reach 20% savings rate?'",
                label_visibility="collapsed",
                key="chat_input"
            )
        with col_btn:
            submitted = st.form_submit_button("➤", use_container_width=True)

        if submitted and user_input.strip():
            _send_message(user_input.strip())

    if st.session_state.messages:
        if st.button("🗑️ Clear conversation"):
            st.session_state.messages = []
            st.rerun()


def _send_message(text: str):
    """Add user message, get AI response, update state."""
    st.session_state.messages.append({"role": "user", "content": text})

    # Build history excluding current message
    history = [{"role": m["role"], "content": m["content"]}
               for m in st.session_state.messages[:-1]]

    with st.spinner("FinMind is thinking…"):
        reply = chat_with_gpt(
            api_key=st.session_state.api_key,
            user_message=text,
            history=history,
            expenses=st.session_state.expenses,
            income=st.session_state.income,
        )

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
