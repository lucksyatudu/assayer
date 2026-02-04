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
