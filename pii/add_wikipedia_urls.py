"""Append a Wikipedia URL column to personal_info_enriched.csv."""

from __future__ import annotations

import argparse
import sys
from itertools import islice
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# Allow running the script directly without installing the package.
sys.path.append(str(Path(__file__).resolve().parents[1]))
from local_llm.wikipedia_url import get_wikipedia_url


DEFAULT_CSV = Path("pii/personal_info_enriched.csv")


def enrich(csv_path: Path, limit: int | None = None) -> None:
    """Add a ``wikipedia_url`` column to ``csv_path`` in place."""
    df = pd.read_csv(csv_path)
    rows = df.iterrows()
    total = len(df)
    if limit is not None:
        total = min(limit, total)
        rows = islice(rows, limit)
    for idx, row in tqdm(rows, total=total):
        df.loc[idx, "wikipedia_url"] = get_wikipedia_url(row["prenom"], row["nom"])
    df.to_csv(csv_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="CSV file to enrich")
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N rows")
    args = parser.parse_args()

    enrich(args.csv, args.limit)


if __name__ == "__main__":
    main()
