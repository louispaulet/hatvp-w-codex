from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DATA_PATH = Path("pii/personal_info_with_gender.csv")
OUTPUT_PNG = Path("age_pyramid.png")


def main() -> None:
    """Load data, build age pyramid and save to PNG."""
    # Load dataset
    df = pd.read_csv(DATA_PATH)
    df["birth"] = pd.to_datetime(df["dateNaissance"], format="%d/%m/%Y", errors="coerce")

    # Keep plausible birth years
    df = df[(df["birth"].dt.year >= 1900) & (df["birth"].dt.year <= 2020)]

    # Compute age
    today = pd.Timestamp.today()
    df["age"] = (today - df["birth"]).dt.days // 365

    # Bin ages into five-year groups
    min_age = int(df["age"].min()) // 5 * 5
    max_age = (int(df["age"].max()) // 5 + 1) * 5
    age_bins = list(range(min_age, max_age + 5, 5))
    df["age_group"] = pd.cut(df["age"], bins=age_bins, right=False)

    # Reverse order so youngest is at the bottom
    age_categories = df["age_group"].cat.categories[::-1]
    df["age_group"] = pd.Categorical(df["age_group"], categories=age_categories, ordered=True)

    # Count by age group and gender
    pyramid = (
        df.groupby(["age_group", "gender"]).size().reset_index(name="count")
    )
    pyramid.loc[pyramid["gender"] == "male", "count"] *= -1

    # Plot
    sns.set_style("whitegrid")
    plt.figure(figsize=(8, 10))
    sns.barplot(
        data=pyramid,
        x="count",
        y="age_group",
        hue="gender",
        orient="h",
        dodge=False,
    )
    plt.axvline(0, color="black", linewidth=0.8)
    plt.xlabel("Number of individuals")
    plt.ylabel("Age group")
    plt.title("Age Pyramid by Gender")
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)


if __name__ == "__main__":
    main()
