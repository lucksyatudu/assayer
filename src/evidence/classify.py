# src/claims/evidence.py

from typing import List, Tuple
from src.claims.schema import Claim
from src.web_search.search import SearchResult

NEGATION_TERMS = {
    "false", "hoax", "incorrect", "misleading", "debunked", "not true"
}

def classify_evidence(
    claim: Claim,
    results: List[SearchResult],
) -> Tuple[List[SearchResult], List[SearchResult]]:
    supporting = []
    contradicting = []

    subj = (claim.subject or "").lower()
    pred = (claim.predicate or "").lower()

    for r in results:
        text = f"{r.title} {r.snippet}".lower()

        if subj and subj not in text:
            continue

        if pred and pred in text:
            supporting.append(r)
        elif any(term in text for term in NEGATION_TERMS):
            contradicting.append(r)

    return supporting, contradicting
