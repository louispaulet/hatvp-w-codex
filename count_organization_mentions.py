import pandas as pd
from pathlib import Path

def main():
    orgs_df = pd.read_csv('avis/NER/organizations.csv')
    org_names = orgs_df['name'].dropna().tolist()
    org_mentions = {name: set() for name in org_names}
    decl_dir = Path('split_declarations')
    for xml_file in decl_dir.glob('*.xml'):
        try:
            text = xml_file.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for name in org_names:
            if name in text:
                org_mentions[name].add(xml_file.name)
    data = []
    for name in org_names:
        files = sorted(org_mentions[name])
        data.append({'organization': name,
                     'mentions': len(files),
                     'filenames': ','.join(files)})
    result_df = pd.DataFrame(data)
    result_df.to_csv('organization_mentions.csv', index=False)

if __name__ == '__main__':
    main()
