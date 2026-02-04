ATTRIBUTION_VERBS = {
    "said", "reported", "claimed", "announced", "stated", "argued"
}

def is_attributed_claim(doc) -> bool:
    return any(
        token.lemma_ in ATTRIBUTION_VERBS
        for token in doc
    )
