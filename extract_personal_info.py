"""Extract personal information from HATVP declaration files.

Each file is an XML document in which a ``<declaration>`` element may
contain a ``<general>`` child, itself optionally nesting a ``<declarant>``
element with the person's details:

``<declaration>``
└─ ``<general>``
   └─ ``<declarant>``
      ├─ ``<civilite>``
      ├─ ``<nom>``
      ├─ ``<prenom>``
      ├─ ``<email>``
      └─ ``<dateNaissance>``

Missing elements simply yield blank fields, while duplicated
``<declaration>``, ``<general>`` or ``<declarant>`` tags raise a
``ValueError``. Completely invalid XML is also surfaced as a
``ValueError`` rather than crashing the script.
"""

import csv
from pathlib import Path
import xml.etree.ElementTree as ET


def extract_personal_info(xml_path: Path) -> dict:
    """Parse ``xml_path`` and return a mapping of personal fields.

    Parameters
    ----------
    xml_path:
        Path to a declaration XML file.

    Returns
    -------
    dict
        Dictionary containing ``file``, ``dateDepot``, ``uuid``,
        ``civilite``, ``nom``, ``prenom``, ``email`` and ``dateNaissance``.

    Error Handling
    --------------
    * If the XML is malformed, ``ValueError`` is raised with a description of
      the parsing problem.
    * If more than one ``<declaration>``, ``<general>`` or ``<declarant>``
      element is encountered, ``ValueError`` is raised to avoid ambiguity.
    * When any of these elements are missing, their associated fields are
      returned as empty strings instead of raising an error.
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
    general = get_unique_desc(declaration, "general")
    declarant = get_unique_desc(general, "declarant")

    def get_text(element, tag):
        if element is None:
            return ""
        text = element.findtext(tag, default="")
        return text.strip() if text else ""

    info = {
        "file": xml_path.name,
        "dateDepot": get_text(declaration, "dateDepot"),
        "uuid": get_text(declaration, "uuid"),
        "civilite": get_text(declarant, "civilite"),
        "nom": get_text(declarant, "nom"),
        "prenom": get_text(declarant, "prenom"),
        "email": get_text(declarant, "email"),
        "dateNaissance": get_text(declarant, "dateNaissance"),
    }
    return info


def main() -> None:
    decl_dir = Path("split_declarations")
    output_file = Path("personal_info.csv")
    fieldnames = [
        "file",
        "dateDepot",
        "uuid",
        "civilite",
        "nom",
        "prenom",
        "email",
        "dateNaissance",
    ]

    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for xml_file in sorted(decl_dir.glob("*.xml")):
            info = extract_personal_info(xml_file)
            writer.writerow(info)


if __name__ == "__main__":
    main()
