# FinMind Project Structure - Refactored

## Overview
The FinMind application has been reorganized into a clean, modular `src/` directory structure for better maintainability and scalability.

## Directory Structure

```
finmind/
├── app.py                          # Main Streamlit entry point
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── ui/                         # User interface layer
│   │   ├── __init__.py
│   │   ├── styles.py               # Global CSS/theming
│   │   ├── sidebar.py              # Sidebar navigation & snapshot
│   │   └── pages/                  # Page components
│   │       ├── __init__.py
│   │       ├── chat.py             # AI Mentor Chat interface
│   │       ├── dashboard.py        # Financial Dashboard & analytics
│   │       └── expenses.py         # Expenses & Budget management
│   │
│   └── logic/                      # Business logic layer
│       ├── __init__.py
│       ├── budget.py               # Budget calculations & analysis
│       └── ai_mentor.py            # OpenAI GPT integration
│
└── [Old root-level files deprecated]
    ├── chat.py                     → src/ui/pages/chat.py
    ├── sidebar.py                  → src/ui/sidebar.py
    ├── dashboard.py                → src/ui/pages/dashboard.py
    ├── expenses.py                 → src/ui/pages/expenses.py
    ├── budget.py                   → src/logic/budget.py
    └── ai_mentor.py                → src/logic/ai_mentor.py
```

## Module Breakdown

### UI Layer (`src/ui/`)
- **styles.py**: Central CSS theming with dark mode, custom fonts (Syne, DM Mono), color palette
- **sidebar.py**: Navigation menu, financial snapshot, API key management, health score visualization
- **pages/chat.py**: AI chat interface with quick prompts, message history, spinner feedback
- **pages/dashboard.py**: KPI cards, Plotly charts (pie chart, bar chart), category breakdown, AI insights
- **pages/expenses.py**: Income input, expense CRUD (Create, Read, Update, Delete), 50/30/20 breakdown, filtering

### Logic Layer (`src/logic/`)
- **budget.py**: Pure Python budget calculations (no Streamlit dependency)
  - `compute_budget()`: Main function returning comprehensive budget breakdown
  - `CATEGORY_COLORS`, `CATEGORY_ICONS`, `BENCHMARKS`: Config constants
  - `summarize_for_ai()`: Generates text summary for GPT system prompt
  
- **ai_mentor.py**: OpenAI integration
  - `build_system_prompt()`: Creates contextualized GPT prompt
  - `chat_with_gpt()`: API call handler with error handling
  - `get_demo_response()`: Demo responses when API key is missing

### Entry Point (`app.py`)
- Streamlit page config setup
- Session state initialization
- Page routing (Chat, Expenses, Dashboard)

## Benefits of This Structure

1. **Separation of Concerns**
   - UI logic isolated from business logic
   - Pure functions in `logic/` can be unit tested independently
   - Streamlit code only in `ui/`

2. **Scalability**
   - Easy to add new pages: Create new file in `src/ui/pages/`
   - Easy to add new features: Extend functions in `src/logic/`
   - Shared utilities can be added to respective `__init__.py` files

3. **Reusability**
   - Budget calculations can be used in other contexts (CLI, API)
   - Components can be imported and tested in isolation

4. **Maintainability**
   - Clear file organization makes code navigation easier
   - Import paths are explicit and predictable
   - Each module has a single responsibility

## Import Examples

```python
# From app.py
from src.ui.styles import inject_css
from src.ui.sidebar import render_sidebar
from src.ui.pages.chat import render_chat_page

# From src/ui/pages/expenses.py
from src.logic.budget import compute_budget, CATEGORY_COLORS, CATEGORY_ICONS

# From src/logic/ai_mentor.py
from src.logic.budget import summarize_for_ai
```

## Migration Notes

- Old root-level files (`chat.py`, `budget.py`, etc.) can be deleted after verifying the refactored version works
- All imports have been updated to use the new `src/` paths
- No functional changes were made—purely structural reorganization
