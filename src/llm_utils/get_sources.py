from typing import Dict, Any
from src.claims.schema import Claim
from src.llm_utils.gemini import BaseModel


VALID_LABELS = {
    "Inaccurate",
    "Unsupported",
    "Disputed",
    "Accurate",
    "Cannot Confidently Assess",
}


class GeminiClaimValidator(BaseModel):

    async def run(self, claim: Claim) -> Dict[str, Any]:
        prompt = self._build_prompt(claim)
        raw_output = ''
        try:
            raw_output = await self._generate(prompt)
        except Exception:
            pass
        return self._parse_output(raw_output)

    # ------------------------------------------------------------------ #
    # Prompt
    # ------------------------------------------------------------------ #

    def _build_prompt(self, claim: Claim) -> str:
        return f"""
        You are a professional fact-checking system.

        Your task:

        1. Perform a web search to verify the claim.
        2. Cross-check at least 2 independent reliable sources.
        3. Determine factual accuracy.
        4. Provide the most authoritative source URL.
        5. Quote a short supporting or contradicting snippet.

        Claim:
        "{claim.original_sentence}"

        Subject: {claim.subject}
        Predicate: {claim.predicate}

        Classify into EXACTLY one of:

        - Accurate
        - Inaccurate
        - Disputed
        - Unsupported
        - Cannot Confidently Assess

        Definitions:
        - Accurate → Strong evidence confirms claim.
        - Inaccurate → Strong evidence disproves claim.
        - Disputed → Credible sources disagree.
        - Unsupported → No reliable evidence exists.
        - Cannot Confidently Assess → Insufficient clarity.

        Return STRICTLY in this format:

        Score: <label>
        Reasoning: <2-4 sentence explanation>
        Source: <best URL>
        Evidence: <quoted snippet>
        """

    # ------------------------------------------------------------------ #
    # Parse
    # ------------------------------------------------------------------ #

    def _parse_output(self, text: str) -> Dict[str, Any]:
        score = None
        reasoning = None
        source = None
        evidence = None

        for line in text.splitlines():
            lower = line.lower()

            if lower.startswith("score:"):
                score = line.split(":", 1)[1].strip()

            elif lower.startswith("reasoning:"):
                reasoning = line.split(":", 1)[1].strip()

            elif lower.startswith("source:"):
                source = line.split(":", 1)[1].strip()

            elif lower.startswith("evidence:"):
                evidence = line.split(":", 1)[1].strip()

        if score not in VALID_LABELS:
            score = "Cannot Confidently Assess"

        return {
            "score": score,
            "reasoning": reasoning or "No explanation provided.",
            "source": source,
            "evidence": evidence,
        }
