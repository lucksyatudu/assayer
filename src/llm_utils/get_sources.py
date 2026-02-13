from typing import List, Dict, Any
from src.claims.schema import Claim
from src.web_search.search import SearchResult
from src.llm_utils.gemini import BaseModel


VALID_LABELS = {
    "Inaccurate",
    "Unsupported",
    "Disputed",
    "Accurate",
    "Cannot Confidently Assess",
}


class GeminiClaimValidator(BaseModel):
    """
    Gemini-powered hybrid claim evaluator.

    Input:
        - Claim
        - Supporting evidence snippets
        - Contradicting evidence snippets

    Output:
        {
            "score": <ValidationScore>,
            "reasoning": <short explanation>
        }
    """

    async def run(
        self,
        claim: Claim,
        supporting: List[SearchResult],
        contradicting: List[SearchResult],
    ) -> Dict[str, Any]:

        prompt = self._build_prompt(claim, supporting, contradicting)

        raw_output = await self._generate(prompt)

        parsed = self._parse_output(raw_output)

        return parsed

    # ------------------------------------------------------------------ #
    # Prompt Construction
    # ------------------------------------------------------------------ #

    def _build_prompt(
        self,
        claim: Claim,
        supporting: List[SearchResult],
        contradicting: List[SearchResult],
    ) -> str:

        def format_evidence(results: List[SearchResult]) -> str:
            if not results:
                return "None"
            return "\n".join(
                f"- {r.snippet} (Source: {r.url})"
                for r in results[:3]
            )

        return f"""
        You are a strict factual claim validator.

        Your task is to classify the claim using the evidence provided.

        Claim:
        "{claim.normalized_claim}"

        Subject: {claim.subject}
        Predicate: {claim.predicate}

        Supporting Evidence:
        {format_evidence(supporting)}

        Contradicting Evidence:
        {format_evidence(contradicting)}

        Classify the claim into EXACTLY one of the following:

        - Accurate
        - Inaccurate
        - Disputed
        - Unsupported
        - Cannot Confidently Assess

        Rules:
        - Accurate → Strong reliable evidence supports claim.
        - Inaccurate → Strong reliable evidence disproves claim.
        - Disputed → Credible sources disagree.
        - Unsupported → No reliable evidence found.
        - Cannot Confidently Assess → Evidence is insufficient or unclear.

        Respond strictly in this format:

        Score: <one of the five labels>
        Reasoning: <1–3 sentence explanation>
        """

    # ------------------------------------------------------------------ #
    # Output Parsing
    # ------------------------------------------------------------------ #

    def _parse_output(self, text: str) -> Dict[str, Any]:
        """
        Extracts:
            Score: ...
            Reasoning: ...
        """

        score = None
        reasoning = None

        for line in text.splitlines():
            if line.lower().startswith("score:"):
                score = line.split(":", 1)[1].strip()
            elif line.lower().startswith("reasoning:"):
                reasoning = line.split(":", 1)[1].strip()

        # Hard safety enforcement
        if score not in VALID_LABELS:
            score = "Cannot Confidently Assess"

        return {
            "score": score,
            "reasoning": reasoning or "No explanation provided.",
        }
