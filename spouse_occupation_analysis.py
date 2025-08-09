"""Analyze spouse occupations and plot trends."""

from pathlib import Path
import unicodedata

import matplotlib.pyplot as plt
import pandas as pd

SPOUSE_CSV = Path("pii/spouse_activities.csv")
PERSONAL_CSV = Path("pii/personal_info_with_gender.csv")
OUTPUT_PLOT = Path("spouse_occupation_trends.png")
OUTPUT_CSV = Path("spouse_occupation_gender_counts.csv")
TOP_N = 50


def main() -> None:
    # Load datasets
    spouse_df = pd.read_csv(SPOUSE_CSV)
    personal_df = pd.read_csv(
        PERSONAL_CSV, parse_dates=["dateDepot"], dayfirst=True
    )

    # Merge on uuid and extract year from deposit date
    df = spouse_df.merge(
        personal_df[["uuid", "dateDepot", "gender"]], on="uuid", how="inner"
    )
    df = df.dropna(subset=["activiteProf", "dateDepot"])  # remove missing values
    df["activiteProf"] = df["activiteProf"].astype(str).str.strip()
    df = df[df["activiteProf"] != "[Données non publiées]"]

    # Normalize job names for consistent counting
    df["job_norm"] = (
        df["activiteProf"]
        .str.lower()
        .apply(lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))
    )
    df["year"] = df["dateDepot"].dt.year
    df["spouse_gender"] = df["gender"].map({"male": "female", "female": "male"})

    # Compute top occupations
    top_jobs = df["job_norm"].value_counts().head(TOP_N)
    print("Top 50 spouse occupations:")
    print(top_jobs.rename(lambda x: x.title()).to_string())

    # Save gender counts per occupation
    gender_counts = (
        df.groupby(["job_norm", "spouse_gender"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["male", "female"], fill_value=0)
        .reset_index()
        .rename(columns={"job_norm": "occupation"})
    )
    gender_counts["occupation"] = gender_counts["occupation"].str.title()
    gender_counts.to_csv(OUTPUT_CSV, index=False)
    print(f"Gender counts saved to {OUTPUT_CSV}")

    # Plot trends for top 5 occupations over time
    top5 = top_jobs.head(5).index
    trend_df = (
        df[df["job_norm"].isin(top5)]
        .groupby(["year", "job_norm"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
        .rename(columns=lambda x: x.title())
    )

    ax = trend_df.plot(kind="line", figsize=(10, 6))
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    ax.set_title("Top spouse occupations over time")
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)
    print(f"Plot saved to {OUTPUT_PLOT}")


if __name__ == "__main__":
    main()
