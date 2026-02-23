"""
Static info/help screens.
"""

from __future__ import annotations

from ..data_handler import DatasetInfo
from .common import print_header


def about_screen(info: DatasetInfo) -> None:
    """Display program description, disclaimers, and navigation tips."""
    print_header("Welcome to Symptom Explorer")
    print(
        f"""
What this program is:
- An educational tool that explores a synthetic medical symptom dataset.
- It can summarize the most common symptoms and diagnoses, generate plots, and run a simple rule-based matcher.

What it is NOT:
- It is NOT medical advice, diagnosis, or treatment guidance.

How it works:
- The dataset contains a diagnosis column ("{info.diagnosis_col}") and symptom indicator columns (e.g., fever, cough...).
- Statistics count how often symptoms appear (value > threshold).
- Visualizations are user-driven: you choose top-N, threshold, and whether to show or save plots.

Navigation:
- Choose menu numbers and press Enter.
- You will be auto-logged out after 60 minutes of inactivity.
"""
    )


def help_page() -> None:
    """Print a help page describing the main features and security details."""
    print_header("Help: Symptom Explorer")
    print(
        """
Main features:
1) Explore dataset
2) Statistics
3) Visualizations
4) Symptom Checker (educational rule-based)

User accounts:
- At startup you can log in or create an account (SQLite).

Security:
- Passwords stored as salted PBKDF2-HMAC-SHA256 hashes (not plaintext).
- Auto-logout after 60 minutes of inactivity.
"""
    )
