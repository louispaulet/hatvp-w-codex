from pathlib import Path
import pandas as pd


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    stocks_path = base / 'stock_analysis' / 'output' / 'normalized_stocks.csv'
    pii_path = base / 'pii' / 'personal_info.csv'
    stocks_df = pd.read_csv(stocks_path)
    pii_df = pd.read_csv(pii_path, usecols=['uuid', 'nom', 'prenom'])
    merged = stocks_df.merge(pii_df, on='uuid', how='left')
    merged['evaluation'] = pd.to_numeric(merged['evaluation'], errors='coerce')
    report = (
        merged.groupby(['uuid', 'nom', 'prenom'])
        .agg(
            stock_count=('nomSociete', 'count'),
            average_valuation=('evaluation', 'mean'),
            total_valuation=('evaluation', 'sum'),
            min_valuation=('evaluation', 'min'),
            max_valuation=('evaluation', 'max'),
        )
        .reset_index()
    )
    report = report.sort_values('total_valuation', ascending=False)
    output_dir = base / 'stock_analysis' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    report.to_csv(output_dir / 'person_stock_report.csv', index=False)
    print(report.head(10))


if __name__ == '__main__':
    main()
