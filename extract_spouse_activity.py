"""Extract spouse activity information from HATVP declaration files.

Each declaration may contain an ``<activProfConjointDto>`` element that
lists the professional activity of the declarant's spouse:

``<declaration>``
└─ ``<activProfConjointDto>``
   └─ ``<items>``
      └─ ``<items>`` (repeated)
         ├─ ``<nomConjoint>``
         ├─ ``<employeurConjoint>``
         ├─ ``<activiteProf>``
         └─ ``<commentaire>``

The script extracts these fields along with the declaration ``uuid`` and
stores the results in ``pii/spouse_activities.csv``.
"""

import csv
from pathlib import Path
import xml.etree.ElementTree as ET


def extract_spouse_activities(xml_path: Path) -> list[dict]:
    """Return spouse activity entries from ``xml_path``.

    Parameters
    ----------
    xml_path:
        Path to a declaration XML file.

    Returns
    -------
    list[dict]
        Each dict contains ``uuid``, ``nomConjoint``, ``employeurConjoint``,
        ``activiteProf`` and ``commentaire`` for one spouse activity.
    """

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as exc:  # pragma: no cover - defensive
        raise ValueError(f"Invalid XML in {xml_path}: {exc}") from exc

    root = tree.getroot()

    def get_unique_desc(parent, tag):
        """Return a single descendant element or ``None`` if missing.

        Raises ``ValueError`` if more than one matching element is found.
        """

        if parent is None:
            return None
        elements = parent.findall(f".//{tag}")
        if len(elements) > 1:
            raise ValueError(f"Multiple <{tag}> elements found in {xml_path}")
        return elements[0] if elements else None

    declaration = root if root.tag == "declaration" else get_unique_desc(root, "declaration")
    uuid = declaration.findtext("uuid", default="").strip() if declaration is not None else ""

    activ_dto = get_unique_desc(declaration, "activProfConjointDto")
    if activ_dto is None:
        return []

    def clean(text: str) -> str:
        """Collapse internal whitespace and strip ends."""

        return " ".join(text.split()) if text else ""

    activities = []
    for item in activ_dto.findall("./items/items"):
        activities.append(
            {
                "uuid": uuid,
                "nomConjoint": clean(item.findtext("nomConjoint")),
                "employeurConjoint": clean(item.findtext("employeurConjoint")),
                "activiteProf": clean(item.findtext("activiteProf")),
                "commentaire": clean(item.findtext("commentaire")),
            }
        )

    return activities


def main() -> None:
    decl_dir = Path("split_declarations")

    output_dir = Path("pii")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "spouse_activities.csv"
    fieldnames = [
        "uuid",
        "nomConjoint",
        "employeurConjoint",
        "activiteProf",
        "commentaire",
    ]

    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for xml_file in sorted(decl_dir.glob("*.xml")):
            for activity in extract_spouse_activities(xml_file):
                writer.writerow(activity)


if __name__ == "__main__":
    main()
