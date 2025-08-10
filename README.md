# HATVP with Codex

HATVP with Codex is an exploration of how OpenAI's Codex models can help analyse official French transparency reports. The goal is to automatically read declarations published by the *Haute Autorité pour la transparence de la vie publique* (HATVP) and produce structured summaries and insights.

## What is the HATVP?

The HATVP is an independent French authority that promotes transparency in public life by collecting and publishing declarations of interests and assets from elected officials and senior public servants. These disclosures help citizens understand potential conflicts of interest and foster trust in democratic institutions.

## Why transparency matters

Open access to information about public officials’ finances is a cornerstone of democratic accountability. By making disclosures easier to analyse, citizens, journalists and researchers can more effectively monitor how power is exercised and ensure that decisions are made in the public interest.

## About OpenAI Codex

OpenAI Codex is a model capable of understanding and generating code in many programming languages. In this project we investigate how Codex can be used to parse the XML declarations released by the HATVP and generate human‑readable reports or datasets that make the information more accessible.

## Repository structure

```text
.
├── avis/
├── pii/
├── report_assets/
├── split_declarations/
├── stock_analysis/
├── stock_extract/
├── generate_report_figures.py
├── script_to_split_declarations.py
└── README.md
```

The listing above omits the many XML files under `split_declarations/`, which contains the sample declaration dataset.

### Regenerating datasets and figures

The repository includes scripts to rebuild derived artifacts:

```bash
# Personal info dataset
python pii/extract_personal_info.py

# Stock analysis CSVs
python stock_analysis/normalize_stocks.py
python stock_analysis/generate_person_stock_report.py

# Figures for reports
python generate_report_figures.py
```

Outputs such as `pii/personal_info.csv`, files in `stock_analysis/output/` and images in `report_assets/` are generated locally and should not be committed.
Running `generate_person_stock_report.py` now also creates `person_stock_sector_report.csv` with valuations by sector and adds a Herfindahl index column to `person_stock_report.csv`.

## Stock holdings

The repository includes `stock_extract/stocks.csv` describing declared equity interests. After normalising company names and removing placeholder values, the dataset contains **8 145 entries** for **2 667 unique companies**.

Most frequently declared companies:

1. CREDIT AGRICOLE – 214 declarations
2. AIR LIQUIDE – 136
3. ORANGE – 128
4. ENGIE – 125
5. AXA – 95
6. AIRBUS – 89
7. SANOFI – 87
8. LVMH – 77
9. SOCIETE GENERALE – 76
10. EDF – 69

Index-based filtering shows the prominence of major market indices:

- **CAC40**: 1 913 stock records
- **SBF120**: 2 242 stock records
- **S&P 500**: 80 stock records (top holdings include Microsoft, Kraft Heinz, Linde, Accenture and Amazon)

Generated CSV outputs are stored under `stock_analysis/output/`, with subfolders for each index.

## Public holdings valuation

`stock_analysis/generate_transparency_report.py` aggregates declared equity valuations by person. The latest report covers **1 389 individuals** with a combined valuation of **€1 092 305 734** and an average of roughly **€786 397** per person. Top holdings include Philippe Briand (€303 454 971) and Roger Pellenc (€84 801 656), while some declarations report negligible or even negative valuations such as Chantal Deseyne (‑€3 473). See `stock_analysis/output/public_holdings_report.md` for complete rankings.

## Personal information and spouse activities

`extract_personal_info.py` parses each declaration XML file and writes basic
details—such as name, email and birth date—to `pii/personal_info.csv`.
Complementary information about declarants' partners can be gathered with
`extract_spouse_activity.py`, which saves results to
`pii/spouse_activities.csv`.

## Gender and age analysis

`gender_analysis.py` enriches the personal info dataset with gender
guesses derived from first names and summarises the distribution in
`pii/gender_report.md`. The output CSV is then reused by
`age_pyramid.py` to build the demographic chart `age_pyramid.png`.

The current dataset spans **11 990 records**, with gender guesses indicating **64.15 % male** and **35.85 % female** entries. Frequent first names include Jean (249), Philippe (205), Patrick (173) and Marie (147). See `pii/gender_report.md` for full tables.

## HATVP avis PDFs

The repository also includes tooling to work with HATVP deliberations and
opinions. `extract_avis_bs4.py` scans raw HTML pages stored in
`raw_avis/` and generates a list of PDF URLs in `avis_links_bs4.txt`.
These files can then be downloaded with `download_avis_pdfs.py`, which
saves them under `pdf_downloads/`.

## OCR of PDF downloads

The repository includes a `pdf_downloads/` folder with source PDFs. The script
`ocr_pdf_downloads.py` runs [ocrmypdf](https://ocrmypdf.readthedocs.io/) on
each file and writes an OCR-enhanced PDF plus a `.txt` sidecar to
`ocr_output/`.

Install the dependencies and run the script:

```bash
apt-get install -y tesseract-ocr tesseract-ocr-fra
pip install ocrmypdf
python ocr_pdf_downloads.py
```

