from typing import List
from src.claims.extractor import extract_claims
from src.claims.schema import Claim

def run_claim_pipeline(text: str) -> List[Claim]:
    claims = extract_claims(text)

    return [
        c for c in claims
        if c.is_claim
        and c.claim_strength >= 0.6
        and c.verifiability >= 0.6
    ]
