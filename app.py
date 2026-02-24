
from __future__ import annotations

import os
from typing import Optional

from .auth import DEFAULT_DB_PATH, init_db
from .data_handler import load_dataset
from .ui.common import check_inactivity, pause, print_header, prompt, now, touch
from .ui.info_ui import about_screen, help_page
from .ui.login_ui import startup_menu, change_own_password, admin_menu
from .ui.explore_ui import explore_menu
from .ui.stats_ui import stats_menu
from .ui.visuals_ui import visuals_menu
from .ui.diagnosis_ui import diagnosis_menu

# Main function that runs the app using the dataset and database
def run_app(csv_path: str, db_path: Optional[str] = None) -> None:
    """Run the application end-to-end."""
    #Use custom DB path OR default one.
    db_path = os.path.abspath(db_path) if db_path else DEFAULT_DB_PATH
    init_db(db_path)
    
     #This part tries to load the dataset and handles failure.
    try:
        df, info = load_dataset(csv_path)
    except Exception as e:
        print(f"ERROR: Could not load dataset: {e}")
        return

    user = startup_menu(db_path)
    if user is None:
        print("Goodbye.")
        return

    about_screen(info)
    state = {"user": user, "last_activity": now()}
    pause()

    while True:
        if check_inactivity(state):
            print("\n[Auto-logout] You were logged out after 60 minutes of inactivity.")
            return

        user = state["user"]
        print_header(f"Main Menu (User: {user.username} | admin={user.is_admin})")
        print("1) Explore dataset")
        print("2) Statistics")
        print("3) Visualizations")
        print("4) Symptom checker (rule-based)")
        print("5) Help")
        print("6) Change my password")
        if user.is_admin:
            print("7) Admin: manage users")
            print("8) Logout")
        else:
            print("7) Logout")

        choice = prompt("Choose an option: ")
        touch(state)

        if choice == "1":
            explore_menu(df, info, state)
        elif choice == "2":
            stats_menu(df, info, state)
        elif choice == "3":
            visuals_menu(df, info, state)
        elif choice == "4":
            diagnosis_menu(df, info, state)
        elif choice == "5":
            help_page()
            pause()
        elif choice == "6":
            change_own_password(user, db_path=db_path)
        elif choice == "7" and user.is_admin:
            admin_menu(state, db_path=db_path)
        elif (choice == "7" and not user.is_admin) or (choice == "8" and user.is_admin):
            print("Logging out...")
            return
        else:
            print("Invalid selection.")
            pause()
