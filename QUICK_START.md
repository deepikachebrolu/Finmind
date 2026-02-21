# Quick Reference Card

## 🚀 Start Here

```bash
cd d:\Documents\projects\finmind
streamlit run app.py
```

## 📁 File Locations

| What | Where |
|------|-------|
| Entry Point | `app.py` |
| Configuration | `src/config.py` |
| Utilities | `src/utils.py` |
| UI Styling | `src/ui/styles.py` |
| Navigation | `src/ui/sidebar.py` |
| Chat Page | `src/ui/pages/chat.py` |
| Dashboard | `src/ui/pages/dashboard.py` |
| Expenses | `src/ui/pages/expenses.py` |
| Budget Logic | `src/logic/budget.py` |
| AI Integration | `src/logic/ai_mentor.py` |

## 📚 Documentation Map

| Document | Purpose |
|----------|---------|
| **README.md** | Start here for overview |
| **SRC_STRUCTURE.md** | Understand architecture |
| **DEVELOPMENT.md** | Add new features |
| **MODULE_INDEX.md** | Find functions |
| **REFACTORING_SUMMARY.md** | See what changed |
| **STATUS_REPORT.md** | Project status |
| **DOCUMENTATION_INDEX.md** | Navigate docs |

## 🎯 Common Tasks

### Add a New Page
1. Create `src/ui/pages/new_page.py`
2. Implement `render_new_page_page()` function
3. Add to `app.py` routing

### Add Configuration
1. Edit `src/config.py`
2. Import in needed files
3. Use like: `from src.config import MY_SETTING`

### Add Utility Function
1. Add to `src/utils.py`
2. Import like: `from src.utils import my_function`

### Modify Budget Calculation
1. Edit `src/logic/budget.py`
2. Test with sample data
3. Verify in dashboard

## 🔗 Import Patterns

### In UI Components
```python
import streamlit as st
from src.config import EXPENSE_CATEGORIES
from src.logic.budget import compute_budget
from src.utils import format_currency
```

### In Logic Modules
```python
from typing import List, Dict
from src.config import BUDGET_BENCHMARKS
from src.utils import clamp
```

## ✅ Verification

All files compile:
```bash
python -m py_compile app.py src/config.py src/utils.py src/ui/styles.py src/ui/sidebar.py src/ui/pages/chat.py src/ui/pages/dashboard.py src/ui/pages/expenses.py src/logic/budget.py src/logic/ai_mentor.py
```

## 📊 Project Stats

- **11** Python source files (organized in src/)
- **7** Documentation files
- **50+** Configuration items
- **6** Utility functions
- **3** UI pages
- **2** Logic modules
- **100%** Code organization complete

## 🎓 Learning Path

1. Run app: `streamlit run app.py` ✅
2. Read: **SRC_STRUCTURE.md** (5 min)
3. Reference: **MODULE_INDEX.md** (as needed)
4. Follow: **DEVELOPMENT.md** (for new features)

## 🆘 Need Help?

- Architecture questions → SRC_STRUCTURE.md
- Code help → DEVELOPMENT.md
- Function lookup → MODULE_INDEX.md
- Changes made → REFACTORING_SUMMARY.md
- Overall status → STATUS_REPORT.md

---

**Everything is organized and ready to go!** ✅
