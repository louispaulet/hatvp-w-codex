"""Generate aggregated datasets for the React visualizations."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    """Compute summary CSV files used by the frontend charts."""
    root = Path(__file__).parent
    public = root / "react-vite-hatvp-dataviz" / "public"
    public.mkdir(parents=True, exist_ok=True)

    # Age band distribution
    personal = pd.read_csv(root / "personal_info_with_gender.csv")
    age_bins = list(range(20, 101, 10))
    age_labels = [f"{b}-{b + 9}" for b in age_bins[:-1]]
    personal["age_band"] = pd.cut(
        personal["age"], bins=age_bins, right=False, labels=age_labels
    )
    age_counts = (
        personal["age_band"].value_counts().sort_index().reset_index()
    )
    age_counts.columns = ["age_band", "count"]
    age_counts.to_csv(public / "age_band_counts.csv", index=False)

    # Gender distribution
    gender_counts = (
        personal["gender"].value_counts().reset_index()
    )
    gender_counts.columns = ["gender", "count"]
    gender_counts.to_csv(public / "gender_counts.csv", index=False)

    # Age pyramid by gender and age band
    pyramid = (
        personal.groupby(["age_band", "gender"]).size().reset_index(name="count")
    )
    pivot = pyramid.pivot(
        index="age_band", columns="gender", values="count"
    ).fillna(0)
    if "male" in pivot.columns:
        pivot["male"] = -pivot["male"]
    pivot.sort_index(ascending=False, inplace=True)
    pivot.reset_index().to_csv(public / "age_pyramid.csv", index=False)

    # Median publication delay by mandate type
    mandates = pd.read_csv(root / "mandates_features.csv")
    delay_by_type = (
        mandates.groupby("mandate_type")["delay_days"].median().reset_index()
    )
    delay_by_type.sort_values("delay_days", ascending=False, inplace=True)
    delay_by_type.to_csv(public / "mandate_delay_median.csv", index=False)


if __name__ == "__main__":
    main()
