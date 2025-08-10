import csv
from pathlib import Path
import spacy

# Load spaCy French model
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    from spacy.cli import download
    download("fr_core_news_sm")
    nlp = spacy.load("fr_core_news_sm")

# Directory containing OCR text files
input_dir = Path("avis/ocr_output")
# Output CSV path
output_csv = Path("avis/per_entities.csv")

rows = []
for file_path in sorted(input_dir.glob("*.txt")):
    text = file_path.read_text(encoding="utf-8")
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PER":
            entity_text = ent.text.replace("\n", " ").strip()
            rows.append({"file": file_path.name, "entity": entity_text})

# Write results to CSV
with output_csv.open("w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["file", "entity"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Extracted {len(rows)} PER entities to {output_csv}")
