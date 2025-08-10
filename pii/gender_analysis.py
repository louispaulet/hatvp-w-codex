"""Generate gender predictions for personal_info dataset and output stats."""

from pathlib import Path
import pandas as pd
from gender_guesser.detector import Detector


DATA_PATH = Path("pii/personal_info.csv")
OUTPUT_CSV = Path("pii/personal_info_with_gender.csv")
REPORT_PATH = Path("pii/gender_report.md")


def main() -> None:
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Extract first name
    df["first_name"] = df["prenom"].astype(str).str.split().str[0]

    # Guess gender from first name
    detector = Detector(case_sensitive=False)
    df["gender_guess"] = df["first_name"].apply(detector.get_gender)

    # Map civilité to gender
    civilite_map = {"M": "male", "M.": "male", "Mme": "female", "Mme.": "female"}
    df["gender"] = df["civilite"].map(civilite_map)

    # Save dataframe with gender and guess columns
    df.to_csv(OUTPUT_CSV, index=False)

    # Generate stats
    total = len(df)
    gender_counts = df["gender"].value_counts().rename_axis("gender").to_frame("count")
    gender_counts["percent"] = (gender_counts["count"] / total * 100).round(2)

    civilite_guess = pd.crosstab(df["civilite"], df["gender_guess"])
    top_first_names = df["first_name"].str.title().value_counts().head(10)

    # Write markdown report
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# Gender Analysis Report\n\n")
        f.write(f"Total records: {total}\n\n")

        f.write("## Gender distribution\n\n")
        f.write(gender_counts.to_markdown())
        f.write("\n\n")

        f.write("## Gender guess by civilité\n\n")
        f.write(civilite_guess.to_markdown())
        f.write("\n\n")

        f.write("## Top 10 first names\n\n")
        f.write(top_first_names.to_markdown())
        f.write("\n")


if __name__ == "__main__":
    main()
