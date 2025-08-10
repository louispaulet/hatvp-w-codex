import csv
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_remuneration(elem: ET.Element) -> str:
    total = 0.0
    if elem is None:
        return ""
    for m in elem.findall('.//montant'):
        if m.find('montant') is None and (m.text or '').strip():
            text = m.text.strip().replace(' ', '').replace(',', '.')
            try:
                total += float(text)
            except ValueError:
                continue
    return str(total) if total else ""


def parse_file(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    rows = []
    for item in root.findall('.//participationDirigeantDto/items/items'):
        organization = (
            item.findtext('nomSociete')
            or item.findtext('nomStructure')
            or item.findtext('organisme')
            or item.findtext('activite')
            or ''
        )
        role = (
            item.findtext('activite')
            or item.findtext('descriptionActivite')
            or item.findtext('fonctionDirigeant')
            or item.findtext('nomSociete')
            or ''
        )
        remuneration = parse_remuneration(item.find('remuneration'))
        date_debut = item.findtext('dateDebut') or ''
        date_fin = item.findtext('dateFin') or ''
        rows.append([
            path.name,
            'participationDirigeant',
            organization,
            role,
            remuneration,
            date_debut,
            date_fin,
        ])
    for item in root.findall('.//fonctionBenevoleDto/items/items'):
        organization = (
            item.findtext('nomStructure')
            or item.findtext('nomSociete')
            or item.findtext('organisme')
            or ''
        )
        role = (
            item.findtext('descriptionActivite')
            or item.findtext('activite')
            or ''
        )
        remuneration = parse_remuneration(item.find('remuneration'))
        date_debut = item.findtext('dateDebut') or ''
        date_fin = item.findtext('dateFin') or ''
        rows.append([
            path.name,
            'fonctionBenevole',
            organization,
            role,
            remuneration,
            date_debut,
            date_fin,
        ])
    return rows


def main():
    input_dir = Path('split_declarations')
    output_file = Path('participations.csv')

    # utf-8-sig so Excel reads it without mojibake
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(
            ['file', 'type', 'organization', 'role', 'remuneration', 'date_start', 'date_end']
        )
        for xml_file in sorted(input_dir.glob('*.xml')):
            for row in parse_file(xml_file):
                writer.writerow(row)


if __name__ == '__main__':
    main()
