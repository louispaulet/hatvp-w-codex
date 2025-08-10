import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import re

OUTPUT_DIR = Path("family_name_analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

# Load datasets
pii = pd.read_csv("personal_info_with_gender.csv")
stocks = pd.read_csv("stock_extract/stocks.csv")

# Helper to clean numeric values
def clean_number(x):
    if pd.isna(x):
        return 0.0
    if isinstance(x, (int, float)):
        return float(x)
    x = str(x)
    x = re.sub(r"[^0-9.,]", "", x)
    x = x.replace(",", "")
    return float(x) if x else 0.0

stocks["evaluation"] = stocks["evaluation"].apply(clean_number)

# 1. Declarations per family name
declarations = (
    pii.groupby("nom")
    .size()
    .reset_index(name="declaration_count")
    .sort_values("declaration_count", ascending=False)
)
declarations.to_csv(OUTPUT_DIR / "declarations_per_family_name.csv", index=False)
plt.figure(figsize=(10, 8))
sns.barplot(data=declarations.head(20), x="declaration_count", y="nom")
plt.title("Top 20 Family Names by Declarations")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "declarations_per_family_name.png")
plt.close()

# 2. People per family name with gender and age stats
people = pii.drop_duplicates("uuid")

def gender_count(series, gender):
    return (series == gender).sum()

people_stats = (
    people.groupby("nom")
    .agg(
        people_count=("uuid", "nunique"),
        male=("gender", lambda x: gender_count(x, "male")),
        female=("gender", lambda x: gender_count(x, "female")),
        min_age=("age", "min"),
        max_age=("age", "max"),
        avg_age=("age", "mean"),
    )
    .reset_index()
    .sort_values("people_count", ascending=False)
)
people_stats.to_csv(OUTPUT_DIR / "people_stats_per_family_name.csv", index=False)
plt.figure(figsize=(10, 8))
sns.barplot(data=people_stats.head(20), x="people_count", y="nom")
plt.title("Top 20 Family Names by People Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "people_per_family_name.png")
plt.close()

# 3. Cumulated wealth per family name
stocks_people = stocks.merge(people[["uuid", "nom", "age", "gender"]], on="uuid", how="left")
person_wealth = stocks_people.groupby("uuid")["evaluation"].sum().reset_index(name="total_wealth")
person_wealth = person_wealth.merge(people[["uuid", "nom", "age", "gender"]], on="uuid", how="left")
family_wealth = (
    person_wealth.groupby("nom")["total_wealth"].sum().reset_index().sort_values("total_wealth", ascending=False)
)
family_wealth.to_csv(OUTPUT_DIR / "wealth_per_family_name.csv", index=False)
plt.figure(figsize=(10, 8))
sns.barplot(data=family_wealth.head(20), x="total_wealth", y="nom")
plt.title("Top 20 Families by Total Wealth")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "wealth_per_family_name.png")
plt.close()

# Additional Analyses
top_families = people_stats.head(10)["nom"]

# 4. Average wealth per person per family name
avg_family_wealth = (
    person_wealth.groupby("nom")["total_wealth"].mean().reset_index(name="avg_person_wealth").sort_values(
        "avg_person_wealth", ascending=False
    )
)
avg_family_wealth.to_csv(OUTPUT_DIR / "avg_wealth_per_person_family.csv", index=False)
plt.figure(figsize=(10, 8))
sns.barplot(data=avg_family_wealth.head(20), x="avg_person_wealth", y="nom")
plt.title("Top Families by Average Wealth per Person")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "avg_wealth_per_person.png")
plt.close()

# 5. Age distribution for top families
age_top = people[people["nom"].isin(top_families)][["nom", "age"]]
age_top.to_csv(OUTPUT_DIR / "age_distribution_top_families.csv", index=False)
plt.figure(figsize=(10, 8))
sns.boxplot(data=age_top, x="age", y="nom")
plt.title("Age Distribution of Top Families")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "age_distribution_top_families.png")
plt.close()

# 6. Gender breakdown for top families
gender_top = (
    people[people["nom"].isin(top_families)]
    .groupby(["nom", "gender"])
    .size()
    .reset_index(name="count")
)
gender_top.to_csv(OUTPUT_DIR / "gender_breakdown_top_families.csv", index=False)
plt.figure(figsize=(10, 8))
sns.barplot(data=gender_top, x="count", y="nom", hue="gender")
plt.title("Gender Breakdown in Top Families")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "gender_breakdown_top_families.png")
plt.close()

# 7. Wealth vs declarations per family
wealth_vs_decl = declarations.merge(family_wealth, on="nom", how="left").fillna(0)
wealth_vs_decl.to_csv(OUTPUT_DIR / "wealth_vs_declarations.csv", index=False)
plt.figure(figsize=(10, 8))
sns.scatterplot(data=wealth_vs_decl, x="declaration_count", y="total_wealth")
plt.title("Declarations vs Total Wealth per Family")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "wealth_vs_declarations.png")
plt.close()

# 8. Average age vs wealth per family
age_vs_wealth_family = person_wealth.groupby("nom").agg(avg_age=("age", "mean"), total_wealth=("total_wealth", "sum")).reset_index()
age_vs_wealth_family.to_csv(OUTPUT_DIR / "age_vs_wealth_family.csv", index=False)
plt.figure(figsize=(10, 8))
sns.scatterplot(data=age_vs_wealth_family, x="avg_age", y="total_wealth")
plt.title("Average Age vs Total Wealth per Family")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "age_vs_wealth_family.png")
plt.close()

print("Analysis complete. Outputs saved to", OUTPUT_DIR)
