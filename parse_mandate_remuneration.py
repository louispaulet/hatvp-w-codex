from __future__ import annotations
import csv
import sys
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_mandats(xml_file: Path) -> list[dict]:
    """Extract mandate remuneration details from a declaration XML file."""
    try:
        root = ET.parse(xml_file).getroot()
    except ET.ParseError:
        return []

    rows: list[dict] = []
    # Iterate over each mandat item
    for item in root.findall(".//mandatElectifDto/items/items"):
        description = (item.findtext("descriptionMandat", default="") or "").strip()
        date_debut = (item.findtext("dateDebut", default="") or "").strip()
        date_fin = (item.findtext("dateFin", default="") or "").strip()

        # Skip mandates missing core fields
        if not description or not date_debut or not date_fin:
            print(
                f"Skipping mandat with missing fields in {xml_file.name}",
                file=sys.stderr,
            )
            continue

        montant_container = item.find("remuneration/montant")
        montant_items = (
            montant_container.findall("montant") if montant_container is not None else []
        )

        if not montant_items:
            print(
                f"No remuneration entries for mandat '{description}' in {xml_file.name}",
                file=sys.stderr,
            )
            rows.append(
                {
                    "file": xml_file.name,
                    "descriptionMandat": description,
                    "dateDebut": date_debut,
                    "dateFin": date_fin,
                    "annee": "",
                    "montant": "",
                }
            )
            continue

        for m in montant_items:
            year = (m.findtext("annee", default="") or "").strip()
            amount = (m.findtext("montant", default="") or "").strip()
            if not year or not amount:
                print(
                    f"Skipping incomplete remuneration entry for mandat '{description}' in {xml_file.name}",
                    file=sys.stderr,
                )
                continue
            rows.append(
                {
                    "file": xml_file.name,
                    "descriptionMandat": description,
                    "dateDebut": date_debut,
                    "dateFin": date_fin,
                    "annee": year,
                    "montant": amount,
                }
            )
    return rows


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    decl_dir = Path("split_declarations")
    all_rows: list[dict] = []
    for xml_file in sorted(decl_dir.glob("*.xml")):
        all_rows.extend(parse_mandats(xml_file))

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["file", "descriptionMandat", "dateDebut", "dateFin", "annee", "montant"],
    )
    writer.writeheader()
    for row in all_rows:
        writer.writerow(row)


if __name__ == "__main__":
    main()
