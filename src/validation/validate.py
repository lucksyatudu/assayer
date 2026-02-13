from typing import List
from src.claims.schema import Claim
from src.validation.schema import ClaimValidationResult
from src.llm_utils.get_sources import GeminiClaimValidator


async def validate_claims(claims: List[Claim]) -> List[ClaimValidationResult]:
    results = []
    llm = GeminiClaimValidator()

    for claim in claims:
        llm_result = await llm.run(claim)

        results.append(
            ClaimValidationResult(
                claim=claim,
                score=llm_result.get("score", "Cannot Confidently Assess"),
                source=llm_result.get("source"),
                evidence_snippet=llm_result.get("evidence"),
            )
        )

    return results
