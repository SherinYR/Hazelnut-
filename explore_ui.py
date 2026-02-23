"""
Dataset exploration UI (columns, preview, filter by diagnosis).
"""

from __future__ import annotations

#Used to ignore blank diagnoses
import numpy as np

# Used to work with the dataset as a table
import pandas as pd

# Provides which column is the diagnosis and which are symptoms
#data handler loads the dataset and turns it into a table (DataFrame).
from ..data_handler import DatasetInfo

# Import shared UI helper functions
"pause → wait for user"
"print_header → show section title"
"prompt → read input"
"touch → update activity time"
"check_inactivity → detect timeout"

from .common import pause, print_header, prompt, touch, check_inactivity

# df: the dataset table
# info: tells which column is diagnosis and symptoms
# state: stores session activity info
#none= This function does not return anything.
def explore_menu(df: pd.DataFrame, info: DatasetInfo, state: dict) -> None:
    """Interactive dataset exploration menu."""
    while True:
        if check_inactivity(state):
            return

        print_header("Explore Dataset")
        print("1) Show dataset shape and columns")
        print("2) Preview first 10 rows")
        print("3) Filter by diagnosis")
        print("4) Back")
        choice = prompt("Choose an option: ")
        touch(state)

        if choice == "1":
            print(f"\nRows: {df.shape[0]}  Columns: {df.shape[1]}")
            print("\nColumns:")
            for c in df.columns:
                tag = ""
                if c == info.diagnosis_col:
                    tag = " (diagnosis)"
                elif c in info.symptom_cols:
                    tag = " (symptom)"
                print(f" - {c}{tag}")
            pause()

        elif choice == "2":
            print("\n" + df.head(10).to_string(index=False)) #index false is for row numbers
            pause()

        elif choice == "3":
            diags = (
                df[info.diagnosis_col]
                .astype(str) #Convert all values to text.
                .str.strip() 
                .replace("", np.nan) #If a value is empty text:treat as missing
                .dropna() #Remove missing values.
                .value_counts() #Count how many times each diagnosis appears.
            )

            if diags.empty:
                print("No diagnosis values found in the dataset.")
                pause() #Wait so the message can be read.
                continue #Go back to the start of the loop.

            print("\nAvailable diagnoses (with counts):")
            diag_names = list(diags.index)
            for i, name in enumerate(diag_names, start=1):
                print(f" {i}) {name}  (n={int(diags[name])})")

            raw = prompt("\nChoose a diagnosis by number or type the exact name: ").strip()
            if not raw:
                continue

            if raw.isdigit():
                idx = int(raw)
                if 1 <= idx <= len(diag_names):
                    selected = diag_names[idx - 1]
                else:
                    print("Invalid number.")
                    pause()
                    continue
            else:
                match = [d for d in diag_names if d.lower() == raw.lower()] #This compares names ignoring case.
                if match:
                    selected = match[0]
                else:
                    print("Diagnosis not recognized. Please choose from the list.")
                    pause()
                    continue

            sub = df[df[info.diagnosis_col].astype(str).str.strip().str.lower() == selected.lower()]
            print(f"\nSelected: {selected}")
            print(f"Matched rows: {len(sub)}")
            print(sub.head(10).to_string(index=False))
            pause()

        elif choice == "4":
            return

        else:
            print("Invalid selection.")
            pause()
