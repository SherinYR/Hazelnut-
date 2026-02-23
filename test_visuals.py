import pandas as pd
import symptom_explorer.data_handler as dh
import symptom_explorer.visuals as vis


def test_visuals_save_png(tmp_path):
    df = pd.DataFrame({"diagnosis": ["A", "B", "A", "C"], "fever": [1, 0, 1, 0], "cough": [0, 1, 1, 0], "sneeze": [0, 0, 0, 1]})
    info = dh.infer_columns(df, diagnosis_col="diagnosis")

    p1 = tmp_path / "symptoms.png"
    vis.symptom_plot(df, info.symptom_cols, threshold=0, top_n=3, metric="count", show=False, save_path=str(p1))
    assert p1.exists() and p1.stat().st_size > 0
