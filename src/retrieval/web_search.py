import os
import requests
from typing import List
from pydantic import BaseModel

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class SearchResult(BaseModel):
    url: str
    title: str
    snippet: str

def web_search(query: str, max_results: int = 5) -> List[SearchResult]:
    if not SERPAPI_KEY:
        return []

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": max_results,
    }

    resp = requests.get("https://serpapi.com/search", params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for r in data.get("organic_results", []):
        results.append(
            SearchResult(
                url=r.get("link"),
                title=r.get("title", ""),
                snippet=r.get("snippet", ""),
            )
        )

    return results
