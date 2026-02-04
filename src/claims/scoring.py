def score_objectivity(sent) -> float:
    """
    Scores objectivity on a continuous scale [0, 1].
    Uses syntactic + semantic signals instead of word lists.
    """

    score = 1.0

    # --- 1. First-person stance (strong penalty)
    for token in sent:
        if token.pos_ == "PRON" and token.text.lower() in {"i", "we"}:
            score -= 0.35

        if token.lemma_.lower() in {"think", "believe", "feel", "guess"}:
            score -= 0.25

    # --- 2. Evaluative adjectives (moderate penalty)
    for token in sent:
        if token.pos_ == "ADJ" and token.dep_ == "amod":
            # Skip measurable adjectives (e.g., "large", "three")
            if token.lemma_.lower() not in {"large", "small", "many", "few"}:
                score -= 0.15

    # --- 3. Hedging / modality (light penalty)
    for token in sent:
        if token.lemma_.lower() in {
            "seem", "appear", "likely", "possibly", "probably"
        }:
            score -= 0.1

    # --- 4. Attribution boosts objectivity
    for token in sent:
        if token.lemma_.lower() in {
            "study", "report", "research", "data", "evidence"
        }:
            score += 0.15

    # --- 5. Named entities increase factuality
    if len(sent.ents) > 0:
        score += 0.1

    return max(0.0, min(score, 1.0))

def score_verifiability(sent) -> float:
    """
    Scores how externally checkable a sentence is.
    """

    score = 0.0

    # --- 1. Named entities (strong signal)
    if any(ent.label_ in {"PERSON", "ORG", "GPE", "LOC", "EVENT", "WORK_OF_ART"}
           for ent in sent.ents):
        score += 0.35

    # --- 2. Concrete subject (noun phrase as subject)
    if any(tok.dep_ in {"nsubj", "nsubjpass"} and tok.pos_ in {"NOUN", "PROPN"}
           for tok in sent):
        score += 0.25

    # --- 3. Assertive verb (penalize modality)
    for tok in sent:
        if tok.pos_ == "VERB":
            if tok.lemma_.lower() in {
                "seem", "appear", "might", "could", "may"
            }:
                score -= 0.15
            else:
                score += 0.2
            break

    # --- 4. External anchoring (time / place / event)
    if any(tok.ent_type_ in {"DATE", "TIME", "GPE", "LOC", "EVENT"}
           for tok in sent):
        score += 0.2

    # --- 5. First-person stance penalty
    if any(tok.text.lower() in {"i", "we"} for tok in sent):
        score -= 0.3

    return max(0.0, min(score, 1.0))
