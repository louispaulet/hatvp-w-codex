"""Exploratory model for delays in mandate publication.

Loads features prepared by :mod:`mandates.prepare_features` from the raw
``liste.csv`` file and fits an XGBoost classifier to model which factors
correlate with long publication delays.

Evaluation is out-of-sample using Precision–Recall AUC (Average Precision),
and we also print a confusion matrix plus extra metrics. Optional flags let you
run cross-validated AUPRC, plot a PR curve, and optimize the decision threshold.

Generated artefacts (figures/CSVs) are for local use only and are not committed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    precision_recall_curve,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from xgboost import XGBClassifier
from xgboost.callback import EarlyStopping


# Import within package or as standalone script
try:  # pragma: no cover - normal package import
    from .prepare_features import prepare_features
except ImportError:  # pragma: no cover - fallback when executed as a script
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from mandates.prepare_features import prepare_features


DEFAULT_THRESHOLD = 90  # days


def build_dataset(csv_path: str, delay_threshold: int) -> tuple[pd.DataFrame, pd.Series]:
    """Prepare design matrix and target for modelling."""
    df = prepare_features(csv_path)
    df = df.dropna(subset=["delay_days", "departement", "mandate_type"])
    df["long_delay"] = df["delay_days"] > delay_threshold
    X = pd.get_dummies(df[["departement", "mandate_type"]], drop_first=True)
    y = df["long_delay"].astype(int)
    return X, y


def print_confusion_and_metrics(y_true: pd.Series, y_scores: np.ndarray, threshold: float, header: str) -> None:
    """Print confusion matrix and common metrics at a given threshold."""
    y_pred = (y_scores >= threshold).astype(int)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    bal_acc = balanced_accuracy_score(y_true, y_pred)

    print(header)
    print("Confusion Matrix")
    print(f"TN: {tn} | FP: {fp}")
    print(f"FN: {fn} | TP: {tp}")
    print(f"Precision:         {precision:.4f}")
    print(f"Recall:            {recall:.4f}")
    print(f"F1-score:          {f1:.4f}")
    print(f"Balanced accuracy: {bal_acc:.4f}\n")


def optimize_threshold_by_f1(y_true: pd.Series, y_scores: np.ndarray) -> float:
    """Return the probability threshold that maximizes F1 on y_true."""
    p, r, t = precision_recall_curve(y_true, y_scores)
    # thresholds t has length len(p)-1; derive F1 for points where threshold is defined
    f1_vals = (2 * p[:-1] * r[:-1]) / (p[:-1] + r[:-1] + 1e-12)
    best_idx = np.nanargmax(f1_vals)
    # guard: thresholds array corresponds to p[1:] / r[1:] points
    return float(t[best_idx]) if len(t) else 0.5


def make_model(random_state: int, scale_pos_weight: float) -> XGBClassifier:
    """Factory for XGBClassifier with sensible defaults for tabular + imbalance."""
    return XGBClassifier(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        tree_method="hist",
        eval_metric="aucpr",
        random_state=random_state,
        n_jobs=-1,
        scale_pos_weight=scale_pos_weight,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Model factors influencing long delays")
    parser.add_argument("--csv", default="liste.csv", help="Raw CSV path (default: %(default)s)")
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help="Delay threshold in days to consider 'long' (default: %(default)s)",
    )
    parser.add_argument("--test-size", type=float, default=0.2, help="Test size fraction (default: %(default)s)")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed (default: %(default)s)")
    parser.add_argument("--cv", type=int, default=0, help="Number of CV folds for AUPRC (0 to disable)")
    parser.add_argument("--plot-pr", action="store_true", help="Save PR curve to pr_curve.png")
    parser.add_argument(
        "--optimize-threshold",
        action="store_true",
        help="Also compute metrics at the F1-maximizing threshold on the test set",
    )
    args = parser.parse_args()

    # Data
    X, y = build_dataset(args.csv, args.threshold)

    # Optional cross-validated AUPRC
    if args.cv and args.cv > 1:
        cv = StratifiedKFold(n_splits=args.cv, shuffle=True, random_state=args.random_state)
        aps = []
        for tr, te in cv.split(X, y):
            X_tr, X_te = X.iloc[tr], X.iloc[te]
            y_tr, y_te = y.iloc[tr], y.iloc[te]
            pos = y_tr.sum()
            neg = len(y_tr) - pos
            spw = (neg / pos) if pos > 0 else 1.0

            clf = make_model(args.random_state, spw)
            clf.fit(
                X_tr,
                y_tr,
                eval_set=[(X_tr, y_tr), (X_te, y_te)],
                verbose=False,
                #callbacks=[EarlyStopping(rounds=50, save_best=True)],
            )
            y_sc = clf.predict_proba(X_te)[:, 1]
            aps.append(average_precision_score(y_te, y_sc))

        print(f"{args.cv}-fold CV Average Precision: {np.mean(aps):.4f} ± {np.std(aps):.4f}")
        return  # Skip holdout path when CV is requested

    # Holdout split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, stratify=y, random_state=args.random_state
    )

    # Class imbalance handling
    pos = y_train.sum()
    neg = len(y_train) - pos
    scale_pos_weight = (neg / pos) if pos > 0 else 1.0

    # Train
    model = make_model(args.random_state, scale_pos_weight)
    model.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=False,
        #callbacks=[EarlyStopping(rounds=50, save_best=True)],
    )

    # Scores
    y_scores = model.predict_proba(X_test)[:, 1]
    pr_auc = average_precision_score(y_test, y_scores)
    prevalence = y_test.mean()

    best_iter = getattr(model, "best_iteration", None)
    if best_iter is None:
        best_iter = model.get_params().get("n_estimators", "n/a")

    print(f"\nTest Precision–Recall AUC (Average Precision): {pr_auc:.4f}")
    print(f"Positive class prevalence (baseline AP):      {prevalence:.4f}")
    print(f"Best iteration used:                          {best_iter}\n")

    # Metrics at default threshold 0.5
    print_confusion_and_metrics(y_test, y_scores, threshold=0.5, header="== Metrics @ threshold = 0.5 ==")

    # Optional: Metrics at F1-maximizing threshold
    if args.optimize_threshold:
        thr = optimize_threshold_by_f1(y_test, y_scores)
        print(f"Chosen threshold to maximize F1 on test set: {thr:.4f}\n")
        print_confusion_and_metrics(y_test, y_scores, threshold=thr, header="== Metrics @ F1-optimal threshold ==")

    # Optional: plot PR curve
    if args.plot_pr:
        import matplotlib.pyplot as plt

        p, r, _ = precision_recall_curve(y_test, y_scores)
        plt.figure()
        plt.step(r, p, where="post")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title(f"PR curve (AP = {pr_auc:.3f})")
        plt.tight_layout()
        plt.savefig("pr_curve.png")
        print("Saved PR curve to pr_curve.png")


if __name__ == "__main__":  # pragma: no cover
    main()
