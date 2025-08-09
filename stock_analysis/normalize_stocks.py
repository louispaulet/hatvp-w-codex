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


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base / 'stock_extract' / 'stocks.csv')
    df['clean_name'] = df['nomSociete'].apply(clean_name)
    df = df[~df['clean_name'].isin(PLACEHOLDER_NAMES)]
    df = df[~df['clean_name'].str.contains('DONNEE', na=False)]
    df = df[~df['clean_name'].str.contains('NON PUBLIE', na=False)]
    df['evaluation'] = df['evaluation'].astype(str)
    df = df[~df['evaluation'].str.contains('non', case=False, na=False)]
    output_dir = base / 'stock_analysis' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / 'normalized_stocks.csv', index=False)


if __name__ == '__main__':
    main()
