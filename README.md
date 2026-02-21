# 💰 FinMind — AI Personal Finance Mentor

> A GPT-4o-powered personal finance mentor that knows your actual expenses.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?logo=openai)](https://openai.com)

## Features

- 📝 **Expense CRUD** — Add, edit, delete, filter your monthly expenses
- 📊 **Live Budget Engine** — Instant 50/30/20 breakdown with benchmark alerts
- 🤖 **AI Mentor Chat** — GPT-4o with your real financial data injected
- 💯 **Financial Health Score** — 0–100 composite score
- 📈 **Dashboard** — Plotly charts, KPI cards, category analysis

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/finmind.git
cd finmind
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 · Add your OpenAI key in the sidebar for live AI.

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select repo → `app.py` → Deploy
4. Add `OPENAI_API_KEY` in App Settings → Secrets

See `finmind_documentation.docx` for full technical docs.
