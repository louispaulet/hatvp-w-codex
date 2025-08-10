# MBA-Style Dossier
**Risk Exposure of Declarants in the HATVP Database**

## 1. Executive Summary
- The dataset covers 2,607 declarants with combined stock valuations exceeding €2.05 billion and median individual holdings of €12,192.
- Concentrated positions in major regulated firms—Credit Agricole (214 declarations), Air Liquide (136), Orange (128), Engie (125)—signal heightened conflict-of-interest exposure.

## 2. Introduction & Methodology
- HATVP requires French public officials to file asset and interest declarations (Law n°2013‑907 and Law n°2016‑1691).
- Data sources: `person_stock_report.csv`, `normalized_stocks.csv`, index membership files (`cac40.csv`, `sbf120.csv`, `sp500.csv`), and `spouse_occupation_gender_counts.csv`.
- Risk assessment follows COSO internal control and OECD anti-corruption guidance.

## 3. Macroeconomic & Regulatory Context
- French and EU frameworks mandate transparency and anti-corruption safeguards.
- Historical scandals (e.g., Thomas Thévenoud, François Fillon) highlight reputational fallout from disclosure gaps.

## 4. Risk Typology & Assessment Criteria
- **Financial**: outlier valuations or rapid wealth growth.
- **Reputational**: media scrutiny of holdings in strategic sectors.
- **Ethical/Conflict-of-interest**: equity ties to regulated industries.
- **Operational/Political**: investigations leading to sanctions or resignations.

## 5. Data-Driven Analysis
### 5.1 Distribution of assets
- Total valuation: €2,051,113,142 with a highly skewed distribution (median €12,192, max €303 million).
- **Figure 1** illustrates the distribution of total valuation across declarants.

### 5.2 Sectoral exposure
- Holdings cluster in finance, energy, telecom, and utilities.
- **Figure 2** shows the proportion of declared valuations by sector for index-listed companies.

### 5.3 International exposure
- 43 declarants hold S&P 500 stocks, notably Microsoft, Amazon, and Kraft Heinz.

### 5.4 Spousal occupations
- “Neant” (unspecified) is the most frequent spousal occupation label (266 male, 649 female entries), limiting transparency.

### 5.5 Illustrative graphs and heatmaps
![Figure 1: Asset distribution histogram](report_assets/fig1_asset_distribution.png)

![Figure 2: Sector exposure pie chart](report_assets/fig2_sector_exposure.png)

![Figure 3: Gender distribution heatmap for spouse occupations](report_assets/fig3_spouse_gender_heatmap.png)

## 6. High-Risk Profiles & Case Studies
- Outlier wealth figures (e.g., Philippe Briand, Roger Pellenc) merit enhanced scrutiny.
- Energy-sector overlaps (local officials holding Engie or TotalEnergies shares) risk policy capture.

## 7. Risk Mitigation & Governance Recommendations
- Enhance disclosure granularity for assets and spousal occupations.
- Require interim updates and conflict-of-interest training.
- Adapt best practices from U.S. blind trusts, U.K. frequent updates, and Canadian ethics audits.

## 8. Appendices
- Data tables, methodology notes, and glossary as referenced in main text.

## Notes
Run `python generate_report_figures.py` to generate Figures 1–3 into the `report_assets/` directory.
