"""Parse financial participations from declaration XML files."""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Iterator


def parse_file(path: Path) -> Iterator[dict]:
    tree = ET.parse(path)
    root = tree.getroot()
    dto = root.find("participationFinanciereDto")
    if dto is None:
        return iter(())
    for item in dto.findall("./items/items"):
        yield {
            "file": path.name,
            "nomSociete": item.findtext("nomSociete", default=""),
            "evaluation": item.findtext("evaluation", default=""),
            "capitalDetenu": item.findtext("capitalDetenu", default=""),
            "nombreParts": item.findtext("nombreParts", default=""),
            "remuneration": item.findtext("remuneration", default=""),
        }
