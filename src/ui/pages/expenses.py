"""
Expenses & Budget Page
Full CRUD: Add, Edit, Delete expenses → live budget recalculation
"""

import streamlit as st
from src.config import EXPENSE_CATEGORIES, EXPENSE_TYPES, MONTHS
from src.logic.budget import compute_budget, CATEGORY_COLORS, CATEGORY_ICONS
from src.utils import hex_to_rgb


def render_expenses_page():
    st.markdown("""
<h2 style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;margin-bottom:4px'>
📝 Expenses & Budget Planner
</h2>
<p style='color:#8899aa;font-size:13px;margin-bottom:20px'>
Add, edit, and delete your expenses. Budget recalculates instantly.
</p>
""", unsafe_allow_html=True)

    # ── Income input ──────────────────────────────────────────────────────────
    col_inc, col_month, _ = st.columns([2, 2, 4])
    with col_inc:
        new_income = st.number_input(
            "💵 Monthly Income ($)",
            min_value=0.0, max_value=500000.0,
            value=float(st.session_state.income),
            step=100.0, format="%.2f"
        )
        if new_income != st.session_state.income:
            st.session_state.income = new_income
            st.rerun()

    with col_month:
        selected_month = st.selectbox("📅 Month", MONTHS, index=0)

    st.markdown("---")

    # ── Live budget summary bar ───────────────────────────────────────────────
    month_expenses = [e for e in st.session_state.expenses if e.get("month") == selected_month]
    budget = compute_budget(month_expenses, st.session_state.income)

    c1, c2, c3, c4 = st.columns(4)
    _metric(c1, "Total Expenses",  f"${budget['total_expenses']:,.0f}", f"of ${st.session_state.income:,.0f} income", "#ff6b35" if budget['total_expenses'] > st.session_state.income else "#8899aa")
    _metric(c2, "Net Savings",     f"${budget['net_savings']:,.0f}",    "left after expenses", "#00d4aa" if budget['net_savings'] >= 0 else "#ff4757")
    _metric(c3, "Savings Rate",    f"{budget['savings_rate']:.1f}%",    "goal: ≥20%", "#00d4aa" if budget['savings_rate'] >= 20 else "#ff6b35")
    _metric(c4, "Health Score",    f"{budget['health_score']}/100",     "financial fitness", "#00d4aa" if budget['health_score'] >= 70 else "#ff6b35")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 50/30/20 progress bars ────────────────────────────────────────────────
    st.markdown("<div style='font-family:Syne,sans-serif;font-weight:700;font-size:15px;margin-bottom:10px'>50/30/20 Rule Breakdown</div>", unsafe_allow_html=True)

    rule_items = [
        ("🏠 Needs",   budget['needs'],  budget['needs_pct'],  50,  "#7c5cfc"),
        ("🎉 Wants",   budget['wants'],  budget['wants_pct'],  30,  "#0099ff"),
        ("💰 Savings", budget['saves'],  budget['saves_pct'],  20,  "#00d4aa"),
    ]

    cols = st.columns(3)
    for col, (label, amt, pct, target, color) in zip(cols, rule_items):
        with col:
            on_track = (label.startswith("💰") and pct >= target) or (not label.startswith("💰") and pct <= target)
            status = "✅" if on_track else "⚠️"
            filled = min(pct / target * 100, 100) if target > 0 else 0
            bar_color = color if on_track else "#ff6b35"
            st.markdown(f"""
<div style='background:#111925;border:1px solid #1e2d42;border-radius:10px;padding:14px'>
  <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
    <span style='font-size:13px;color:#e8f0fe'>{label}</span>
    <span style='font-size:11px;color:#8899aa'>{status} {pct:.1f}% / {target}%</span>
  </div>
  <div style='background:#1e2d42;border-radius:4px;height:8px;overflow:hidden'>
    <div style='width:{filled:.0f}%;height:100%;background:{bar_color};border-radius:4px;transition:width 0.5s'></div>
  </div>
  <div style='font-family:DM Mono,monospace;font-size:13px;color:{color};margin-top:6px'>${amt:,.0f}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs: List | Add | Edit | Category View ───────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📋  Expense List", "➕  Add Expense", "📊  By Category"])

    with tab1:
        _render_expense_list(month_expenses, selected_month)

    with tab2:
        _render_add_form(selected_month)

    with tab3:
        _render_category_view(budget)


def _metric(col, label, value, sub, color):
    with col:
        st.markdown(f"""
<div style='background:#111925;border:1px solid #1e2d42;border-radius:12px;padding:16px;text-align:center'>
  <div style='font-size:10px;color:#4a6070;text-transform:uppercase;letter-spacing:1px;font-family:DM Mono,monospace'>{label}</div>
  <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:{color};margin:6px 0 2px'>{value}</div>
  <div style='font-size:11px;color:#8899aa'>{sub}</div>
</div>""", unsafe_allow_html=True)


def _render_expense_list(month_expenses, selected_month):
    """Render editable list of expenses."""
    if not month_expenses:
        st.info("No expenses for this month yet. Add one in the 'Add Expense' tab!")
        return

    # Filter / search
    col_s, col_f, _ = st.columns([2, 2, 3])
    with col_s:
        search = st.text_input("🔍 Search", placeholder="Filter expenses...", key="search_exp")
    with col_f:
        filter_cat = st.selectbox("Category", ["All"] + EXPENSE_CATEGORIES, key="filter_cat")

    filtered = month_expenses
    if search:
        filtered = [e for e in filtered if search.lower() in e["name"].lower() or search.lower() in e["category"].lower()]
    if filter_cat != "All":
        filtered = [e for e in filtered if e["category"] == filter_cat]

    st.markdown(f"<div style='color:#8899aa;font-size:12px;margin-bottom:10px'>{len(filtered)} expense(s)</div>", unsafe_allow_html=True)

    # Edit state
    if "editing_id" not in st.session_state:
        st.session_state.editing_id = None

    for exp in filtered:
        color = CATEGORY_COLORS.get(exp["category"], "#8899aa")
        icon  = CATEGORY_ICONS.get(exp["category"], "📦")

        if st.session_state.editing_id == exp["id"]:
            # ── Inline edit form ──────────────────────────────────────────────
            with st.container():
                st.markdown(f"<div style='background:rgba(0,212,170,0.06);border:1px solid rgba(0,212,170,0.25);border-radius:10px;padding:14px;margin-bottom:8px'>", unsafe_allow_html=True)
                ec1, ec2, ec3, ec4 = st.columns([3, 2, 2, 1])
                with ec1:
                    new_name = st.text_input("Name", value=exp["name"], key=f"ename_{exp['id']}")
                with ec2:
                    new_cat = st.selectbox("Category", EXPENSE_CATEGORIES,
                                           index=EXPENSE_CATEGORIES.index(exp["category"]) if exp["category"] in EXPENSE_CATEGORIES else 0,
                                           key=f"ecat_{exp['id']}")
                with ec3:
                    new_amt = st.number_input("Amount ($)", value=float(exp["amount"]),
                                              min_value=0.0, step=10.0, key=f"eamt_{exp['id']}")
                with ec4:
                    new_type = st.selectbox("Type", EXPENSE_TYPES,
                                            index=EXPENSE_TYPES.index(exp["type"]) if exp["type"] in EXPENSE_TYPES else 0,
                                            key=f"etype_{exp['id']}")

                bc1, bc2, _ = st.columns([1, 1, 4])
                with bc1:
                    if st.button("✅ Save", key=f"save_{exp['id']}"):
                        for e in st.session_state.expenses:
                            if e["id"] == exp["id"]:
                                e["name"]     = new_name
                                e["category"] = new_cat
                                e["amount"]   = new_amt
                                e["type"]     = new_type
                        st.session_state.editing_id = None
                        st.rerun()
                with bc2:
                    if st.button("✖ Cancel", key=f"cancel_{exp['id']}"):
                        st.session_state.editing_id = None
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            # ── Read row ──────────────────────────────────────────────────────
            rc1, rc2, rc3, rc4, rc5 = st.columns([3, 2, 2, 1, 1])
            with rc1:
                st.markdown(f"<div style='padding:10px 4px'>{icon} <b>{exp['name']}</b></div>", unsafe_allow_html=True)
            with rc2:
                st.markdown(f"<div style='padding:10px 4px'><span style='background:rgba({_hex_to_rgb(color)},0.15);color:{color};padding:3px 8px;border-radius:10px;font-size:11px;font-family:DM Mono,monospace'>{exp['category']}</span></div>", unsafe_allow_html=True)
            with rc3:
                st.markdown(f"<div style='padding:10px 4px;font-family:DM Mono,monospace;font-size:14px;font-weight:600;color:{color}'>${exp['amount']:,.2f}</div>", unsafe_allow_html=True)
            with rc4:
                if st.button("✏️", key=f"edit_{exp['id']}", help="Edit"):
                    st.session_state.editing_id = exp["id"]
                    st.rerun()
            with rc5:
                if st.button("🗑️", key=f"del_{exp['id']}", help="Delete"):
                    st.session_state.expenses = [e for e in st.session_state.expenses if e["id"] != exp["id"]]
                    st.rerun()


def _render_add_form(selected_month):
    """Add new expense form."""
    st.markdown("<div style='max-width:520px'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Expense Name *", placeholder="e.g. Netflix, Rent, Groceries", key="add_name")
    with col2:
        amount = st.number_input("Amount ($) *", min_value=0.01, max_value=100000.0,
                                  value=100.0, step=10.0, key="add_amount")

    col3, col4 = st.columns(2)
    with col3:
        category = st.selectbox("Category *", EXPENSE_CATEGORIES, key="add_cat")
    with col4:
        exp_type = st.selectbox("Type", EXPENSE_TYPES, key="add_type")

    note = st.text_input("Note (optional)", placeholder="Any details...", key="add_note")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("➕  Add Expense", type="primary", use_container_width=False):
        if not name:
            st.error("Please enter an expense name.")
        else:
            new_exp = {
                "id":       st.session_state.next_id,
                "name":     name,
                "category": category,
                "amount":   amount,
                "type":     exp_type,
                "month":    selected_month,
                "note":     note,
            }
            st.session_state.expenses.append(new_exp)
            st.session_state.next_id += 1
            st.success(f"✅ '{name}' added — ${amount:,.2f}")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _render_category_view(budget):
    """Grouped by category with spend vs benchmark bars."""
    if not budget["category_detail"]:
        st.info("Add expenses to see category breakdown.")
        return

    for item in budget["category_detail"]:
        pct_of_benchmark = (item["amount"] / item["benchmark"] * 100) if item["benchmark"] > 0 else 0
        bar_w = min(pct_of_benchmark, 100)
        bar_color = item["color"] if not item["over_budget"] else "#ff6b35"
        status = "⚠️ Over" if item["over_budget"] else "✅ OK"

        st.markdown(f"""
<div style='background:#111925;border:1px solid #1e2d42;border-radius:10px;
     padding:14px 16px;margin-bottom:8px'>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
    <span style='font-size:14px'>{item["icon"]} <b>{item["category"]}</b></span>
    <div style='display:flex;gap:16px;align-items:center'>
      <span style='font-size:11px;color:#8899aa'>{status} · benchmark: ${item["benchmark"]:,.0f}</span>
      <span style='font-family:DM Mono,monospace;font-size:15px;font-weight:600;color:{item["color"]}'>${item["amount"]:,.0f}</span>
    </div>
  </div>
  <div style='background:#1e2d42;border-radius:4px;height:6px;overflow:hidden'>
    <div style='width:{bar_w:.0f}%;height:100%;background:{bar_color};border-radius:4px'></div>
  </div>
  <div style='font-size:11px;color:#4a6070;margin-top:4px'>{item["percent"]:.1f}% of income</div>
</div>""", unsafe_allow_html=True)

