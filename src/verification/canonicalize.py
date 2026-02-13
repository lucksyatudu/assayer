def canonicalize_claim(claim) -> dict:
    """
    Converts a claim into a privacy-safe factual representation.
    """

    return {
        "entities": [
            {"text": ent.text, "type": ent.label_}
            for ent in claim.doc.ents
        ],
        "subject": claim.subject,
        "predicate": claim.main_verb,
        "object": claim.object,
        "tense": claim.tense,
        "domain_hint": infer_domain(claim)
    }
