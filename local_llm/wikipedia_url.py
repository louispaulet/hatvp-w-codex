"""Utilities for querying a local LLM for Wikipedia URLs."""

from __future__ import annotations

import json
from typing import Iterable

import requests

MODEL = "gpt-oss:20b"
URL = "http://localhost:11434/api/generate"


def stream_lines(response: requests.Response) -> Iterable[dict]:
    """Yield decoded JSON objects from a streaming response."""
    for line in response.iter_lines():
        if not line:
            continue
        yield json.loads(line.decode("utf-8"))


def build_prompt(first_name: str, last_name: str) -> str:
    """Return a prompt asking for the person's Wikipedia URL."""
    return (
        "Provide the full English Wikipedia URL for the public figure named "
        f"{first_name} {last_name}. If you are unsure, respond with 'None'."
    )


def get_wikipedia_url(first_name: str, last_name: str) -> str:
    """Use the local LLM to retrieve a Wikipedia URL for a person."""
    payload = {
        "model": MODEL,
        "prompt": build_prompt(first_name, last_name),
        "stream": True,
    }
    headers = {"Content-Type": "application/json"}

    result: list[str] = []
    try:
        with requests.post(URL, headers=headers, json=payload, stream=True, timeout=120) as response:
            for data in stream_lines(response):
                if "response" in data:
                    result.append(data["response"])
                if data.get("done"):
                    break
    except requests.RequestException:
        return ""

    return "".join(result).strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("Usage: python wikipedia_url.py FIRST_NAME LAST_NAME")

    print(get_wikipedia_url(sys.argv[1], sys.argv[2]))
