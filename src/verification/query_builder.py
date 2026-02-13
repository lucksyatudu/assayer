def build_search_queries(canonical_claim: dict) -> list[str]:
    """
    Builds multiple safe queries from canonical claim.
    """

    base = f"{canonical_claim['subject']} {canonical_claim['object']}"

    queries = [
        base,
        f"{canonical_claim['subject']} identity",
        f"{base} official source",
        f"{canonical_claim['subject']} {canonical_claim['domain_hint']}"
    ]

    return queries
