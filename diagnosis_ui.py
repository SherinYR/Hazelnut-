"""
Diagnosis (rule-based symptom checker) UI.
"""

from __future__ import annotations

import pandas as pd

from ..data_handler import DatasetInfo
from ..rules import parse_symptom_input, suggest_diagnosis
from .common import ask_float, pause, print_header, prompt, touch, check_inactivity


def diagnosis_menu(df: pd.DataFrame, info: DatasetInfo, state: dict) -> None:
    """Interactive menu for the educational rule-based symptom checker."""
    while True:
        if check_inactivity(state):
            return

        print_header("Rule-based Symptom Checker (Educational)")
        print("Type symptoms separated by commas.")
        print("Available symptom columns:")
        print("  " + ", ".join(sorted([c.lower() for c in info.symptom_cols])))
        print("\n1) Enter symptoms and get suggestion")
        print("2) Back")
        choice = prompt("Choose an option: ")
        touch(state)

        if choice == "1":
            threshold = ask_float("Symptom threshold (present if > threshold)", default=0.0)
            raw = prompt("Symptoms (comma-separated, e.g., fever,cough): ")
            user_symptoms = parse_symptom_input(raw)
            matched_count, suggestions, notes = suggest_diagnosis(
                df,
                diagnosis_col=info.diagnosis_col,
                symptom_cols=info.symptom_cols,
                user_symptoms=user_symptoms,
                threshold=threshold,
            )
            print("")
            for n in notes:
                print("NOTE:", n)

            if matched_count > 0:
                print(f"\nMatched records: {matched_count}")
                print("Suggested diagnoses (most frequent among matches):")
                for d, cnt in suggestions:
                    print(f" - {d}: {cnt}")
            pause()

        elif choice == "2":
            return

        else:
            print("Invalid selection.")
            pause()
