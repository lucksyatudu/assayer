from typing import List
from src.claims.schema import Claim
from src.validation.schema import ClaimValidationResult
from src.web_search.utils import build_search_query
from src.web_search.search import web_search
from src.evidence.classify import classify_evidence
from src.llm_utils.get_sources import GeminiClaimValidator

async def validate_claims(claims: List[Claim]) -> List[ClaimValidationResult]:
    results = []
    llm = GeminiClaimValidator()

    for claim in claims:
        query = build_search_query(claim)
        search_results = web_search(query)

        if not search_results:
            results.append(
                ClaimValidationResult(
                    claim=claim,
                    score="Cannot Confidently Assess",
                    source=None,
                    evidence_snippet=None,
                )
            )
            continue

        supporting, contradicting = classify_evidence(claim, search_results)

        if supporting and not contradicting:
            score = "Accurate"
            best = supporting[0]

        elif contradicting and not supporting:
            score = "Inaccurate"
            best = contradicting[0]

        elif supporting and contradicting:
            score = "Disputed"
            best = supporting[0]

        else:
            # fallback to LLM
            llm_result = await llm.run(claim, supporting, contradicting)
            score = llm_result.get("score", "Cannot Confidently Assess")
            best = (supporting or contradicting or [None])[0]

        results.append(
            ClaimValidationResult(
                claim=claim,
                score=score,
                source=best.url if best else None,
                evidence_snippet=best.snippet if best else None,
            )
        )

    return results