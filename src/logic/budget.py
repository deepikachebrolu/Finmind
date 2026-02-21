"""
Core budget calculation logic.
All financial math lives here — pure functions, no Streamlit.
"""

from typing import List, Dict, Any
from src.config import (
    CATEGORY_COLORS,
    CATEGORY_ICONS,
    BUDGET_BENCHMARKS,
    BUDGET_NEEDS_CATEGORIES,
    BUDGET_WANTS_CATEGORIES,
)


def compute_budget(expenses: List[Dict], income: float) -> Dict[str, Any]:
    """Compute full budget breakdown from expense list and income."""
    if not expenses or income <= 0:
        return _empty_budget(income)

    # Sum by category
    by_category: Dict[str, float] = {}
    for e in expenses:
        cat = e.get("category", "Other")
        by_category[cat] = by_category.get(cat, 0) + e.get("amount", 0)

    total_expenses = sum(by_category.values())

    # Separate savings from spending
    savings_total = by_category.get("Savings", 0)
    spending_total = total_expenses - savings_total
    net_savings = income - spending_total - savings_total
    savings_rate = ((savings_total + max(net_savings, 0)) / income * 100) if income > 0 else 0

    # 50/30/20 breakdown
    needs = sum(v for k, v in by_category.items() if k in BUDGET_NEEDS_CATEGORIES)
    wants = sum(v for k, v in by_category.items() if k in BUDGET_WANTS_CATEGORIES)
    saves = savings_total + max(net_savings, 0)

    needs_pct  = needs / income * 100 if income else 0
    wants_pct  = wants / income * 100 if income else 0
    saves_pct  = saves / income * 100 if income else 0

    # Category breakdown with benchmarks
    category_detail = []
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        benchmark = BUDGET_BENCHMARKS.get(cat, 0.05) * income
        over = amt > benchmark * 1.1
        category_detail.append({
            "category": cat,
            "amount": amt,
            "percent": amt / income * 100 if income else 0,
            "benchmark": benchmark,
            "over_budget": over,
            "color": CATEGORY_COLORS.get(cat, "#8899aa"),
            "icon": CATEGORY_ICONS.get(cat, "📦"),
        })

    # Health score (0–100)
    health_score = _calculate_health_score(
        savings_rate, needs_pct, wants_pct, net_savings, income
    )

    return {
        "total_expenses": total_expenses,
        "spending_total": spending_total,
        "savings_total": savings_total,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "needs": needs,
        "wants": wants,
        "saves": saves,
        "needs_pct": needs_pct,
        "wants_pct": wants_pct,
        "saves_pct": saves_pct,
        "by_category": by_category,
        "category_detail": category_detail,
        "health_score": int(health_score),
    }


def _calculate_health_score(savings_rate, needs_pct, wants_pct, net_savings, income) -> float:
    score = 50.0  # baseline

    # Savings rate (up to +30)
    score += min(savings_rate, 30)

    # Needs under 50% (+10)
    if needs_pct <= 50:
        score += 10
    else:
        score -= (needs_pct - 50) * 0.5

    # Wants under 30% (+10)
    if wants_pct <= 30:
        score += 10
    else:
        score -= (wants_pct - 30) * 0.5

    # Positive net savings (+10)
    if net_savings > 0:
        score += min(net_savings / income * 20, 10)
    else:
        score += net_savings / income * 20  # penalty

    return max(0, min(100, score))


def _empty_budget(income: float) -> Dict:
    return {
        "total_expenses": 0, "spending_total": 0, "savings_total": 0,
        "net_savings": income, "savings_rate": 0,
        "needs": 0, "wants": 0, "saves": 0,
        "needs_pct": 0, "wants_pct": 0, "saves_pct": 0,
        "by_category": {}, "category_detail": [],
        "health_score": 50,
    }


def summarize_for_ai(expenses: List[Dict], income: float) -> str:
    """Generate a text summary of finances to inject into the AI system prompt."""
    budget = compute_budget(expenses, income)
    lines = [
        f"Monthly Income: ${income:,.0f}",
        f"Total Expenses: ${budget['total_expenses']:,.0f}",
        f"Net Savings: ${budget['net_savings']:,.0f}",
        f"Savings Rate: {budget['savings_rate']:.1f}%",
        f"Needs (50% goal): ${budget['needs']:,.0f} ({budget['needs_pct']:.1f}%)",
        f"Wants (30% goal): ${budget['wants']:,.0f} ({budget['wants_pct']:.1f}%)",
        f"Saves (20% goal): ${budget['saves']:,.0f} ({budget['saves_pct']:.1f}%)",
        "",
        "Expense Breakdown:",
    ]
    for item in budget["category_detail"]:
        flag = " ⚠️ OVER BENCHMARK" if item["over_budget"] else ""
        lines.append(f"  {item['icon']} {item['category']}: ${item['amount']:,.0f} ({item['percent']:.1f}%){flag}")

    return "\n".join(lines)
