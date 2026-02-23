"""
Dataset loading and schema inference.

The dataset is expected to contain a diagnosis column ("diagnosis") and a number of
symptom indicator columns (typically 0..3). This module infers which columns are
symptoms vs non-symptoms via heuristics and performs basic cleaning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DatasetInfo:
    """Holds inferred dataset schema details."""
    diagnosis_col: str
    symptom_cols: List[str]
    non_symptom_cols: List[str]


DEFAULT_EXCLUDES = {
    "diagnosis",
    "age",
    "gender",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "temperature_c",
    "oxygen_saturation",
    "wbc_count",
    "hemoglobin",
    "platelet_count",
    "crp_level",
    "glucose_level",
}


def infer_columns(df: pd.DataFrame, diagnosis_col: str = "diagnosis") -> DatasetInfo:
    """
    Infer which columns are symptoms vs non-symptoms.

    Heuristic:
    - numeric columns with values typically in [0..3] and few unique values are treated as symptom indicators.
    - known clinical measurement columns are excluded via DEFAULT_EXCLUDES.
    """
    cols = [c for c in df.columns]
    if diagnosis_col not in cols:
        raise ValueError(f"Expected diagnosis column '{diagnosis_col}' not found. Columns: {cols}")

    symptom_cols: List[str] = []
    non_symptom_cols: List[str] = []

    for c in cols:
        lc = c.lower().strip()
        if lc in DEFAULT_EXCLUDES:
            non_symptom_cols.append(c)
            continue
        if c == diagnosis_col:
            continue

        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            s_numeric = pd.to_numeric(s, errors="coerce")
            smax = s_numeric.max()
            smin = s_numeric.min()
            nunique = s_numeric.nunique(dropna=True)
            if (smin >= 0) and (smax <= 3) and (nunique <= 5):
                symptom_cols.append(c)
            else:
                non_symptom_cols.append(c)
        else:
            non_symptom_cols.append(c)

    symptom_cols = [c for c in cols if c in symptom_cols]
    non_symptom_cols = [c for c in cols if c in non_symptom_cols and c != diagnosis_col]
    return DatasetInfo(diagnosis_col=diagnosis_col, symptom_cols=symptom_cols, non_symptom_cols=non_symptom_cols)


def load_dataset(csv_path: str) -> Tuple[pd.DataFrame, DatasetInfo]:
    """Load a CSV dataset and perform basic cleaning and schema inference."""
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]

    info = infer_columns(df, diagnosis_col="diagnosis")

    df[info.diagnosis_col] = df[info.diagnosis_col].astype(str).str.strip()
    df[info.diagnosis_col] = df[info.diagnosis_col].replace({"": np.nan}).fillna("Unknown")

    for c in info.symptom_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).clip(lower=0)

    if "gender" in df.columns:
        df["gender"] = df["gender"].astype(str).str.strip().str.title()

    return df, info
