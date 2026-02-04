from pydantic import BaseModel
from typing import Optional

class Claim(BaseModel):
    original_sentence: str        # untouched sentence from text
    normalized_claim: str         # pruned / canonical form

    is_claim: bool
    claim_strength: float         # 0–1
    verifiability: float          # 0–1

    subject: Optional[str] = None
    predicate: Optional[str] = None
