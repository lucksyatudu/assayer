def extract_relevant_evidence(page_text: str, canonical_claim: dict) -> list[str]:
    """
    Extracts sentences mentioning claim entities and predicates.
    """

    evidence = []
    for sent in split_sentences(page_text):
        if canonical_claim["subject"].lower() in sent.lower():
            evidence.append(sent)

    return evidence[:5]
