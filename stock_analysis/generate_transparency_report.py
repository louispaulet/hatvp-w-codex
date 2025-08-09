from pathlib import Path
import pandas as pd


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    report_path = base / "stock_analysis" / "output" / "person_stock_report.csv"
    df = pd.read_csv(report_path)

    df["total_valuation"] = pd.to_numeric(df["total_valuation"], errors="coerce").fillna(0)
    df_sorted = df.sort_values("total_valuation", ascending=False)

    top10 = df_sorted.head(10)[["nom", "prenom", "stock_count", "total_valuation"]]
    bottom10 = df_sorted.tail(10)[["nom", "prenom", "stock_count", "total_valuation"]]

    summary = {
        "total_people": len(df_sorted),
        "aggregate_valuation": df_sorted["total_valuation"].sum(),
        "average_valuation": df_sorted["total_valuation"].mean(),
    }

    lines = [
        "# Transparency Report on Public Officials' Holdings",
        "",
        f"Total people analyzed: {summary['total_people']}",
        f"Aggregate valuation (EUR): {summary['aggregate_valuation']:.2f}",
        f"Average valuation per person (EUR): {summary['average_valuation']:.2f}",
        "",
        "## Top 10 by Total Valuation",
        top10.to_markdown(index=False),
        "",
        "## Bottom 10 by Total Valuation",
        bottom10.to_markdown(index=False),
        "",
    ]

    output_path = base / "stock_analysis" / "output" / "public_holdings_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote report to {output_path}")


if __name__ == "__main__":
    main()
