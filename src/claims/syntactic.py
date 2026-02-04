import spacy

nlp = spacy.load("en_core_web_sm")

def has_independent_clause(sentence: str) -> bool:
    doc = nlp(sentence)

    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            return True
    return False


def has_subject(doc) -> bool:
    return any(t.dep_ in ("nsubj", "nsubjpass") for t in doc)


def is_declarative(doc) -> bool:
    if doc[-1].text == "?":
        return False
    for token in doc:
        if token.dep_ == "aux" and token.tag_ == "MD":
            # modal verbs weaken certainty but don't disqualify
            continue
    return True
