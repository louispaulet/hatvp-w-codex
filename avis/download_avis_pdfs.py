import time
import requests
from tqdm import tqdm
from pathlib import Path

# Read URLs from file (strip whitespace, skip empty lines)
with open("avis_links_bs4.txt", "r", encoding="utf-8") as f:
    pdf_urls = [line.strip() for line in f if line.strip()]

# Output folder
output_dir = Path("pdf_downloads")
output_dir.mkdir(exist_ok=True)

for url in tqdm(pdf_urls, desc="Downloading PDFs", unit="file"):
    try:
        filename = url.split("/")[-1] or "file.pdf"
        filepath = output_dir / filename
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        time.sleep(0.5)  # Wait 500 ms
    except Exception as e:
        tqdm.write(f"Error downloading {url}: {e}")
