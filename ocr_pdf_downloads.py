"""OCR PDFs in ``pdf_downloads`` and write text files.

This script uses ``ocrmypdf`` to extract searchable text from PDFs. For each
PDF found in ``pdf_downloads/``, it writes an OCR'd PDF and a ``.txt``
sidecar file to ``ocr_output/``.
"""

from pathlib import Path

import ocrmypdf


def ocr_pdf(pdf_path: Path, out_dir: Path) -> None:
    """Run OCR on ``pdf_path`` and save outputs to ``out_dir``."""
    out_pdf = out_dir / pdf_path.name
    sidecar = out_dir / f"{pdf_path.stem}.txt"
    ocrmypdf.ocr(
        str(pdf_path),
        str(out_pdf),
        sidecar=str(sidecar),
        language="fra",
        force_ocr=True,
    )


def main() -> None:
    input_dir = Path("pdf_downloads")
    output_dir = Path("ocr_output")
    output_dir.mkdir(exist_ok=True)

    for pdf_file in sorted(input_dir.glob("*.pdf")):
        print(f"Processing {pdf_file.name}")
        ocr_pdf(pdf_file, output_dir)


if __name__ == "__main__":
    main()
