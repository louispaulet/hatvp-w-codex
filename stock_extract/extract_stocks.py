import csv
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_stock_info(xml_file: Path):
    """Extract stock-related information from a single declaration XML file."""
    try:
        root = ET.parse(xml_file).getroot()
    except ET.ParseError:
        return []

    declaration = root.find('.//declaration')
    if declaration is None:
        return []

    uuid = declaration.findtext('uuid', default='')
    pf = declaration.find('participationFinanciereDto')
    if pf is None:
        return []

    rows = []
    for item in pf.findall('./items/items'):
        row = {
            'uuid': uuid,
            'nomSociete': ' '.join((item.findtext('nomSociete', '') or '').split()),
            'evaluation': item.findtext('evaluation', ''),
            'capitalDetenu': item.findtext('capitalDetenu', ''),
            'nombreParts': item.findtext('nombreParts', ''),
            'commentaire': item.findtext('commentaire', ''),
            'remuneration': item.findtext('remuneration', ''),
        }
        rows.append(row)
    return rows

def main():
    base_path = Path(__file__).resolve().parent.parent
    declarations_dir = base_path / 'split_declarations'
    output_dir = base_path / 'stock_extract'
    output_dir.mkdir(exist_ok=True)

    all_rows = []
    for xml_path in declarations_dir.glob('*.xml'):
        all_rows.extend(extract_stock_info(xml_path))

    fieldnames = ['uuid', 'nomSociete', 'evaluation', 'capitalDetenu', 'nombreParts', 'commentaire', 'remuneration']
    output_file = output_dir / 'stocks.csv'
    with output_file.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

if __name__ == '__main__':
    main()
