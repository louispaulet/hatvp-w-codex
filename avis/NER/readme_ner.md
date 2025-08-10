# HATVP NER Entity Extraction – Quick Overview

## 📄 Files Description

- **`per_entities.csv`**  
  Extracted using **spaCy**’s Named Entity Recognition (NER) model on **526 HATVP decisions**.  
  Focus: `PER` (person) entities only, taken from the **TXT files** produced by OCR of the original PDFs.

- **`cleaned_entities.csv`**  
  A **ChatGPT-5**–processed version of `per_entities.csv` that:
  - Removes exact and near duplicates  
  - Normalizes formatting (consistent capitalization, spacing, etc.)  
  - Merges obvious variants of the same entity name  

- **`organizations.csv`** & **`people.csv`**  
  Derived from `cleaned_entities.csv` by **ChatGPT-5**, splitting entities into:
  - **Organizations** (companies, associations, institutions)  
  - **People** (individual names)

## 🎯 Purpose

This is an **initial exploration step** to:
1. Identify **important named entities** present in HATVP decisions.
2. Provide a **clean, structured list** of people and organizations for further analysis.
3. Lay the groundwork for building a **searchable database** of entities linked to decisions.

⚠️ **Note:** This is **not a finalized dataset** — it is an early pass for **data discovery and scoping**.  
Further work will involve:
- Improving NER precision and recall
- Linking entities across decisions
- Adding metadata (roles, dates, relationships)
- Validating against external authoritative datasets
