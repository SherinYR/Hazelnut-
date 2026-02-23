"""
Statistics UI: compute summary and optionally save it to a text file.
"""

from __future__ import annotations

import os
import pandas as pd

from ..data_handler import DatasetInfo
from ..stats import format_stats, run_all_stats
from .common import ask_float, ask_int, pause, print_header, prompt, touch, check_inactivity


def stats_menu(df: pd.DataFrame, info: DatasetInfo, state: dict) -> None:
    """Interactive statistics menu with save-to-text functionality."""
    while True:
        if check_inactivity(state):
            return

        print_header("Statistics")
        print("1) Compute full summary (user settings)")
        print("2) Save last summary to text file")
        print("3) Back")
        choice = prompt("Choose an option: ")
        touch(state)

        if choice == "1":
            top_n = ask_int("Top N for symptoms/diagnoses", default=10, min_v=1, max_v=200)
            threshold = ask_float("Symptom threshold (present if > threshold)", default=0.0)
            metric = prompt("Symptom metric: count or proportion? (C/P) [default C]: ").lower()
            symptom_metric = "proportion" if metric.startswith("p") else "count"

            results = run_all_stats(
                df,
                diagnosis_col=info.diagnosis_col,
                symptom_cols=info.symptom_cols,
                threshold=threshold,
                top_n=top_n,
                symptom_metric=symptom_metric,
            )
            text = format_stats(results, symptom_metric=symptom_metric)
            state["last_stats_text"] = text
            print("\n" + text)
            pause()

        elif choice == "2":
            text = state.get("last_stats_text")
            if not text:
                print("No summary computed yet. Run option 1 first.")
                pause()
                continue
            path = prompt("Enter output file path (e.g., stats_summary.txt): ")
            if not path:
                continue
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved to: {os.path.abspath(path)}")
            pause()

        elif choice == "3":
            return

        else:
            print("Invalid selection.")
            pause()
