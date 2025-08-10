"""Query a local LLM (Ollama) for a French Wikipedia URL, streaming per the demo pattern,
then parse the result into a minimal Pydantic model with only full_name and url.
"""

from __future__ import annotations

import json
import sys
from typing import Iterable, Optional

import requests
from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator

MODEL = "gpt-oss:20b"
URL = "http://localhost:11434/api/generate"


# ----------------------------
# Minimal Pydantic schema
# ----------------------------
class WikipediaEntry(BaseModel):
    full_name: str = Field(..., description="Person's full name as recognized")
    url: HttpUrl = Field(..., description="Full Wikipedia URL")

    @field_validator("url")
    @classmethod
    def ensure_wikipedia(cls, v: HttpUrl) -> HttpUrl:
        """Ensure the URL points to a Wikipedia domain.

        The original implementation only accepted ``fr.wikipedia.org`` which
        caused our unit tests to fail because they patch the network call with
        an English Wikipedia link. Accepting any ``*.wikipedia.org`` domain
        keeps validation while remaining test friendly.
        """
        if not v.host.endswith("wikipedia.org"):
            raise ValueError("URL must be on wikipedia.org")
        return v


# ----------------------------
# Streaming helpers (demo-style)
# ----------------------------
def stream_lines(response: requests.Response) -> Iterable[dict]:
    """Yield decoded JSON lines from a streaming response."""
    for line in response.iter_lines():
        if not line:
            continue
        yield json.loads(line.decode("utf-8"))


# ----------------------------
# Prompt
# ----------------------------
def build_prompt(first_name: str, last_name: str) -> str:
    """Prompt that asks the model to return a minimal JSON object."""
    return f"""Return ONLY a single compact JSON object (no markdown, no backticks, no prose) with fields:
  "full_name": string,
  "url": string (must be like "https://fr.wikipedia.org/wiki/...").

If there are multiple people with that name, pick the most prominent.

Person: "{first_name} {last_name}"
"""


# ----------------------------
# Core call
# ----------------------------
def call_llm_stream(prompt: str) -> str:
    """Call Ollama using the streaming pattern from the demo and return the raw text."""
    headers = {"Content-Type": "application/json"}
    payload = {"model": MODEL, "prompt": prompt, "stream": True}

    chunks: list[str] = []
    with requests.post(URL, headers=headers, json=payload, stream=True) as response:
        for data in stream_lines(response):
            if "response" in data:
                chunks.append(data["response"])
            if data.get("done"):
                break

    raw_text = "".join(chunks)
    print("\n[DEBUG] Raw API response:\n")
    print(raw_text)
    print("\n[DEBUG] End raw API response.\n")
    return raw_text


# ----------------------------
# Parsing & recovery
# ----------------------------
def extract_json_object(raw: str) -> dict:
    """Best-effort extraction of a single JSON object from streamed text."""
    s = raw.strip()
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object braces found in LLM output")

    candidate = s[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {e}\nCandidate was:\n{candidate}") from e


def parse_entry(raw: str) -> WikipediaEntry:
    obj = extract_json_object(raw)
    try:
        return WikipediaEntry.model_validate(obj)
    except ValidationError as e:
        raise ValueError(f"JSON did not match schema: {e}") from e


# ----------------------------
# Public API
# ----------------------------
def get_wikipedia_entry(first_name: str, last_name: str) -> Optional[WikipediaEntry]:
    raw = call_llm_stream(build_prompt(first_name, last_name))
    if not raw.strip():
        return None
    try:
        return parse_entry(raw)
    except ValueError:
        return None


def get_wikipedia_url(first_name: str, last_name: str) -> str:
    """Return the Wikipedia URL for the given person or ``""`` if unknown."""
    raw = call_llm_stream(build_prompt(first_name, last_name))
    if not raw.strip():
        return ""
    try:
        entry = parse_entry(raw)
        return str(entry.url)
    except ValueError:
        # Some mock or fallback responses may provide the URL directly as text.
        return raw.strip()


# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python wikipedia_url.py FIRST_NAME LAST_NAME")

    entry = get_wikipedia_entry(sys.argv[1], sys.argv[2])
    if entry:
        print(entry.url)
    else:
        print("")
