HEDGES = {
    "may", "might", "could", "possibly", "likely", "unlikely",
    "appears", "suggests", "seems"
}

OPINION_MARKERS = {
    "i think", "i believe", "in my opinion", "we feel"
}

def modality_score(sentence: str) -> float:
    words = sentence.lower().split()
    hedge_count = sum(1 for w in words if w in HEDGES)
    return max(0.0, 1.0 - hedge_count * 0.15)


def is_pure_opinion(sentence: str) -> bool:
    s = sentence.lower()
    return any(p in s for p in OPINION_MARKERS)