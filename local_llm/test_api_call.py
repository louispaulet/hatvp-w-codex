"""
Sample run output:

PS C:\Users\USERNAME\Documents\projets\hatvp-w-codex\local_llm> python .\test_api_call.py
- **Conception & Development (1961-1969)** – President John F. Kennedy pledged a crewed Moon landing by the end of the decade, leading to NASA’s Apollo program that built the Saturn V launch system, Gemini-tested rendezvous and EVA skills, and developed the Lunar Module (LM) for the first crewed Moon missions.

- **First Moon Landing & Manned Missions (1969-1972)** – Apollo 11’s *Tranquility Base* launch marked the first human Moon landing; subsequent flights (Apollo 12–17) achieved extensive surface exploration, sample return, and the only crewed extraterrestrial visits to the Moon.

- **Legacy & Conclusion (1973-1975)** – NASA shifted focus to cost-constrained programs, decommissioning Apollo after *Apollo 17*; the program’s technological breakthroughs (safety systems, guidance computers, high-strength materials) laid groundwork for modern spaceflight and left a permanent monument in the history of space exploration.
---
Tokens generated: 203
Elapsed time: 3.35 seconds
Tokens/sec: 60.66
"""

import requests
import time
import json

MODEL = "gpt-oss:20b"
PROMPT = "In exactly 3 bullet points, summarize the history of the Apollo program."

def main():
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "stream": True
    }

    token_count = 0
    start_time = None

    with requests.post(url, headers=headers, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                # Start timer on first token
                if start_time is None:
                    start_time = time.time()
                # Increment token count
                token_count += len(data["response"].split())

                # Print the token(s) as they come in
                print(data["response"], end="", flush=True)

            # End condition
            if data.get("done", False):
                break

    end_time = time.time()
    elapsed = end_time - start_time if start_time else 0

    print("\n---")
    print(f"Tokens generated: {token_count}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    if elapsed > 0:
        print(f"Tokens/sec: {token_count / elapsed:.2f}")

if __name__ == "__main__":
    main()
