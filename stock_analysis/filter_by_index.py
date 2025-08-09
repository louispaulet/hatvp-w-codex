import pandas as pd
from pathlib import Path
from normalize_stocks import clean_name

INDEX_FILES = {
    'cac40': 'cac40.csv',
    'sbf120': 'sbf120.csv',
    'sp500': 'sp500.csv',
}


def load_index_df(index: str) -> pd.DataFrame:
    base = Path(__file__).resolve().parent / 'index_lists'
    path = base / INDEX_FILES[index]
    if index == 'sp500':
        df = pd.read_csv(path)
        df['name'] = df['Security']
    else:
        df = pd.read_csv(path)
    df['clean_name'] = df['name'].apply(clean_name)
    return df[['clean_name']]


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    cleaned = pd.read_csv(base / 'stock_analysis' / 'output' / 'normalized_stocks.csv')
    output_dir = base / 'stock_analysis' / 'output' / 'indexes'
    output_dir.mkdir(parents=True, exist_ok=True)

    for index in INDEX_FILES:
        path = Path(__file__).resolve().parent / 'index_lists' / INDEX_FILES[index]
        if not path.exists():
            continue
        idx_df = load_index_df(index)
        merged = cleaned.merge(idx_df, on='clean_name', how='inner')
        merged.to_csv(output_dir / f'{index}.csv', index=False)


if __name__ == '__main__':
    main()
