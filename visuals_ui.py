"""
Visualization UI: bar charts and heatmaps.
"""

from __future__ import annotations

import os
import pandas as pd

from ..data_handler import DatasetInfo
from ..visuals import diagnosis_plot, symptom_diagnosis_heatmap, symptom_plot
from .common import ask_float, ask_int, choose_show_or_save, pause, print_header, prompt, touch, check_inactivity


def visuals_menu(df: pd.DataFrame, info: DatasetInfo, state: dict) -> None:
    """Interactive visualization menu for bar charts and heatmaps."""
    while True:
        if check_inactivity(state):
            return

        print_header("Visualizations (User-driven)")
        print("1) Bar chart: top symptoms (choose settings)")
        print("2) Bar chart: top diagnoses (choose settings)")
        print("3) Heatmap: symptom vs diagnosis (choose settings)")
        print("4) Back")
        choice = prompt("Choose an option: ")
        touch(state)

        if choice == "1":
            top_n = ask_int("Top N symptoms", default=10, min_v=1, max_v=max(1, len(info.symptom_cols)))
            threshold = ask_float("Symptom threshold (present if > threshold)", default=0.0)
            metric = prompt("Metric: count or proportion? (C/P) [default C]: ").lower()
            metric = "proportion" if metric.startswith("p") else "count"
            show, save_path = choose_show_or_save()
            symptom_plot(df, info.symptom_cols, threshold, top_n, metric, show, save_path)
            if save_path:
                print(f"Saved PNG to: {os.path.abspath(save_path)}")
            pause()

        elif choice == "2":
            top_n = ask_int("Top N diagnoses", default=10, min_v=1, max_v=200)
            show, save_path = choose_show_or_save()
            diagnosis_plot(df, info.diagnosis_col, top_n, show, save_path)
            if save_path:
                print(f"Saved PNG to: {os.path.abspath(save_path)}")
            pause()

        elif choice == "3":
            top_symptoms = ask_int("Top symptoms in heatmap (columns)", default=10, min_v=2, max_v=max(2, len(info.symptom_cols)))
            top_diagnoses = ask_int("Top diagnoses in heatmap (rows)", default=10, min_v=2, max_v=200)
            threshold = ask_float("Symptom threshold (present if > threshold)", default=0.0)
            show, save_path = choose_show_or_save()
            symptom_diagnosis_heatmap(
                df, info.diagnosis_col, info.symptom_cols, threshold, top_symptoms, top_diagnoses, show, save_path
            )
            if save_path:
                print(f"Saved PNG to: {os.path.abspath(save_path)}")
            pause()

        elif choice == "4":
            return

        else:
            print("Invalid selection.")
            pause()
