"""Simple test script for a local LLM API."""

import json
import time
from typing import Iterable

import requests

MODEL = "gpt-oss:20b"
PROMPT = "In exactly 3 bullet points, summarize the history of the Apollo program."


def stream_lines(response: requests.Response) -> Iterable[str]:
    """Yield decoded JSON lines from a streaming response."""

    for line in response.iter_lines():
        if not line:
            continue
        yield json.loads(line.decode("utf-8"))


def main() -> None:
    """Post a prompt to the local server and print streamed tokens."""

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"model": MODEL, "prompt": PROMPT, "stream": True}

    token_count = 0
    start_time = None

    with requests.post(url, headers=headers, json=payload, stream=True) as response:
        for data in stream_lines(response):
            if "response" in data:
                if start_time is None:
                    start_time = time.time()
                print(data["response"], end="", flush=True)
                token_count += 1
            if data.get("done"):
                break

    if start_time is None:
        return

    elapsed = time.time() - start_time
    print("\n---")
    print(f"Tokens generated: {token_count}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"Tokens/sec: {token_count / elapsed:.2f}")


if __name__ == "__main__":
    main()

