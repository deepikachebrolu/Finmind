"""Dashboard Page — Financial Overview with Charts"""

import streamlit as st
from src.logic.budget import compute_budget, CATEGORY_COLORS


def render_dashboard_page():
    st.markdown("""
<h2 style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;margin-bottom:4px'>
📊 Financial Dashboard
</h2>
<p style='color:#8899aa;font-size:13px;margin-bottom:20px'>
Live overview of your finances. Update expenses to see instant changes.
</p>
""", unsafe_allow_html=True)

    month_expenses = [e for e in st.session_state.expenses if e.get("month") == "2026-02"]
    budget = compute_budget(month_expenses, st.session_state.income)
    income = st.session_state.income

    # ── KPI Row ────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "Monthly Income",  f"${income:,.0f}",                    "", "#ffd700"),
        (k2, "Net Savings",     f"${budget['net_savings']:,.0f}",      f"{budget['savings_rate']:.1f}% savings rate", "#00d4aa" if budget['net_savings'] >= 0 else "#ff4757"),
        (k3, "Total Expenses",  f"${budget['total_expenses']:,.0f}",   f"{budget['total_expenses']/income*100:.0f}% of income", "#ff6b35"),
        (k4, "Health Score",    f"{budget['health_score']} / 100",     "financial fitness", "#00d4aa" if budget['health_score'] >= 70 else "#ff6b35"),
    ]
    for col, label, val, sub, color in kpis:
        with col:
            st.markdown(f"""
<div style='background:#111925;border:1px solid #1e2d42;border-radius:12px;
     padding:18px;text-align:center;border-bottom:2px solid {color}'>
  <div style='font-size:10px;color:#4a6070;text-transform:uppercase;
       letter-spacing:1px;font-family:DM Mono,monospace'>{label}</div>
  <div style='font-family:Syne,sans-serif;font-size:28px;font-weight:800;
       color:{color};margin:8px 0 4px'>{val}</div>
  <div style='font-size:11px;color:#8899aa'>{sub}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ────────────────────────────────────────────────────────────
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("<div style='font-family:Syne,sans-serif;font-weight:700;font-size:14px;margin-bottom:12px'>Spending by Category</div>", unsafe_allow_html=True)

        try:
            import plotly.graph_objects as go
            if budget["category_detail"]:
                labels = [f"{item['icon']} {item['category']}" for item in budget["category_detail"]]
                values = [item["amount"] for item in budget["category_detail"]]
                colors = [item["color"] for item in budget["category_detail"]]

                fig = go.Figure(go.Pie(
                    labels=labels, values=values,
                    hole=0.55, marker_colors=colors,
                    textfont_size=12,
                    hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>"
                ))
                fig.update_layout(
                    paper_bgcolor="#111925", plot_bgcolor="#111925",
                    font_color="#e8f0fe", showlegend=True,
                    legend=dict(bgcolor="#111925", font_color="#8899aa"),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=300,
                    annotations=[dict(text=f"${budget['total_expenses']:,.0f}", x=0.5, y=0.5,
                                      font_size=18, font_color="#e8f0fe", showarrow=False)]
                )
                st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            _fallback_category_bars(budget)

    with col_chart2:
        st.markdown("<div style='font-family:Syne,sans-serif;font-weight:700;font-size:14px;margin-bottom:12px'>50/30/20 vs Actual</div>", unsafe_allow_html=True)

        try:
            import plotly.graph_objects as go
            categories_bar = ["Needs (50%)", "Wants (30%)", "Savings (20%)"]
            targets   = [income * 0.50, income * 0.30, income * 0.20]
            actuals   = [budget["needs"], budget["wants"], budget["saves"]]
            bar_colors = ["#7c5cfc", "#0099ff", "#00d4aa"]

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(name="Target", x=categories_bar, y=targets,
                                   marker_color=["rgba(124,92,252,0.3)","rgba(0,153,255,0.3)","rgba(0,212,170,0.3)"],
                                   marker_line_color=bar_colors, marker_line_width=1.5))
            fig2.add_trace(go.Bar(name="Actual", x=categories_bar, y=actuals,
                                   marker_color=bar_colors))
            fig2.update_layout(
                paper_bgcolor="#111925", plot_bgcolor="#111925",
                font_color="#e8f0fe", barmode="group",
                legend=dict(bgcolor="#111925", font_color="#8899aa"),
                yaxis=dict(gridcolor="#1e2d42", tickformat="$,.0f"),
                xaxis=dict(gridcolor="#1e2d42"),
                margin=dict(t=10, b=10, l=10, r=10), height=300
            )
            st.plotly_chart(fig2, use_container_width=True)
        except ImportError:
            _fallback_5030_bars(budget, income)

    # ── Category detail table ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Syne,sans-serif;font-weight:700;font-size:14px;margin-bottom:12px'>Category Breakdown</div>", unsafe_allow_html=True)

    for item in budget["category_detail"]:
        pct = min(item["amount"] / item["benchmark"] * 100, 120) if item["benchmark"] else 0
        bar_color = item["color"] if not item["over_budget"] else "#ff6b35"
        status = "⚠️" if item["over_budget"] else "✅"
        st.markdown(f"""
<div style='display:flex;align-items:center;gap:14px;padding:10px 14px;
     background:#111925;border:1px solid #1e2d42;border-radius:8px;margin-bottom:6px'>
  <div style='width:130px;font-size:13px'>{item["icon"]} {item["category"]}</div>
  <div style='flex:1;background:#1e2d42;border-radius:3px;height:6px;overflow:hidden'>
    <div style='width:{min(pct,100):.0f}%;height:100%;background:{bar_color};border-radius:3px'></div>
  </div>
  <div style='width:80px;font-family:DM Mono,monospace;font-size:13px;
       text-align:right;color:{item["color"]}'>${item["amount"]:,.0f}</div>
  <div style='width:50px;font-size:11px;color:#8899aa;text-align:right'>{item["percent"]:.1f}%</div>
  <div style='width:20px;text-align:right'>{status}</div>
</div>""", unsafe_allow_html=True)

    # ── AI Insights box ───────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    over_cats = [i for i in budget["category_detail"] if i["over_budget"]]
    insights = []

    if budget["savings_rate"] >= 20:
        insights.append("✅ **Savings rate is on target** — you're saving {:.1f}% of income.".format(budget["savings_rate"]))
    else:
        gap = income * 0.20 - budget["saves"]
        insights.append(f"⚠️ **Savings below 20% goal** — increase monthly savings by **${gap:,.0f}** to hit the target.")

    for cat in over_cats[:2]:
        excess = cat["amount"] - cat["benchmark"]
        insights.append(f"⚠️ **{cat['category']} is over budget** by **${excess:,.0f}** — consider trimming here first.")

    if budget["net_savings"] > 0:
        insights.append(f"💡 **${budget['net_savings']:,.0f} unallocated** this month — put it toward your top financial goal!")

    if insights:
        insight_html = "".join(f"<div style='font-size:13px;line-height:1.8;padding:4px 0;border-bottom:1px solid #1a2535'>{ins}</div>" for ins in insights)
        st.markdown(f"""
<div style='background:rgba(0,212,170,0.05);border:1px solid rgba(0,212,170,0.15);
     border-radius:12px;padding:16px 20px'>
  <div style='font-family:Syne,sans-serif;font-weight:700;font-size:14px;
       color:#00d4aa;margin-bottom:10px'>💡 AI Insights</div>
  {insight_html}
  <div style='margin-top:10px;font-size:12px;color:#4a6070'>
    Go to the AI Mentor Chat for deeper analysis →
  </div>
</div>""", unsafe_allow_html=True)


def _fallback_category_bars(budget):
    for item in budget["category_detail"][:6]:
        pct = min(item["percent"] / 30 * 100, 100)
        st.markdown(f"""
<div style='margin-bottom:8px'>
  <div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px'>
    <span>{item["icon"]} {item["category"]}</span>
    <span style='font-family:DM Mono,monospace;color:{item["color"]}'>${item["amount"]:,.0f}</span>
  </div>
  <div style='background:#1e2d42;border-radius:3px;height:6px'>
    <div style='width:{pct:.0f}%;height:100%;background:{item["color"]};border-radius:3px'></div>
  </div>
</div>""", unsafe_allow_html=True)


def _fallback_5030_bars(budget, income):
    items = [
        ("Needs (50%)", budget["needs"], budget["needs_pct"], income * 0.50, "#7c5cfc"),
        ("Wants (30%)", budget["wants"], budget["wants_pct"], income * 0.30, "#0099ff"),
        ("Savings(20%)",budget["saves"], budget["saves_pct"], income * 0.20, "#00d4aa"),
    ]
    for label, amt, pct, target, color in items:
        bar = min(amt / target * 100 if target else 0, 100)
        st.markdown(f"""
<div style='margin-bottom:12px'>
  <div style='display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px'>
    <span>{label}</span><span style='font-family:DM Mono,monospace;color:{color}'>${amt:,.0f} / ${target:,.0f}</span>
  </div>
  <div style='background:#1e2d42;border-radius:4px;height:8px'>
    <div style='width:{bar:.0f}%;height:100%;background:{color};border-radius:4px'></div>
  </div>
</div>""", unsafe_allow_html=True)
