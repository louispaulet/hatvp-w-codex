"""Analyze spouse occupation data for gender disparities."""

from pathlib import Path
from typing import Optional
import re
import unicodedata

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("spouse_occupation_gender_counts.csv")
TOP_MALE_CSV = Path("top_male_jobs.csv")
TOP_FEMALE_CSV = Path("top_female_jobs.csv")
PAY_SUMMARY_CSV = Path("pay_grade_summary.csv")
MALE_PLOT = Path("top_male_jobs.png")
FEMALE_PLOT = Path("top_female_jobs.png")
PAY_CATEGORY_PLOT = Path("pay_category_comparison.png")
TOP_N = 20

PLACEHOLDER_VALUES = {
    "",
    "-",
    "/",
    "0",
    "na",
    "n/a",
    "none",
    "null",
    "neant",
}

PLACEHOLDER_SUBSTRINGS = [
    "donnees non publiees",
    "donnee non publiee",
    "sans profession",
    "sans activite",
    "sans emploi",
]


def clean_occupation(occ: str) -> Optional[str]:
    """Normalize occupation text and drop placeholder values."""
    if pd.isna(occ):
        return None
    occ = str(occ).strip().lower()
    occ = re.sub(r"[\"']", "", occ)
    occ = unicodedata.normalize("NFKD", occ).encode("ascii", "ignore").decode()
    occ = re.sub(r"\s+", " ", occ)
    if not re.search(r"[a-z]", occ):
        return None
    for token in PLACEHOLDER_SUBSTRINGS:
        if token in occ:
            return None
    if "retraite" in occ:
        return None
    if occ in PLACEHOLDER_VALUES:
        return None
    return occ


HIGH_PAY_KEYWORDS = [
    "directeur",
    "director",
    "manager",
    "chef",
    "president",
    "medecin",
    "doctor",
    "ingenieur",
    "ingenieure",
    "professeur",
    "avocat",
    "notaire",
    "architect",
    "entrepreneur",
    "pharmacien",
    "pilote",
]

LOW_PAY_KEYWORDS = [
    "assistant",
    "assistante",
    "secretaire",
    "vendeur",
    "vendeuse",
    "agent",
    "employe",
    "employee",
    "caissier",
    "caissiere",
    "serveur",
    "serveuse",
    "aide",
    "infirmier",
    "infirmiere",
    "technicien",
    "ouvrier",
    "artisan",
    "animateur",
    "animatrice",
]


def classify_pay(job: str) -> str:
    """Classify job using keyword heuristics into pay categories."""
    for kw in HIGH_PAY_KEYWORDS:
        if kw in job:
            return "high"
    for kw in LOW_PAY_KEYWORDS:
        if kw in job:
            return "low"
    return "unknown"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    df["occupation"] = df["occupation"].apply(clean_occupation)
    df = df.dropna(subset=["occupation"])

    top_male = df.sort_values("male", ascending=False).head(TOP_N).copy()
    top_female = df.sort_values("female", ascending=False).head(TOP_N).copy()

    top_male["pay_grade"] = top_male["occupation"].apply(classify_pay)
    top_female["pay_grade"] = top_female["occupation"].apply(classify_pay)

    top_male.to_csv(TOP_MALE_CSV, index=False)
    top_female.to_csv(TOP_FEMALE_CSV, index=False)

    # Plot top male jobs
    ax = top_male.plot.barh(x="occupation", y="male", figsize=(10, 8))
    ax.invert_yaxis()
    ax.set_xlabel("Number of Spouses")
    ax.set_ylabel("Occupation")
    ax.set_title("Top 20 Spouse Occupations - Men")
    plt.tight_layout()
    plt.savefig(MALE_PLOT)
    plt.close()

    # Plot top female jobs
    ax = top_female.plot.barh(x="occupation", y="female", color="orange", figsize=(10, 8))
    ax.invert_yaxis()
    ax.set_xlabel("Number of Spouses")
    ax.set_ylabel("Occupation")
    ax.set_title("Top 20 Spouse Occupations - Women")
    plt.tight_layout()
    plt.savefig(FEMALE_PLOT)
    plt.close()

    pay_summary = (
        pd.DataFrame({
            "male": top_male["pay_grade"].value_counts(),
            "female": top_female["pay_grade"].value_counts(),
        })
        .T
        .reindex(columns=["high", "low", "unknown"], fill_value=0)
    )
    pay_summary.to_csv(PAY_SUMMARY_CSV)

    ax = pay_summary.plot(kind="bar", figsize=(8, 6))
    ax.set_ylabel("Count in Top 20")
    ax.set_title("Pay Grade Distribution in Top Occupations")
    plt.tight_layout()
    plt.savefig(PAY_CATEGORY_PLOT)
    plt.close()

    print("Top male occupations saved to", TOP_MALE_CSV)
    print("Top female occupations saved to", TOP_FEMALE_CSV)
    print("Pay grade summary saved to", PAY_SUMMARY_CSV)
    print("Plots saved to", MALE_PLOT, FEMALE_PLOT, "and", PAY_CATEGORY_PLOT)


if __name__ == "__main__":
    main()
