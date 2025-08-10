"""Exploratory model for delays in mandate publication.

The script loads features prepared by :mod:`mandates.prepare_features`
from the raw ``liste.csv`` file and fits a simple logistic regression to
understand which factors correlate with long publication delays.

Generated artefacts such as figures or CSV files are intended for local
use only and are not committed to the repository.
"""

from __future__ import annotations

import argparse

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Import within package or as standalone script
try:  # pragma: no cover - normal package import
    from .prepare_features import prepare_features
except ImportError:  # pragma: no cover - fallback when executed as a script
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from mandates.prepare_features import prepare_features


DEFAULT_THRESHOLD = 90  # days


def build_dataset(csv_path: str, delay_threshold: int) -> tuple[pd.DataFrame, pd.Series]:
    """Prepare design matrix and target for modelling."""
    df = prepare_features(csv_path)
    df = df.dropna(subset=["delay_days", "departement", "mandate_type"])
    df["long_delay"] = df["delay_days"] > delay_threshold
    X = pd.get_dummies(df[["departement", "mandate_type"]], drop_first=True)
    y = df["long_delay"]
    return X, y


def main() -> None:
    parser = argparse.ArgumentParser(description="Model factors influencing long delays")
    parser.add_argument(
        "--csv", default="liste.csv", help="Raw CSV path (default: %(default)s)"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help="Delay threshold in days to consider 'long' (default: %(default)s)",
    )
    args = parser.parse_args()

    X, y = build_dataset(args.csv, args.threshold)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    report = classification_report(y, model.predict(X))
    print(report)


if __name__ == "__main__":  # pragma: no cover
    main()
