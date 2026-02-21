# FinMind Development Guide

## Project Structure Overview

```
finmind/
├── app.py                 # Main entry point
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project overview
├── SRC_STRUCTURE.md      # Architecture documentation
├── DEVELOPMENT.md        # This file
│
└── src/
    ├── __init__.py
    ├── config.py         # Centralized configuration & constants
    ├── utils.py          # Utility functions
    │
    ├── ui/               # User interface layer
    │   ├── __init__.py
    │   ├── styles.py     # CSS theming & styling
    │   ├── sidebar.py    # Navigation & sidebar
    │   └── pages/
    │       ├── __init__.py
    │       ├── chat.py   # AI Mentor Chat
    │       ├── dashboard.py # Financial Dashboard
    │       └── expenses.py  # Expense Management
    │
    └── logic/            # Business logic layer
        ├── __init__.py
        ├── budget.py     # Budget calculations
        └── ai_mentor.py  # OpenAI integration
```

## Adding a New Feature

### 1. Add Configuration
If your feature needs constants, add them to `src/config.py`:

```python
# src/config.py
MY_FEATURE_SETTING = "value"
MY_FEATURE_COLORS = {"color1": "#hex", "color2": "#hex"}
```

### 2. Add Business Logic
Create or modify files in `src/logic/`:

```python
# src/logic/my_feature.py
from src.config import MY_FEATURE_SETTING

def compute_my_feature(data):
    """Pure function - no Streamlit code here."""
    return result
```

### 3. Add UI Component
Create a render function in `src/ui/pages/` or `src/ui/`:

```python
# src/ui/pages/my_feature.py
import streamlit as st
from src.logic.my_feature import compute_my_feature

def render_my_feature_page():
    """Streamlit UI for my feature."""
    st.title("My Feature")
    # Use compute_my_feature() and render UI
```

### 4. Add to App Router
Update `app.py` to include your new page:

```python
# app.py
elif page == "my_feature":
    render_my_feature_page()
```

## Coding Standards

### Imports Organization
```python
# Standard library first
import re
from typing import List, Dict

# Third-party
import streamlit as st

# Local imports
from src.config import COLORS
from src.logic.budget import compute_budget
from src.utils import format_currency
```

### Function Documentation
```python
def my_function(param1: str, param2: int) -> Dict[str, float]:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    pass
```

### Configuration Best Practices
- All magic strings/numbers go in `src/config.py`
- Import constants directly: `from src.config import MY_CONSTANT`
- Avoid hardcoding colors, categories, or thresholds

### Utility Functions
- Common helpers go in `src/utils.py`
- Examples: formatting, validation, conversions
- Keep them pure functions (no Streamlit side effects)

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run with specific port
streamlit run app.py --server.port 8501
```

## Testing

### Manual Testing
1. Test each page individually
2. Check state persistence across page navigation
3. Verify calculations with known values
4. Test edge cases (empty data, zero values, large numbers)

### Future: Unit Testing
```bash
# Once pytest is added
pytest tests/
pytest tests/logic/test_budget.py -v
```

## Common Tasks

### Adding a New Expense Category
1. Add to `EXPENSE_CATEGORIES` in `src/config.py`
2. Add icon in `CATEGORY_ICONS`
3. Add color in `CATEGORY_COLORS`
4. Add benchmark in `BUDGET_BENCHMARKS`
5. Update `BUDGET_NEEDS_CATEGORIES` or `BUDGET_WANTS_CATEGORIES` if needed

### Updating Color Theme
Edit `COLORS` and `CATEGORY_COLORS` in `src/config.py`, then update references in `src/ui/styles.py`.

### Modifying Budget Calculation
1. Edit the algorithm in `src/logic/budget.py`
2. Test with `DEFAULT_EXPENSES` data
3. Verify health score calculation reflects changes
4. Update documentation in comments

## Performance Tips

- Use `st.cache_data` for expensive calculations
- Pre-calculate category summaries where possible
- Lazy-load charts only when tab is active
- Use session state to avoid recalculations

## Debugging

### Enable Streamlit Debugging
```bash
streamlit run app.py --logger.level=debug
```

### Print Debug Info
```python
import streamlit as st
st.write("Debug:", variable)  # Shows in browser
print("Debug:", variable)       # Shows in terminal
```

## Deployment

### Streamlit Cloud (Recommended)
```bash
git push  # to your repo
# Then deploy via https://share.streamlit.io
```

### Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## Contributing Guidelines

1. Create a new branch: `git checkout -b feature/my-feature`
2. Make changes following coding standards
3. Test thoroughly
4. Commit with clear messages: `git commit -m "Add my feature"`
5. Push and create a pull request

## Troubleshooting

### Import Errors
- Ensure you're running from the project root directory
- Check that all `__init__.py` files exist in packages
- Verify no circular imports between modules

### Streamlit Rerun Issues
- Avoid modifying `st.session_state` during render
- Use `st.rerun()` after state changes
- Understand Streamlit's reactive execution model

### Performance Issues
- Check for unnecessary re-renders
- Profile with `--client.toolbarMode="minimal"`
- Look for N+1 query patterns in loops

## Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Python Typing Docs](https://docs.python.org/3/library/typing.html)
- [OpenAI API Docs](https://platform.openai.com/docs/)
