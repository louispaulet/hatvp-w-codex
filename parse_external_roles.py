"""Parse external roles from declaration XML files."""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List


def parse_file(path: Path) -> List[List[str]]:
    tree = ET.parse(path)
    root = tree.getroot()
    rows: List[List[str]] = []

    def handle(dto_tag: str) -> None:
        dto = root.find(dto_tag)
        if dto is None:
            return
        for item in dto.findall("./items/items"):
            row = [
                path.name,
                dto_tag.replace("Dto", ""),
                item.findtext("nomStructure", default=""),
                item.findtext("descriptionActivite", default=""),
                (lambda v: str(float(v)) if v else "")(item.findtext("remuneration/montant", default="")),
                item.findtext("dateDebut", default=""),
                item.findtext("dateFin", default=""),
            ]
            rows.append(row)

    handle("participationDirigeantDto")
    handle("fonctionBenevoleDto")
    return rows
