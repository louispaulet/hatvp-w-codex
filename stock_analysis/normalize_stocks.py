import pandas as pd
from pathlib import Path
import re
from unidecode import unidecode

LEGAL_FORMS = [
    ' SA', ' SAS', ' SASU', ' SARL', ' SE', ' SCA', ' SCS', ' SCI', ' GIE', ' SNC',
    ' EURL', ' SASP', ' LTD', ' PLC', ' INC', ' BV', ' NV', ' AG', ' GMBH'
]
PLACEHOLDER_NAMES = {
    'DONNEE NON PUBLIEE', 'DONNEES NON PUBLIEES', 'VALEUR NON DECLAREE',
    'VALEUR NON DECLAREE', 'SANS OBJET', 'NEANT', 'NON RENSEIGNE',
    'NON RENSEIGNEE', 'NC', 'NA'
}


def clean_name(name: str) -> str:
    if not isinstance(name, str):
        return ''
    name = unidecode(name).upper()
    for form in LEGAL_FORMS:
        name = re.sub(rf'{form}$', '', name)
    name = re.sub(r'[^A-Z0-9& ]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def map_sector(df: pd.DataFrame) -> pd.DataFrame:
    """Map company names to sector information from index lists.

    Parameters
    ----------
    df:
        DataFrame containing a ``clean_name`` column.

    Returns
    -------
    pd.DataFrame
        Original ``df`` with optional ``GICS`` sector columns joined.
    """

    index_dir = Path(__file__).resolve().parent / 'index_lists'
    sector_frames = []
    for path in index_dir.glob('*.csv'):
        idx_df = pd.read_csv(path)
        if 'Security' in idx_df.columns:
            name_col = 'Security'
        elif 'name' in idx_df.columns:
            name_col = 'name'
        else:
            continue

        sector_cols = [col for col in ['GICS Sector', 'GICS Sub-Industry'] if col in idx_df.columns]
        if not sector_cols:
            continue

        idx_df['clean_name'] = idx_df[name_col].apply(clean_name)
        sector_frames.append(idx_df[['clean_name'] + sector_cols])

    if not sector_frames:
        return df

    sectors = pd.concat(sector_frames, ignore_index=True).drop_duplicates('clean_name')
    return df.merge(sectors, on='clean_name', how='left')


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base / 'stock_extract' / 'stocks.csv')
    df['clean_name'] = df['nomSociete'].apply(clean_name)
    df = df[~df['clean_name'].isin(PLACEHOLDER_NAMES)]
    df = df[~df['clean_name'].str.contains('DONNEE', na=False)]
    df = df[~df['clean_name'].str.contains('NON PUBLIE', na=False)]
    df['evaluation'] = df['evaluation'].astype(str)
    df = df[~df['evaluation'].str.contains('non', case=False, na=False)]
    df = map_sector(df)
    output_dir = base / 'stock_analysis' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / 'normalized_stocks.csv', index=False)


if __name__ == '__main__':
    main()
