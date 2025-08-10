"""Classes implementing the PII extraction and analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Dict, List, Tuple
import re
import unicodedata
import xml.etree.ElementTree as ET

import pandas as pd
from tqdm import tqdm
from gender_guesser.detector import Detector
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# Extraction utilities
# ---------------------------------------------------------------------------

@dataclass
class ExtractedData:
    """Container for extracted datasets."""

    personal_info: pd.DataFrame
    spouse_activities: pd.DataFrame
    organization_mentions: pd.DataFrame
    people_mentions: pd.DataFrame


class DeclarationPipeline:
    """Parse declaration XML files once and extract required datasets."""

    def __init__(
        self,
        decl_dir: Path,
        organization_names: Optional[Iterable[str]] = None,
        people_names: Optional[Iterable[str]] = None,
    ) -> None:
        self.decl_dir = Path(decl_dir)
        self.organization_names = list(organization_names or [])
        self.people_names = list(people_names or [])

    def run(self) -> ExtractedData:
        """Process all XML files and return extracted datasets."""
        personal_rows: List[Dict[str, str]] = []
        spouse_rows: List[Dict[str, str]] = []
        org_mentions: Dict[str, set] = {n: set() for n in self.organization_names}
        people_mentions: Dict[str, set] = {n: set() for n in self.people_names}

        xml_files = sorted(self.decl_dir.glob("*.xml"))
        for xml_file in tqdm(xml_files, desc="Declarations"):
            text = xml_file.read_text(encoding="utf-8", errors="ignore")
            for name in self.organization_names:
                if name in text:
                    org_mentions[name].add(xml_file.name)
            for name in self.people_names:
                if name in text:
                    people_mentions[name].add(xml_file.name)

            try:
                tree = ET.parse(xml_file)
            except ET.ParseError:
                continue
            root = tree.getroot()

            def get_unique(parent, tag):
                elems = parent.findall(f".//{tag}") if parent is not None else []
                if len(elems) > 1:
                    raise ValueError(f"Multiple <{tag}> in {xml_file}")
                return elems[0] if elems else None

            declaration = root if root.tag == "declaration" else get_unique(root, "declaration")
            general = get_unique(declaration, "general")
            declarant = get_unique(general, "declarant")

            def get_text(elem: ET.Element | None, tag: str) -> str:
                if elem is None:
                    return ""
                text = elem.findtext(tag, default="")
                return text.strip() if text else ""

            info = {
                "file": xml_file.name,
                "dateDepot": get_text(declaration, "dateDepot"),
                "uuid": get_text(declaration, "uuid"),
                "civilite": get_text(declarant, "civilite"),
                "nom": get_text(declarant, "nom"),
                "prenom": get_text(declarant, "prenom"),
                "email": get_text(declarant, "email"),
                "dateNaissance": get_text(declarant, "dateNaissance"),
            }
            personal_rows.append(info)

            spouse_dto = get_unique(declaration, "activProfConjointDto")
            if spouse_dto is not None:
                for item in spouse_dto.findall("./items/items"):
                    def clean(text: Optional[str]) -> str:
                        return " ".join(text.split()) if text else ""

                    spouse_rows.append(
                        {
                            "uuid": info["uuid"],
                            "nomConjoint": clean(item.findtext("nomConjoint")),
                            "employeurConjoint": clean(item.findtext("employeurConjoint")),
                            "activiteProf": clean(item.findtext("activiteProf")),
                            "commentaire": clean(item.findtext("commentaire")),
                        }
                    )

        personal_df = pd.DataFrame(personal_rows)
        spouse_df = pd.DataFrame(spouse_rows)
        org_df = self._mentions_to_df(org_mentions, "organization")
        people_df = self._mentions_to_df(people_mentions, "person")
        return ExtractedData(personal_df, spouse_df, org_df, people_df)

    @staticmethod
    def _mentions_to_df(mentions: Dict[str, set], label: str) -> pd.DataFrame:
        rows = []
        for name, files in mentions.items():
            rows.append(
                {
                    label: name,
                    "mentions": len(files),
                    "filenames": ",".join(sorted(files)),
                }
            )
        return pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# Gender analysis
# ---------------------------------------------------------------------------

class GenderAnalyzer:
    """Add gender predictions and summary columns to personal data."""

    def __init__(self) -> None:
        self.detector = Detector(case_sensitive=False)

    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        data["first_name"] = data["prenom"].astype(str).str.split().str[0]
        data["gender_guess"] = data["first_name"].apply(self.detector.get_gender)
        civilite_map = {"M": "male", "M.": "male", "Mme": "female", "Mme.": "female"}
        data["gender"] = data["civilite"].map(civilite_map)
        return data

# ---------------------------------------------------------------------------
# Spouse occupation analysis
# ---------------------------------------------------------------------------

class SpouseOccupationAnalyzer:
    """Merge spouse activities with personal info and compute gender counts."""

    def analyze(
        self, spouse_df: pd.DataFrame, personal_df: pd.DataFrame, top_n: int = 50
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = spouse_df.merge(
            personal_df[["uuid", "dateDepot", "gender"]], on="uuid", how="inner"
        )
        df = df.dropna(subset=["activiteProf", "dateDepot"])
        df["activiteProf"] = df["activiteProf"].astype(str).str.strip()
        df = df[df["activiteProf"] != "[Données non publiées]"]
        df["job_norm"] = (
            df["activiteProf"].str.lower().apply(
                lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8")
            )
        )
        df["dateDepot"] = pd.to_datetime(df["dateDepot"], dayfirst=True, errors="coerce")
        df["year"] = df["dateDepot"].dt.year
        df["spouse_gender"] = df["gender"].map({"male": "female", "female": "male"})

        gender_counts = (
            df.groupby(["job_norm", "spouse_gender"])
            .size()
            .unstack(fill_value=0)
            .reindex(columns=["male", "female"], fill_value=0)
            .reset_index()
            .rename(columns={"job_norm": "occupation"})
        )
        gender_counts.columns.name = None
        gender_counts["occupation"] = gender_counts["occupation"].str.title()

        top_jobs = df["job_norm"].value_counts().head(top_n).index
        trend_df = (
            df[df["job_norm"].isin(top_jobs)]
            .groupby(["year", "job_norm"])
            .size()
            .unstack(fill_value=0)
            .sort_index()
            .rename(columns=lambda x: x.title())
        )
        return gender_counts, trend_df

# ---------------------------------------------------------------------------
# Gender discrimination analysis
# ---------------------------------------------------------------------------

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


class GenderDiscriminationAnalyzer:
    """Analyze spouse occupation gender counts for disparities."""

    def __init__(self, top_n: int = 20) -> None:
        self.top_n = top_n

    @staticmethod
    def _clean_occupation(occ: str) -> Optional[str]:
        if pd.isna(occ):
            return None
        occ = str(occ).strip().lower()
        occ = re.sub(r"[\"']", "", occ)
        occ = unicodedata.normalize("NFKD", occ).encode("ascii", "ignore").decode()
        occ = re.sub(r"\s+", " ", occ)
        if not re.search(r"[a-z]", occ):
            return None
        placeholders = {
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
        for token in [
            "donnees non publiees",
            "donnee non publiee",
            "sans profession",
            "sans activite",
            "sans emploi",
        ]:
            if token in occ:
                return None
        if "retraite" in occ:
            return None
        if occ in placeholders:
            return None
        return occ

    @staticmethod
    def _classify_pay(job: str) -> str:
        for kw in HIGH_PAY_KEYWORDS:
            if kw in job:
                return "high"
        for kw in LOW_PAY_KEYWORDS:
            if kw in job:
                return "low"
        return "unknown"

    def analyze(self, counts_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        df = counts_df.copy()
        df["occupation"] = df["occupation"].apply(self._clean_occupation)
        df = df.dropna(subset=["occupation"])

        top_male = df.sort_values("male", ascending=False).head(self.top_n).copy()
        top_female = df.sort_values("female", ascending=False).head(self.top_n).copy()
        top_male["pay_grade"] = top_male["occupation"].apply(self._classify_pay)
        top_female["pay_grade"] = top_female["occupation"].apply(self._classify_pay)

        pay_summary = (
            pd.DataFrame(
                {
                    "male": top_male["pay_grade"].value_counts(),
                    "female": top_female["pay_grade"].value_counts(),
                }
            )
            .T
            .reindex(columns=["high", "low", "unknown"], fill_value=0)
        )
        pay_summary.columns.name = None
        return top_male, top_female, pay_summary

# ---------------------------------------------------------------------------
# Age pyramid
# ---------------------------------------------------------------------------

class AgePyramidBuilder:
    """Build an age pyramid plot from personal info with gender."""

    def build(self, df: pd.DataFrame, output: Path) -> None:
        df = df.copy()
        df["birth"] = pd.to_datetime(df["dateNaissance"], format="%d/%m/%Y", errors="coerce")
        df = df[(df["birth"].dt.year >= 1900) & (df["birth"].dt.year <= 2020)]
        today = pd.Timestamp.today()
        df["age"] = (today - df["birth"]).dt.days // 365
        min_age = int(df["age"].min()) // 5 * 5
        max_age = (int(df["age"].max()) // 5 + 1) * 5
        age_bins = list(range(min_age, max_age + 5, 5))
        df["age_group"] = pd.cut(df["age"], bins=age_bins, right=False)
        age_categories = df["age_group"].cat.categories[::-1]
        df["age_group"] = pd.Categorical(df["age_group"], categories=age_categories, ordered=True)
        pyramid = df.groupby(["age_group", "gender"]).size().reset_index(name="count")
        pyramid.loc[pyramid["gender"] == "male", "count"] *= -1
        sns.set_style("whitegrid")
        plt.figure(figsize=(8, 10))
        sns.barplot(data=pyramid, x="count", y="age_group", hue="gender", orient="h", dodge=False)
        plt.axvline(0, color="black", linewidth=0.8)
        plt.xlabel("Number of individuals")
        plt.ylabel("Age group")
        plt.title("Age Pyramid by Gender")
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()

# ---------------------------------------------------------------------------
# Report figures
# ---------------------------------------------------------------------------

class ReportFigureGenerator:
    """Reproduce figure generation for the final report."""

    def generate(self) -> None:
        asset_dir = Path("report_assets")
        asset_dir.mkdir(exist_ok=True)

        person_df = pd.read_csv("stock_analysis/output/person_stock_report.csv")
        plt.figure(figsize=(8, 6))
        plt.hist(person_df["total_valuation"] / 1e6, bins=50, color="steelblue", edgecolor="black")
        plt.xlabel("Total valuation (million €)")
        plt.ylabel("Number of declarants")
        plt.title("Distribution of total valuation among declarants")
        plt.tight_layout()
        plt.savefig(asset_dir / "fig1_asset_distribution.png")
        plt.close()

        norm_df = pd.read_csv("stock_analysis/output/normalized_stocks.csv")
        index_names = set(pd.read_csv("stock_analysis/output/indexes/cac40.csv")["clean_name"])
        index_names |= set(pd.read_csv("stock_analysis/output/indexes/sbf120.csv")["clean_name"])
        index_names |= set(pd.read_csv("stock_analysis/output/indexes/sp500.csv")["clean_name"])
        sector_df = norm_df[norm_df["clean_name"].isin(index_names)].copy()
        sector_map = {
            "CREDIT AGRICOLE": "Finance",
            "BNP PARIBAS": "Finance",
            "SOCIETE GENERALE": "Finance",
            "AXA": "Finance",
            "ENGIE": "Energy",
            "TOTALENERGIES": "Energy",
            "EDF": "Energy",
            "AIR LIQUIDE": "Industry",
            "VEOLIA": "Utilities",
            "ORANGE": "Telecom",
            "SANOFI": "Healthcare",
            "MICROSOFT": "Technology",
            "AMAZON": "Technology",
            "ACCENTURE": "Technology",
            "KRAFT HEINZ": "Consumer",
            "LINDE": "Industry",
        }
        sector_df["sector"] = sector_df["clean_name"].map(sector_map).fillna("Other")
        sector_counts = sector_df.groupby("sector")["evaluation"].sum().sort_values(ascending=False)
        plt.figure(figsize=(8, 6))
        sector_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90)
        plt.ylabel("")
        plt.title("Sector exposure of declared holdings")
        plt.tight_layout()
        plt.savefig(asset_dir / "fig2_sector_exposure.png")
        plt.close()

        spouse_df = pd.read_csv("spouse_occupation_gender_counts.csv")
        spouse_df["total"] = spouse_df["male"] + spouse_df["female"]
        top = spouse_df.nlargest(10, "total").set_index("occupation")[["male", "female"]]
        plt.figure(figsize=(8, 6))
        sns.heatmap(top, annot=True, fmt="d", cmap="Blues")
        plt.xlabel("Gender")
        plt.ylabel("Spouse occupation")
        plt.title("Gender distribution by spouse occupation (top 10)")
        plt.tight_layout()
        plt.savefig(asset_dir / "fig3_spouse_gender_heatmap.png")
        plt.close()
