import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import symptom_explorer.data_handler as dh
import symptom_explorer.stats as st
import symptom_explorer.rules as rules


def _toy_df():
    return pd.DataFrame(
        {"diagnosis": ["Flu", "Cold", "Flu", "Allergy"], "fever": [1, 0, 1, 0], "cough": [1, 1, 0, 0], "sneeze": [0, 0, 0, 1]}
    )


def test_run_all_stats_and_format():
    df = _toy_df()
    info = dh.infer_columns(df, diagnosis_col="diagnosis")
    res = st.run_all_stats(df, info.diagnosis_col, info.symptom_cols, threshold=0, top_n=10, symptom_metric="count")
    txt = st.format_stats(res, symptom_metric="count")
    assert "Top Symptoms" in txt
    assert "Top Diagnoses" in txt


def test_rules_suggest_diagnosis():
    df = _toy_df()
    info = dh.infer_columns(df, diagnosis_col="diagnosis")
    matched, sugg, notes = rules.suggest_diagnosis(df, info.diagnosis_col, info.symptom_cols, ["fever", "cough"], threshold=0)
    assert matched == 1
    assert len(sugg) >= 1
    assert isinstance(notes, list)


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
