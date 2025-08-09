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
├── LICENSE
├── README.md
├── extract_personal_info.py
├── ocr_pdf_downloads.py
├── liste.csv
├── pii/
│   └── personal_info.csv
├── pdf_downloads/             # source PDFs
├── script_to_split_declarations.py
├── split_declarations/        # individual declaration XML files (omitted)
├── stock_analysis/
│   ├── filter_by_index.py
│   ├── normalize_stocks.py
│   └── output/
└── stock_extract/
    ├── extract_stocks.py
    └── stocks.csv
```

The listing above omits the many XML files under `split_declarations/`, which contains the sample declaration dataset.

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

