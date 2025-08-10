import pandas as pd
from pathlib import Path


def tally_mentions(names, decl_dir: Path, label: str) -> pd.DataFrame:
    """Count how many declaration XML files mention each name.

    Parameters
    ----------
    names : list[str]
        Names to search for within declaration files.
    decl_dir : Path
        Directory containing declaration XML files.
    label : str
        Column name for the entity (e.g., 'organization' or 'person').

    Returns
    -------
    pd.DataFrame
        DataFrame with columns [label, 'mentions', 'filenames'].
    """

    mentions = {name: set() for name in names}
    for xml_file in decl_dir.glob('*.xml'):
        try:
            text = xml_file.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for name in names:
            if name in text:
                mentions[name].add(xml_file.name)

    rows = []
    for name in names:
        files = sorted(mentions[name])
        rows.append({label: name,
                     'mentions': len(files),
                     'filenames': ','.join(files)})
    return pd.DataFrame(rows)


def main():
    decl_dir = Path('split_declarations')

    org_names = pd.read_csv('avis/NER/organizations.csv')['name'].dropna().tolist()
    org_df = tally_mentions(org_names, decl_dir, 'organization')
    org_df.to_csv('organization_mentions.csv', index=False)

    people_names = pd.read_csv('avis/NER/people.csv')['name'].dropna().tolist()
    people_df = tally_mentions(people_names, decl_dir, 'person')
    people_df.to_csv('people_mentions.csv', index=False)


if __name__ == '__main__':
    main()
