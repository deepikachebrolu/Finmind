# FinMind Module Index

## Quick Reference Guide

### Entry Point
- **`app.py`** - Main Streamlit application, page routing, session state init

### Configuration (`src/`)
- **`config.py`** - All constants, colors, categories, defaults, settings
- **`utils.py`** - Helper functions (formatting, validation, color conversion)

### UI Layer (`src/ui/`)

#### Core Styling
- **`styles.py`** - Global CSS, themes, fonts, animations

#### Navigation
- **`sidebar.py`** - Sidebar navigation, financial snapshot widget, health score ring, API key input

#### Pages (`src/ui/pages/`)
- **`chat.py`** - AI Mentor chat interface with quick prompts, message history
- **`expenses.py`** - Expense CRUD, income input, 50/30/20 breakdown, category view
- **`dashboard.py`** - KPI cards, Plotly visualizations, category breakdown, AI insights

### Logic Layer (`src/logic/`)

#### Budget Engine
- **`budget.py`** - Budget calculations
  - `compute_budget()` - Main calculation function
  - `summarize_for_ai()` - Text summary for GPT context
  - Constants: `CATEGORY_COLORS`, `CATEGORY_ICONS` (re-exported from config)

#### AI Integration
- **`ai_mentor.py`** - OpenAI integration
  - `build_system_prompt()` - Create contextualized GPT prompt
  - `chat_with_gpt()` - API call with error handling
  - `get_demo_response()` - Fallback responses without API key

---

## Import Patterns

### In UI Components
```python
import streamlit as st
from src.config import EXPENSE_CATEGORIES, COLORS
from src.logic.budget import compute_budget
from src.utils import format_currency, hex_to_rgb
```

### In Logic Modules
```python
from typing import List, Dict, Any
from src.config import BUDGET_BENCHMARKS, DEFAULT_EXPENSES
from src.utils import clamp, get_health_score_label
```

---

## Key Functions

### Budget Calculation
```python
from src.logic.budget import compute_budget
budget = compute_budget(expenses, income)
# Returns: {
#   "total_expenses": float,
#   "net_savings": float,
#   "savings_rate": float,
#   "needs": float, "wants": float, "saves": float,
#   "needs_pct": float, "wants_pct": float, "saves_pct": float,
#   "category_detail": List[Dict],
#   "health_score": int,
#   ...
# }
```

### AI Chat
```python
from src.logic.ai_mentor import chat_with_gpt
response = chat_with_gpt(
    api_key="sk-...",
    user_message="Analyze my budget",
    history=[],
    expenses=expenses_list,
    income=6400.0
)
```

### Formatting Utilities
```python
from src.utils import (
    format_currency,        # "$1,234.56"
    format_percentage,      # "25.3%"
    hex_to_rgb,            # "0,212,170" from "#00d4aa"
    get_health_score_label, # "Good" / "Fair" / etc
    clamp                  # Constrain values
)
```

---

## Configuration Access

### Common Imports
```python
from src.config import (
    # App settings
    APP_NAME, APP_VERSION,
    STREAMLIT_PAGE_CONFIG,
    
    # Financial
    EXPENSE_CATEGORIES, EXPENSE_TYPES, MONTHS,
    BUDGET_BENCHMARKS,
    BUDGET_NEEDS_CATEGORIES, BUDGET_WANTS_CATEGORIES,
    
    # Colors
    COLORS, CATEGORY_COLORS, CATEGORY_ICONS,
    
    # AI
    AI_MODEL, AI_TEMPERATURE, AI_MAX_TOKENS,
    
    # Defaults
    DEFAULT_INCOME, DEFAULT_EXPENSES, DEFAULT_NEXT_ID,
)
```

---

## File Organization by Concern

### To Add/Modify Expense Categories
→ Edit `src/config.py` (EXPENSE_CATEGORIES, icons, colors, benchmarks)

### To Change Budget Algorithm
→ Edit `src/logic/budget.py` (compute_budget function)

### To Adjust UI Styling
→ Edit `src/ui/styles.py` (CSS), `src/config.py` (colors)

### To Add New AI Features
→ Edit `src/logic/ai_mentor.py` (new functions, system prompt)

### To Add New Page
→ Create `src/ui/pages/new_page.py`, update `app.py` routing

### To Add Utility Function
→ Add to `src/utils.py`, export from there

---

## Data Flow

```
app.py (state init)
  ↓
Session State (st.session_state)
  ├─→ expenses: List[Dict]
  ├─→ income: float
  ├─→ messages: List[Dict]
  ├─→ page: str
  └─→ api_key: str

User Interaction
  ↓
UI Component (src/ui/pages/*.py)
  ↓
Logic Function (src/logic/*.py)
  ↓
Result displayed / state updated
```

---

## Testing Checklist

- [ ] All imports resolve without errors
- [ ] Budget calculations match manual verification
- [ ] UI renders without Streamlit errors
- [ ] Navigation between pages works
- [ ] Session state persists across reruns
- [ ] API calls handled gracefully (no key, rate limit, etc)
- [ ] Empty data scenarios handled
- [ ] Large numbers display correctly

