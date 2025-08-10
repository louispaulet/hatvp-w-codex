"""Entry point to run the full PII pipeline."""

from pathlib import Path

import pandas as pd

from full_pipeline import (
    DeclarationPipeline,
    GenderAnalyzer,
    SpouseOccupationAnalyzer,
    GenderDiscriminationAnalyzer,
)


def main() -> None:
    decl_dir = Path("split_declarations")
    org_names = pd.read_csv("avis/NER/organizations.csv")["name"].dropna().tolist()
    people_names = pd.read_csv("avis/NER/people.csv")["name"].dropna().tolist()
    pipeline = DeclarationPipeline(decl_dir, org_names, people_names)
    data = pipeline.run()

    gendered = GenderAnalyzer().analyze(data.personal_info)
    occ_counts, _ = SpouseOccupationAnalyzer().analyze(data.spouse_activities, gendered)
    GenderDiscriminationAnalyzer().analyze(occ_counts)


if __name__ == "__main__":
    main()
