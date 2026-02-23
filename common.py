#tuple[bool, Optional[str]]
#In older Python versions, this can cause errors because Python tries to 
#interpret type hints immediately when the file runs.
from __future__ import annotations

#used to track inactivity
import time

# Needed because a filename may or may not exist
from typing import Optional

#timeout threshold
INACTIVITY_SECONDS = 60 * 60  # 60 minutes

# Gets the current time in seconds to track user activity
def now() -> float:
    """Return current Unix time as float seconds."""
    return time.time()

# Updates the user's last activity time
def touch(state: dict) -> None:
    """Update last activity timestamp in state."""
    state["last_activity"] = now()

# Checks if the user has been inactive for too long
def check_inactivity(state: dict) -> bool:
    """Return True if inactivity exceeds timeout."""
    last = state.get("last_activity", now())
    return (now() - last) > INACTIVITY_SECONDS

## Prompts the user and returns cleaned input
def prompt(msg: str) -> str:
    """Read a user input line and strip it."""
    return input(msg).strip()

# Pauses the program until Enter is pressed
def pause() -> None:
    """Pause until user presses Enter."""
    input("\nPress Enter to continue...")

# Prints a formatted section title
def print_header(title: str) -> None:
    """Print a section header with separators for readability."""
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

# Sends user's show/save choice to the plotting functions
def choose_show_or_save() -> tuple[bool, Optional[str]]:
    """Ask whether to show a plot or save it to a PNG."""
    choice = prompt("Show on screen or save to PNG? (S=show / P=png): ").lower()
    if choice.startswith("p"):
        path = prompt("Enter PNG file path (e.g., output.png): ")
        return False, path or None
    return True, None

# Reusable safe integer input with default and limits
def ask_int(msg: str, default: int, min_v: int = 1, max_v: int = 10_000) -> int:
    """Prompt for an integer with clamping and a default fallback."""
    raw = prompt(f"{msg} [default {default}]: ")
    if not raw:
        return default
    try:
        v = int(raw)
        return max(min_v, min(max_v, v))
    except ValueError:
        print("Invalid number. Using default.")
        return default

#collects a decimal number from the user.
def ask_float(msg: str, default: float, min_v: float = -1e9, max_v: float = 1e9) -> float:
    """Prompt for a float with clamping and a default fallback."""
    raw = prompt(f"{msg} [default {default}]: ")
    if not raw:
        return default
    try:
        v = float(raw)
        return max(min_v, min(max_v, v))
    except ValueError:
        print("Invalid number. Using default.")
        return default
