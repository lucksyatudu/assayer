def score_objectivity(sent) -> float:
    subjective_markers = {
        "interesting", "fascinating", "amazing",
        "I think", "I believe", "arguably"
    }

    text = sent.text.lower()
    if any(m in text for m in subjective_markers):
        return 0.4

    return 0.85


def score_verifiability(sent) -> float:
    has_entity = any(ent.label_ in ("PERSON", "ORG", "GPE", "EVENT")
                     for ent in sent.ents)

    has_action = any(tok.pos_ == "VERB" for tok in sent)

    return 0.9 if has_entity and has_action else 0.5
