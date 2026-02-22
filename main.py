"""
Package entrypoint.

Run:
    python -m symptom_explorer.main --csv synthetic_medical_symptoms_and_diagnosis_dataset.csv
"""

from __future__ import annotations

import argparse
import os

from .app import run_app


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    p = argparse.ArgumentParser(description="Symptom Explorer - educational symptom/diagnosis tool.")
    p.add_argument("--csv", default="synthetic_medical_symptoms_and_diagnosis_dataset.csv", help="Path to the dataset CSV.")
    p.add_argument("--db", default=None, help="Optional SQLite database path for users.")
    return p.parse_args()


def main() -> None:
    """Main entrypoint."""
    args = parse_args()
    csv_path = os.path.abspath(args.csv)
    run_app(csv_path=csv_path, db_path=args.db)


if __name__ == "__main__":
    main()
