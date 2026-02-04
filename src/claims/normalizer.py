def normalize_sentence(sent) -> str:
    """
    Removes discourse markers & fluff WITHOUT breaking grammar.
    """
    tokens = []
    for token in sent:
        if token.dep_ in ("mark", "advmod") and token.text.lower() in {
            "however", "actually", "later", "finally"
        }:
            continue
        tokens.append(token.text)

    return " ".join(tokens).strip()
