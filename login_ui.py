"""
Login, account creation, password change, and admin user management UI.

UI-only: uses symptom_explorer.auth for actual authentication/storage.
"""

from __future__ import annotations

from typing import Optional

from ..auth import (
    User,
    authenticate,
    create_user,
    delete_user,
    get_user_by_username,
    list_users,
    set_password,
    validate_password_rules,
)
from .common import pause, print_header, prompt, touch, check_inactivity


def startup_menu(db_path: str) -> Optional[User]:
    """Show login/create-account menu and return authenticated user or None."""
    while True:
        print_header("Symptom Explorer - Start")
        print("1) I already have an account (Login)")
        print("2) I don't have an account (Create one)")
        print("3) Exit")
        choice = prompt("Choose an option: ")

        if choice == "1":
            username = prompt("Username: ")
            password = prompt("Password: ")
            user = authenticate(username, password, db_path=db_path)
            if not user:
                print("Invalid username or password.")
                pause()
                continue
            return user

        elif choice == "2":
            print_header("Create Account")
            username = prompt("Choose a username: ").strip()
            if not username:
                print("Username cannot be empty.")
                pause()
                continue
            if get_user_by_username(username, db_path=db_path) is not None:
                print("That username already exists. Try logging in.")
                pause()
                continue

            print("\nPassword rules: at least 8 chars + lowercase + uppercase + digit + special char.")
            pw = prompt("Choose a password: ")
            ok, msg = validate_password_rules(pw)
            if not ok:
                print("Password rejected:", msg)
                pause()
                continue
            confirm = prompt("Confirm password: ")
            if confirm != pw:
                print("Passwords do not match.")
                pause()
                continue

            try:
                create_user(username, pw, is_admin=False, db_path=db_path)
                print("Account created successfully. Please log in now.")
            except Exception as e:
                print("Could not create account:", e)
            pause()

        elif choice == "3":
            return None
        else:
            print("Invalid selection.")
            pause()


def change_own_password(user: User, db_path: str) -> None:
    """Allow a logged-in user to change their own password."""
    print_header("Change Password")
    new_pw = prompt("Enter new password: ")
    ok, msg = validate_password_rules(new_pw)
    if not ok:
        print("Password rejected:", msg)
        pause()
        return
    confirm = prompt("Confirm new password: ")
    if confirm != new_pw:
        print("Passwords do not match.")
        pause()
        return
    try:
        set_password(user.username, new_pw, db_path=db_path)
        print("Password updated successfully.")
    except Exception as e:
        print("Could not update password:", e)
    pause()


def admin_menu(state: dict, db_path: str) -> None:
    """Admin-only menu for managing user accounts."""
    user: User = state["user"]
    if not user.is_admin:
        return

    while True:
        if check_inactivity(state):
            return
        print_header("Admin - Manage Users")
        print("1) List users")
        print("2) Add user")
        print("3) Delete user")
        print("4) Reset user password")
        print("5) Back")
        choice = prompt("Choose an option: ")
        touch(state)

        if choice == "1":
            users = list_users(db_path=db_path)
            print("")
            for uname, is_admin_flag in users:
                badge = "ADMIN" if is_admin_flag else "USER"
                print(f" - {uname} [{badge}]")
            pause()

        elif choice == "2":
            uname = prompt("New username: ")
            pw = prompt("New password (must follow rules): ")
            ok, msg = validate_password_rules(pw)
            if not ok:
                print("Password rejected:", msg)
                pause()
                continue
            adm = prompt("Is admin? (y/N): ").lower().startswith("y")
            try:
                create_user(uname, pw, is_admin=adm, db_path=db_path)
                print("User created.")
            except Exception as e:
                print(f"Could not create user: {e}")
            pause()

        elif choice == "3":
            uname = prompt("Username to delete: ")
            if uname == user.username:
                print("You cannot delete your own account while logged in.")
                pause()
                continue
            ok = delete_user(uname, db_path=db_path)
            print("Deleted." if ok else "No such user.")
            pause()

        elif choice == "4":
            uname = prompt("Username to reset password: ")
            pw = prompt("New password (must follow rules): ")
            try:
                ok = set_password(uname, pw, db_path=db_path)
                print("Password updated." if ok else "No such user.")
            except Exception as e:
                print("Password rejected:", e)
            pause()

        elif choice == "5":
            return
        else:
            print("Invalid selection.")
            pause()
