#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

INPUT_FILE = "declarations.xml"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def localname(tag: str) -> str:
    """Strip XML namespace from a tag."""
    return tag.split("}", 1)[-1] if "}" in tag else tag

def child_text(parent: ET.Element, wanted: str):
    """Get direct child text by tag name."""
    for ch in parent:
        if localname(ch.tag) == wanted:
            return (ch.text or "").strip()
    return ""

# First, count declarations for tqdm
print("Counting declarations...")
total = sum(1 for _, elem in ET.iterparse(INPUT_FILE, events=("end",)) if localname(elem.tag) == "declaration")

# Now process and split
print("Splitting...")
root = None
with tqdm(total=total, unit="decl") as pbar:
    for event, elem in ET.iterparse(INPUT_FILE, events=("start", "end")):
        if event == "start" and root is None:
            root = elem  # capture the root (<declarations>)
        if event == "end" and localname(elem.tag) == "declaration":
            uuid = child_text(elem, "uuid")
            version = child_text(elem, "declarationVersion")
            if uuid and version:
                filename = f"{uuid}-{version}.xml"
                path = os.path.join(OUTPUT_DIR, filename)
                # Wrap in <declarations> for valid XML
                wrapper = ET.Element("declarations")
                wrapper.append(ET.fromstring(ET.tostring(elem, encoding="utf-8")))
                ET.ElementTree(wrapper).write(path, encoding="utf-8", xml_declaration=True)
            pbar.update(1)
            # Free memory
            if root is not None:
                try:
                    root.remove(elem)
                except ValueError:
                    elem.clear()
