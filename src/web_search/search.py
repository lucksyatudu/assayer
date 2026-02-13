from typing import List
from pydantic import BaseModel
from ddgs import DDGS


class SearchResult(BaseModel):
    url: str
    title: str
    snippet: str


def web_search(query: str, max_results: int = 5) -> List[SearchResult]:
    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    SearchResult(
                        url=r.get("href", ""),
                        title=r.get("title", ""),
                        snippet=r.get("body", ""),
                    )
                )

    except Exception as e:
        print("Search failed:", e)
        return []

    return results
