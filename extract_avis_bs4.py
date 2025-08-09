from pathlib import Path
from bs4 import BeautifulSoup


def extract_links(directory: str) -> list[str]:
    """Extract unique PDF links from raw HATVP avis HTML files using BeautifulSoup."""
    links = set()
    path = Path(directory)
    for html_file in sorted(path.glob("*Consulter les délibérations et avis.html")):
        with html_file.open("rb") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                links.add(href)
    return sorted(links)


def main():
    avis_dir = Path("raw_avis")
    links = extract_links(str(avis_dir))

    out_file = avis_dir / "avis_links_bs4.txt"
    out_file.write_text("\n".join(links) + "\n")

    old_links_path = avis_dir / "avis_links.txt"
    old_links = set(old_links_path.read_text().splitlines())
    new_links = set(links)

    missing_in_new = sorted(old_links - new_links)
    extra_in_new = sorted(new_links - old_links)

    print(f"BS4 extracted {len(new_links)} links")
    print(f"Existing list contains {len(old_links)} links")
    print(f"Missing in new list: {len(missing_in_new)}")
    print(f"Extra links in new list: {len(extra_in_new)}")

    if missing_in_new:
        print("\nMissing URLs:")
        for url in missing_in_new:
            print(url)
    if extra_in_new:
        print("\nExtra URLs:")
        for url in extra_in_new:
            print(url)


if __name__ == "__main__":
    main()
