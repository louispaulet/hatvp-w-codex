from pathlib import Path

import pandas as pd

from stock_analysis.filter_by_index import load_index_df


def test_filter_by_index(tmp_path):
    base = Path(__file__).resolve().parent
    cleaned = pd.read_csv(base / 'output' / 'normalized_stocks.csv', usecols=['clean_name'])
    index_df = load_index_df('cac40')

    in_index = cleaned[cleaned['clean_name'].isin(index_df['clean_name'])].head(1)
    not_in_index = cleaned[~cleaned['clean_name'].isin(index_df['clean_name'])].head(1)

    assert not in_index.empty and not not_in_index.empty

    sample = pd.concat([in_index, not_in_index])
    filtered = sample.merge(index_df, on='clean_name', how='inner')

    out_file = tmp_path / 'cac40.csv'
    filtered.to_csv(out_file, index=False)

    result = pd.read_csv(out_file)
    expected_names = set(in_index['clean_name'])
    result_names = set(result['clean_name'])

    assert result_names == expected_names
