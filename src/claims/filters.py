DISCOURSE_PREFIXES = (
    "however",
    "in the film",
    "it's later revealed that",
)

def normalize_clause(text: str) -> str:
    t = text.strip()
    lower = t.lower()

    for prefix in DISCOURSE_PREFIXES:
        if lower.startswith(prefix):
            t = t[len(prefix):].strip(" ,.")
    return t
