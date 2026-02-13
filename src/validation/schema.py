from pydantic import BaseModel
from typing import Optional, Literal
from src.claims.schema import Claim

ValidationScore = Literal[
    "Inaccurate",
    "Unsupported",
    "Disputed",
    "Accurate",
    "Cannot Confidently Assess"
]

class ClaimValidationResult(BaseModel):
    claim: Claim
    score: ValidationScore
    source: Optional[str] = None
    evidence_snippet: Optional[str] = None