"""
Visualization helpers for Symptom Explorer.

Uses matplotlib to generate:
- Horizontal bar charts
- Heatmaps

Plots can be shown interactively or saved as PNG files.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .stats import compute_top_symptoms


def plot_horizontal_bar(
    labels: List[str],
    values: List[float],
    title: str,
    xlabel: str,
    show: bool = True,
    save_path: Optional[str] = None,
    value_format: str = "{:.0f}",
) -> None:
    """Plot a horizontal bar chart; optionally show and/or save to disk."""
    plt.figure(figsize=(10, max(4, 0.5 * len(labels) + 1)))
    y = np.arange(len(labels))
    plt.barh(y, values)
    plt.yticks(y, labels)
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.xlabel(xlabel)

    for i, v in enumerate(values):
        plt.text(v, i, "  " + value_format.format(v), va="center")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=220)
    if show:
        plt.show()
    plt.close()


def symptom_plot(
    df: pd.DataFrame,
    symptom_cols: List[str],
    threshold: float,
    top_n: int,
    metric: str,
    show: bool,
    save_path: Optional[str],
) -> None:
    """Generate a top-symptoms bar chart from user-selected settings."""
    items = compute_top_symptoms(df, symptom_cols, threshold=threshold, top_n=top_n, metric=metric)
    labels = [x[0] for x in items]
    values = [x[1] for x in items]
    if metric == "proportion":
        plot_horizontal_bar(
            labels,
            values,
            title=f"Top {len(labels)} Symptoms (proportion of records, > {threshold})",
            xlabel="Proportion",
            show=show,
            save_path=save_path,
            value_format="{:.3f}",
        )
    else:
        plot_horizontal_bar(
            labels,
            values,
            title=f"Top {len(labels)} Symptoms (count of records, > {threshold})",
            xlabel="Count",
            show=show,
            save_path=save_path,
            value_format="{:.0f}",
        )


def diagnosis_plot(
    df: pd.DataFrame,
    diagnosis_col: str,
    top_n: int,
    show: bool,
    save_path: Optional[str],
) -> None:
    """Generate a top-diagnoses bar chart."""
    vc = df[diagnosis_col].astype(str).value_counts(dropna=False)
    items = vc.head(top_n)
    labels = list(items.index)
    values = [float(v) for v in items.values]
    plot_horizontal_bar(
        labels,
        values,
        title=f"Top {len(labels)} Diagnoses (frequency)",
        xlabel="Count",
        show=show,
        save_path=save_path,
        value_format="{:.0f}",
    )


def symptom_diagnosis_heatmap(
    df: pd.DataFrame,
    diagnosis_col: str,
    symptom_cols: List[str],
    threshold: float,
    top_symptoms: int,
    top_diagnoses: int,
    show: bool,
    save_path: Optional[str],
) -> None:
    """Generate a symptom–diagnosis heatmap of symptom proportions per diagnosis."""
    diag_top = df[diagnosis_col].astype(str).value_counts().head(top_diagnoses).index.tolist()

    sym_counts = []
    for c in symptom_cols:
        s = pd.to_numeric(df[c], errors="coerce").fillna(0)
        sym_counts.append((c, int((s > threshold).sum())))
    sym_counts.sort(key=lambda x: x[1], reverse=True)
    sym_top = [c for c, _ in sym_counts[:top_symptoms]]

    sub = df[df[diagnosis_col].astype(str).isin(diag_top)].copy()
    mat = np.zeros((len(diag_top), len(sym_top)), dtype=float)

    for i, d in enumerate(diag_top):
        group = sub[sub[diagnosis_col].astype(str) == d]
        for j, sname in enumerate(sym_top):
            s = pd.to_numeric(group[sname], errors="coerce").fillna(0)
            mat[i, j] = float((s > threshold).mean()) if len(group) else 0.0

    plt.figure(figsize=(1.2 * len(sym_top) + 3, 0.6 * len(diag_top) + 3))
    plt.imshow(mat, aspect="auto")
    plt.colorbar(label="Proportion with symptom")
    plt.title(f"Symptom–Diagnosis Heatmap (proportion, > {threshold})")
    plt.yticks(range(len(diag_top)), diag_top)
    plt.xticks(range(len(sym_top)), sym_top, rotation=45, ha="right")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=220)
    if show:
        plt.show()
    plt.close()
