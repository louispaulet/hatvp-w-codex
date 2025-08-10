"""Tests for local_llm.wikipedia_url."""

import json
from unittest.mock import patch

from local_llm.wikipedia_url import get_wikipedia_url


def mock_post(*args, **kwargs):
    class MockResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def iter_lines(self):
            yield json.dumps({"response": "https://en.wikipedia.org/wiki/Emmanuel_Macron"}).encode("utf-8")
            yield json.dumps({"done": True}).encode("utf-8")

    return MockResponse()


def test_get_wikipedia_url_returns_url():
    with patch("local_llm.wikipedia_url.requests.post", mock_post):
        url = get_wikipedia_url("Emmanuel", "Macron")
    assert url == "https://en.wikipedia.org/wiki/Emmanuel_Macron"
