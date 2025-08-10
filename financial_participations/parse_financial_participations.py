import csv
from pathlib import Path
import xml.etree.ElementTree as ET


def localname(tag: str) -> str:
    """Return tag name without namespace."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def find_child(parent: ET.Element, wanted: str):
    """Return first child element with given localname."""
    for ch in parent:
        if localname(ch.tag) == wanted:
            return ch
    return None


def clean_text(s: str) -> str:
    """Normalize whitespace and special spaces."""
    if not s:
        return ""
    return (
        s.replace("\u202f", " ")  # narrow no-break space
         .replace("\u00a0", " ")  # no-break space
         .replace("\n", " ")
         .strip()
    )


def child_text(parent: ET.Element, tag: str) -> str:
    """Get direct child text by tag name (namespace agnostic)."""
    child = find_child(parent, tag)
    return clean_text(child.text) if (child is not None and child.text) else ""


def parse_file(path: Path):
    """Yield dictionaries for each participationFinanciere item in a file."""
    tree = ET.parse(path)
    root = tree.getroot()
    for pf in root.iter():
        if localname(pf.tag) != "participationFinanciereDto":
            continue
        items_container = find_child(pf, "items")
        if items_container is None:
            continue
        for item in items_container:
            if localname(item.tag) != "items":
                continue
            yield {
                "file": path.name,
                "nomSociete": child_text(item, "nomSociete"),
                "evaluation": child_text(item, "evaluation"),
                "capitalDetenu": child_text(item, "capitalDetenu"),
                "nombreParts": child_text(item, "nombreParts"),
                "remuneration": child_text(item, "remuneration"),
            }


def main() -> None:
    input_dir = Path("split_declarations")
    output_csv = Path("participations.csv")

    paths = sorted(input_dir.glob("*.xml"))
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["file", "nomSociete", "evaluation", "capitalDetenu", "nombreParts", "remuneration"]
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for path in paths:
            try:
                for row in parse_file(path):
                    writer.writerow(row)
            except ET.ParseError as e:
                print(f"Warning: failed to parse {path.name}: {e}")

    print(f"✅ Wrote {output_csv}")


if __name__ == "__main__":
    main()
