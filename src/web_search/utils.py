from src.claims.schema import Claim

def build_search_query(claim: Claim) -> str:
    parts = []

    if claim.subject:
        parts.append(claim.subject)

    if claim.predicate:
        parts.append(claim.predicate)

    for token in claim.normalized_claim.split():
        if token.istitle() or token.isdigit():
            parts.append(token)

    return " ".join(parts[:12])
