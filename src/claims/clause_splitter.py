import spacy

nlp = spacy.load("en_core_web_sm")

def extract_factual_clauses(sentence: str) -> list[str]:
    """
    Extract independent + subordinate factual clauses.
    """
    doc = nlp(sentence)
    clauses = []

    for token in doc:
        # Root clause
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            subtree = list(token.subtree)
            clauses.append(" ".join(t.text for t in subtree))
        
        # Complement clauses (revealed that, said that, etc.)
        if token.dep_ in ("ccomp", "xcomp"):
            subtree = list(token.subtree)
            clauses.append(" ".join(t.text for t in subtree))

    return list(set(c.strip() for c in clauses))
