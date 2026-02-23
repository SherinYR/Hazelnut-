"""
Statistical analysis functions for Symptom Explorer.
"""

from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd


@dataclass(frozen=True)
class StatsResults:
    """Container for computed statistics shown in the CLI and saved to text."""
    top_symptoms: List[Tuple[str, float]]
    top_diagnoses: List[Tuple[str, int]]
    avg_symptoms_per_patient: float
    top_cooccurrences: List[Tuple[Tuple[str, str], int]]
    notes: List[str]


def compute_top_symptoms(
    df: pd.DataFrame,
    symptom_cols: List[str],
    threshold: float = 0,
    top_n: int = 10,
    metric: str = "count",
) -> List[Tuple[str, float]]:
    """Compute the top-N symptoms by count or proportion of records."""
    rows = len(df)
    out: List[Tuple[str, float]] = []
    for c in symptom_cols:
        s = pd.to_numeric(df[c], errors="coerce").fillna(0)
        count = float((s > threshold).sum())
        if metric == "proportion":
            out.append((c, count / rows if rows else 0.0))
        else:
            out.append((c, count))
    out.sort(key=lambda x: x[1], reverse=True)
    return out[:top_n]


def compute_top_diagnoses(df: pd.DataFrame, diagnosis_col: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """Compute the top-N diagnoses by frequency."""
    vc = df[diagnosis_col].astype(str).value_counts(dropna=False)
    return [(idx, int(v)) for idx, v in vc.head(top_n).items()]


def compute_avg_symptoms(df: pd.DataFrame, symptom_cols: List[str], threshold: float = 0) -> float:
    """Compute average number of present symptoms per record (value > threshold)."""
    s = (df[symptom_cols].apply(pd.to_numeric, errors="coerce").fillna(0) > threshold).sum(axis=1)
    return float(s.mean())


def compute_cooccurrences(
    df: pd.DataFrame,
    symptom_cols: List[str],
    threshold: float = 0,
    top_n: int = 10,
) -> List[Tuple[Tuple[str, str], int]]:
    """Compute top co-occurring symptom pairs across records."""
    presence = (df[symptom_cols].apply(pd.to_numeric, errors="coerce").fillna(0) > threshold)
    counter: Counter = Counter()
    for _, row in presence.iterrows():
        present = [c for c, v in row.items() if bool(v)]
        for a, b in itertools.combinations(sorted(present), 2):
            counter[(a, b)] += 1
    return counter.most_common(top_n)


def run_all_stats(
    df: pd.DataFrame,
    diagnosis_col: str,
    symptom_cols: List[str],
    threshold: float = 0,
    top_n: int = 10,
    symptom_metric: str = "count",
) -> StatsResults:
    """Run the full statistics pipeline and return a StatsResults object."""
    notes: List[str] = []
    n_diag = df[diagnosis_col].astype(str).nunique()
    if n_diag < top_n:
        notes.append(f"Dataset contains only {n_diag} unique diagnoses; showing all available diagnoses.")

    return StatsResults(
        top_symptoms=compute_top_symptoms(df, symptom_cols, threshold=threshold, top_n=top_n, metric=symptom_metric),
        top_diagnoses=compute_top_diagnoses(df, diagnosis_col, top_n=top_n),
        avg_symptoms_per_patient=compute_avg_symptoms(df, symptom_cols, threshold=threshold),
        top_cooccurrences=compute_cooccurrences(df, symptom_cols, threshold=threshold, top_n=top_n),
        notes=notes,
    )


def format_stats(results: StatsResults, symptom_metric: str) -> str:
    """Format statistics results as a human-readable text block."""
    lines: List[str] = []
    lines.append("=== Symptom Explorer: Statistics Summary ===\n")
    for n in results.notes:
        lines.append(f"NOTE: {n}")
    if results.notes:
        lines.append("")

    lines.append("Top Symptoms:")
    for name, val in results.top_symptoms:
        if symptom_metric == "proportion":
            lines.append(f"  - {name}: {val:.3f}")
        else:
            lines.append(f"  - {name}: {int(val)}")
    lines.append("")

    lines.append("Top Diagnoses (by frequency):")
    for name, cnt in results.top_diagnoses:
        lines.append(f"  - {name}: {cnt}")
    lines.append("")

    lines.append(f"Average # of symptoms per patient (value > threshold): {results.avg_symptoms_per_patient:.2f}\n")

    lines.append("Top Symptom Co-occurrences (pairs):")
    for (a, b), cnt in results.top_cooccurrences:
        lines.append(f"  - ({a}, {b}): {cnt}")

    lines.append("")
    return "\n".join(lines)
