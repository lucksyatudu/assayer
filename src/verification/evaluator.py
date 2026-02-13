def evaluate_accuracy(claim_facts, evidence_summary) -> int:
    """
    LLM-based factual comparison using structured inputs only.
    """

    prompt = f"""
    Compare the factual claim with the evidence.

    Claim facts:
    {claim_facts}

    Evidence summary:
    {evidence_summary}

    Choose ONE category:
    1. Completely accurate
    2. Mostly accurate
    3. Mixed accuracy
    4. Mostly inaccurate
    5. Completely inaccurate
    6. Cannot confidently assess

    Return only the number.
    """

    return call_llm(prompt)
