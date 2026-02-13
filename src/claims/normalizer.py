import spacy

def normalize_sentence(doc) -> str:
    """
    Extracts the main propositional clause.
    """
    root = None
    for token in doc:
        if token.dep_ == "ROOT":
            root = token
            break

    if not root:
        return doc.text.strip()

    # Keep subject + predicate subtree
    keep = set()

    for child in root.subtree:
        if child.dep_ not in {"discourse", "mark"}:
            keep.add(child.i)

    tokens = [t.text for t in doc if t.i in keep]
    return " ".join(tokens).strip()

def canonicalize_claim(span: spacy.tokens.Span) -> str:
    subject = None
    predicate = None
    obj = None

    for token in span:
        if token.dep_ in ("nsubj", "nsubjpass"):
            subject = token.ent_type_ or "ENTITY"

        if token.dep_ == "ROOT":
            predicate = token.lemma_

        if token.dep_ in ("dobj", "attr", "pobj"):
            obj = token.lemma_

    parts = [p for p in [subject, predicate, obj] if p]
    return " | ".join(parts)

