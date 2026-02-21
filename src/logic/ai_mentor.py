"""
OpenAI GPT integration for FinMind.
Handles API calls, system prompt building, and error handling.
"""

from typing import List, Dict
from src.logic.budget import summarize_for_ai

BASE_SYSTEM_PROMPT = """You are FinMind, a world-class AI personal finance mentor with the expertise of a CFP, CPA, and wealth manager combined.

## Your Mission
Help users achieve financial freedom through personalized, data-driven, actionable advice based on their ACTUAL expense data shown below.

## Expertise Areas
- Budgeting & cash flow (50/30/20, zero-based budgeting)
- Debt elimination (avalanche, snowball)
- Investing (index funds, ETFs, DCA, compound interest)
- Retirement planning (401k, IRA, FIRE math)
- Emergency fund strategy
- Tax optimization basics
- Credit improvement

## Response Style
- Start with the **direct insight** — no fluff
- Include **specific numbers** and calculations from the user's data
- Use bullet points for action steps
- End with 2–3 concrete **next steps the user can take TODAY**
- Tone: warm, encouraging, non-judgmental
- Use emojis strategically: 💡 insight, 📊 data, ⚡ action, ⚠️ warning, ✅ good news
- Keep responses focused and scannable

## Guardrails
- Recommend consulting a CFP/CPA for complex tax/legal matters
- Never guarantee investment returns
- State assumptions clearly

## User's Current Financial Data:
{financial_summary}"""


def build_system_prompt(expenses: list, income: float) -> str:
    summary = summarize_for_ai(expenses, income)
    return BASE_SYSTEM_PROMPT.format(financial_summary=summary)


def chat_with_gpt(
    api_key: str,
    user_message: str,
    history: List[Dict],
    expenses: list,
    income: float,
) -> str:
    """Send a message to GPT-4o and return the response."""
    try:
        import openai
    except ImportError:
        return "⚠️ **OpenAI package not installed.** Run: `pip install openai`"

    if not api_key:
        return get_demo_response(user_message, expenses, income)

    client = openai.OpenAI(api_key=api_key)

    system_prompt = build_system_prompt(expenses, income)

    messages = [{"role": "system", "content": system_prompt}]
    # Rolling window — last 16 messages
    messages.extend(history[-16:])
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content

    except openai.AuthenticationError:
        return "⚠️ **Invalid API key.** Please check your key in the sidebar."
    except openai.RateLimitError:
        return "⚠️ **Rate limit reached.** Please wait a moment and try again."
    except openai.APIConnectionError:
        return "⚠️ **Connection error.** Check your internet and try again."
    except Exception as e:
        return f"⚠️ **Error:** {str(e)}"


def get_demo_response(message: str, expenses: list, income: float) -> str:
    """Smart demo responses when no API key is set."""
    from src.logic.budget import compute_budget
    budget = compute_budget(expenses, income)
    m = message.lower()

    if any(w in m for w in ["budget", "spend", "50/30", "allocation"]):
        return f"""💡 **Your Budget Analysis — 50/30/20 Framework**

Based on your **${income:,.0f}/month** income:

📊 **Current Breakdown:**
- 🏠 **Needs** (goal ≤50%): ${budget['needs']:,.0f} — {budget['needs_pct']:.1f}% {"✅" if budget['needs_pct'] <= 50 else "⚠️ Over target"}
- 🎉 **Wants** (goal ≤30%): ${budget['wants']:,.0f} — {budget['wants_pct']:.1f}% {"✅" if budget['wants_pct'] <= 30 else "⚠️ Over target"}
- 💰 **Savings** (goal ≥20%): ${budget['saves']:,.0f} — {budget['saves_pct']:.1f}% {"✅" if budget['saves_pct'] >= 20 else "⚠️ Below target"}

Net cash left over: **${budget['net_savings']:,.0f}/month**

⚡ **Top 3 Actions:**
1. {"Reduce wants spending by ~$" + str(int(budget['wants'] - income*0.3)) if budget['wants_pct'] > 30 else "Wants spending is on target! 🎉"}
2. {"Increase savings to hit the 20% mark — you need $" + str(int(income*0.2 - budget['saves'])) + "/mo more" if budget['saves_pct'] < 20 else "Savings rate is solid ✅"}
3. Set up automatic transfers on payday so savings happen before spending

> 💡 *Add your OpenAI API key for personalized, conversational analysis!*"""

    if any(w in m for w in ["debt", "loan", "credit card", "pay off"]):
        debt_total = budget["by_category"].get("Debt", 0)
        return f"""⚡ **Debt Payoff Strategy**

You're currently allocating **${debt_total:,.0f}/month** toward debt repayment.

**Two proven strategies:**

🏔️ **Debt Avalanche** *(mathematically optimal)*
→ Attack highest APR first. Saves the most interest. Best if you're numbers-motivated.

⛄ **Debt Snowball** *(psychologically powerful)*  
→ Attack smallest balance first. Quick wins build momentum. Higher completion rates.

📊 **Quick math:** At ${debt_total:,.0f}/month extra payments on a $15K loan at 7% APR:
→ Paid off in ~26 months · Interest saved: ~$1,400

⚡ **Next Steps:**
1. List all debts with balance + APR (go to Expenses tab)
2. Apply any windfalls (tax refund, bonus) directly to top debt
3. Consider balance transfer to 0% APR card for CC debt

> 💡 *Add your OpenAI API key for a personalized payoff schedule!*"""

    # Default response
    return f"""💡 **FinMind Analysis**

Based on your current financial snapshot:
- **Monthly Income:** ${income:,.0f}
- **Total Spending:** ${budget['spending_total']:,.0f}
- **Savings Rate:** {budget['savings_rate']:.1f}%
- **Health Score:** {budget['health_score']}/100

{'✅ Your savings rate is above the 20% target — excellent discipline!' if budget['savings_rate'] >= 20 else '⚠️ Your savings rate is below 20% — small adjustments can make a big difference.'}

I can help you with:
- 📊 Budget optimization and 50/30/20 analysis
- 💳 Debt payoff strategies  
- 📈 Investment allocation for your income level
- 🎯 Goal planning (emergency fund, house, retirement)

What would you like to explore? Or go to the **Expenses tab** to update your numbers first!

> 💡 *Add your OpenAI API key in the sidebar for live, personalized GPT-4o responses.*"""
