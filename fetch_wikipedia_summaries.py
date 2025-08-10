#!/usr/bin/env python3
"""Fetch French Wikipedia summaries for names listed in avis/NER/people.csv.

For each person in the CSV file, the script queries the French Wikipedia REST
API for a short summary and stores the result in individual text files within
``avis/NER/wikipedia_summaries``.
"""
from __future__ import annotations

import csv
import pathlib
from urllib.parse import quote

import requests

PEOPLE_CSV = pathlib.Path("avis/NER/people.csv")
OUTPUT_DIR = pathlib.Path("avis/NER/wikipedia_summaries")


def fetch_summary(name: str) -> str | None:
    """Return the summary extract for *name* from French Wikipedia.

    Parameters
    ----------
    name:
        Person's full name.
    """
    title = quote(name.replace(" ", "_"))
    url = f"https://fr.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get("extract")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with PEOPLE_CSV.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            name = row.get("name")
            if not name:
                continue
            summary = fetch_summary(name)
            sanitized = name.replace(" ", "_")
            out_file = OUTPUT_DIR / f"{sanitized}.txt"
            text = summary if summary else "No summary found or request failed."
            out_file.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
