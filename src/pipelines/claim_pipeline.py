from typing import List
from src.claims.extractor import extract_claims
from src.claims.schema import Claim
from src.validation.validate import validate_claims

async def run_claim_pipeline(text: str):
    claims = extract_claims(text)

    filtered = [
        c for c in claims
        if c.is_claim
        and c.claim_strength >= 0.6
        and c.verifiability >= 0.6
    ]

    return await validate_claims(filtered)
