from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
from PIL import Image

from full_pipeline import (
    DeclarationPipeline,
    GenderAnalyzer,
    SpouseOccupationAnalyzer,
    GenderDiscriminationAnalyzer,
    ReportFigureGenerator,
)


def _sort(df: pd.DataFrame, sort_cols: list[str]) -> pd.DataFrame:
    return df.sort_values(sort_cols).reset_index(drop=True)[sorted(df.columns)]


def _img_bytes(path: Path) -> bytes:
    with Image.open(path) as img:
        return img.tobytes()


def test_pii_pipeline_matches_existing():
    org_names = pd.read_csv("avis/NER/organizations.csv")["name"].dropna().tolist()
    people_names = pd.read_csv("avis/NER/people.csv")["name"].dropna().tolist()
    pipeline = DeclarationPipeline(Path("split_declarations"), org_names, people_names)
    data = pipeline.run()

    expected_personal = pd.read_csv("pii/personal_info.csv")
    assert_frame_equal(
        _sort(data.personal_info, ["file"]), _sort(expected_personal, ["file"])
    )

    expected_spouse = pd.read_csv("pii/spouse_activities.csv")
    assert _sort(
        data.spouse_activities,
        ["uuid", "nomConjoint", "employeurConjoint", "activiteProf", "commentaire"],
    ).shape == _sort(
        expected_spouse,
        ["uuid", "nomConjoint", "employeurConjoint", "activiteProf", "commentaire"],
    ).shape

    expected_org = pd.read_csv("organization_mentions.csv")[["organization", "mentions"]]
    assert_frame_equal(
        _sort(data.organization_mentions[["organization", "mentions"]], ["organization"]),
        _sort(expected_org, ["organization"]),
    )

    expected_people = pd.read_csv("people_mentions.csv")[["person", "mentions"]]
    assert_frame_equal(
        _sort(data.people_mentions[["person", "mentions"]], ["person"]),
        _sort(expected_people, ["person"]),
    )

    gendered = GenderAnalyzer().analyze(data.personal_info)
    expected_gendered = pd.read_csv("pii/personal_info_with_gender.csv")
    assert_frame_equal(
        _sort(gendered, ["file"]), _sort(expected_gendered, ["file"])
    )

    occ_counts, _ = SpouseOccupationAnalyzer().analyze(data.spouse_activities, gendered)
    expected_counts = pd.read_csv("pii/spouse_occupation_gender_counts.csv")
    assert_frame_equal(
        _sort(occ_counts, ["occupation"]), _sort(expected_counts, ["occupation"])
    )

    top_male, top_female, pay_summary = GenderDiscriminationAnalyzer().analyze(
        occ_counts
    )
    expected_top_male = pd.read_csv("pii/top_male_jobs.csv")
    expected_top_female = pd.read_csv("pii/top_female_jobs.csv")
    expected_pay_summary = pd.read_csv("pii/pay_grade_summary.csv", index_col=0)
    assert_frame_equal(
        _sort(top_male, ["occupation"]), _sort(expected_top_male, ["occupation"])
    )
    assert_frame_equal(
        _sort(top_female, ["occupation"]), _sort(expected_top_female, ["occupation"])
    )
    assert_frame_equal(pay_summary, expected_pay_summary)


def test_report_figure_generator_reproduces_reference_figures():
    dest = Path("spouse_occupation_gender_counts.csv")
    original_csv = dest.read_bytes() if dest.exists() else None
    dest.write_bytes(Path("pii/spouse_occupation_gender_counts.csv").read_bytes())

    figs = [
        Path("report_assets/fig1_asset_distribution.png"),
        Path("report_assets/fig2_sector_exposure.png"),
        Path("report_assets/fig3_spouse_gender_heatmap.png"),
    ]
    backups = {p: p.read_bytes() for p in figs}
    orig_pixels = {p: _img_bytes(p) for p in figs}
    try:
        ReportFigureGenerator().generate()
        for p in figs:
            assert _img_bytes(p) == orig_pixels[p]
    finally:
        for p in figs:
            p.write_bytes(backups[p])
        if original_csv is None:
            dest.unlink()
        else:
            dest.write_bytes(original_csv)
