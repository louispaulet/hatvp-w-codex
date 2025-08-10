"""Feature preparation for mandate compliance analysis.

This module parses the publication and deposit dates from the raw
`liste.csv` dataset, computes the delay between the two events in days
and exposes the mandate type as a categorical feature.

The script can be executed directly to produce a local CSV file with the
added features.  Generated files are not tracked in version control.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def prepare_features(csv_path: str | Path) -> pd.DataFrame:
    """Load dataset and create basic features.

    Parameters
    ----------
    csv_path:
        Path to the raw `liste.csv` file.

    Returns
    -------
    pandas.DataFrame
        DataFrame with parsed dates, the delay in days and a categorical
        `mandate_type` column.
    """
    df = pd.read_csv(csv_path, sep=";", dtype=str)
    # Parse the publication and deposit dates
    df["date_publication"] = pd.to_datetime(df["date_publication"], errors="coerce")
    df["date_depot"] = pd.to_datetime(df["date_depot"], errors="coerce")

    # Compute the delay in days between deposit and publication
    df["delay_days"] = (df["date_publication"] - df["date_depot"]).dt.days

    # Expose mandate type as categorical data
    df["mandate_type"] = df["type_mandat"].astype("category")

    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare mandate features")
    parser.add_argument(
        "--csv",
        default="liste.csv",
        help="Path to the raw CSV file (default: %(default)s)",
    )
    parser.add_argument(
        "--out",
        default="mandates_features.csv",
        help="Where to store the feature CSV (default: %(default)s)",
    )
    args = parser.parse_args()

    df = prepare_features(args.csv)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"Wrote {args.out} with {len(df)} rows")


if __name__ == "__main__":  # pragma: no cover
    main()
