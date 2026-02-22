"""
Educational rule-based diagnosis matching.

This is NOT a medical diagnosis system; it simply filters dataset rows that match
a set of symptoms and reports the most frequent diagnoses among those rows.
"""

from __future__ import annotations

from typing import List, Tuple

import pandas as pd


def normalize_symptom_name(name: str) -> str:
    """Normalize a symptom name to a column-like token (lowercase, underscores)."""
    return (name or "").strip().lower().replace(" ", "_")


def parse_symptom_input(raw: str) -> List[str]:
    """Parse a comma-separated symptom list into normalized tokens."""
    parts = [p.strip() for p in (raw or "").split(",")]
    parts = [p for p in parts if p]
    return [normalize_symptom_name(p) for p in parts]


def suggest_diagnosis(
    df: pd.DataFrame,
    diagnosis_col: str,
    symptom_cols: List[str],
    user_symptoms: List[str],
    threshold: float = 0,
    top_k: int = 3,
) -> Tuple[int, List[Tuple[str, int]], List[str]]:
    """
    Suggest diagnoses by filtering records that match all entered symptoms.

    Returns:
    - matched_count: number of matching records
    - suggestions: list of (diagnosis, count) among matching records
    - notes: user-facing notes such as unknown symptoms ignored
    """
    if not user_symptoms:
        return 0, [], ["No symptoms entered."]

    col_map = {c.lower(): c for c in symptom_cols}
    resolved = [col_map[s] for s in user_symptoms if s in col_map]

    unknown = [s for s in user_symptoms if s not in col_map]
    notes: List[str] = []
    if unknown:
        notes.append(f"Ignored unknown symptom(s): {', '.join(unknown)}")

    if not resolved:
        notes.append("None of the entered symptoms matched dataset symptom columns.")
        return 0, [], notes

    mask = pd.Series([True] * len(df))
    for c in resolved:
        mask = mask & (pd.to_numeric(df[c], errors="coerce").fillna(0) > threshold)

    matched = df[mask]
    matched_count = int(len(matched))
    if matched_count == 0:
        notes.append("No matching records found for that symptom set.")
        return 0, [], notes

    vc = matched[diagnosis_col].astype(str).value_counts().head(top_k)
    suggestions = [(idx, int(v)) for idx, v in vc.items()]
    return matched_count, suggestions, notes
