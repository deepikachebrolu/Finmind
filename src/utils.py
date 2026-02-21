"""
Utility functions for FinMind application.
"""

import re


def hex_to_rgb(hex_color: str) -> str:
    """
    Convert hex color to RGB string format.
    
    Args:
        hex_color: Color in hex format (e.g., "#00d4aa")
    
    Returns:
        RGB string format (e.g., "0,212,170")
    """
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return "136,153,170"  # Default fallback color
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"{r},{g},{b}"
    except ValueError:
        return "136,153,170"


def format_currency(amount: float) -> str:
    """Format amount as currency with thousands separator."""
    return f"${amount:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage string."""
    return f"{value:.{decimals}f}%"


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max."""
    return max(min_val, min(value, max_val))


def get_health_score_label(score: int) -> str:
    """Get descriptive label for health score."""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Needs Work"


def get_health_score_color(score: int) -> str:
    """Get color for health score based on value."""
    if score >= 70:
        return "#00d4aa"  # Cyan (good)
    elif score >= 40:
        return "#ff6b35"  # Orange (fair)
    else:
        return "#ff4757"  # Red (poor)
