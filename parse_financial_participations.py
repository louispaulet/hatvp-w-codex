import sys
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


def child_text(parent: ET.Element, tag: str) -> str:
    """Get direct child text by tag name (namespace agnostic)."""
    child = find_child(parent, tag)
    if child is not None and child.text:
        return child.text.replace("\n", " ").strip()
    return ""


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
    paths = sorted(Path("split_declarations").glob("*.xml"))
    writer = csv.DictWriter(sys.stdout, fieldnames=[
        "file", "nomSociete", "evaluation", "capitalDetenu", "nombreParts", "remuneration"
    ])
    writer.writeheader()
    for path in paths:
        for row in parse_file(path):
            writer.writerow(row)


if __name__ == "__main__":
    main()
