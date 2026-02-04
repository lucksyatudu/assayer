import re

def is_declarative(sentence: str) -> bool:
    return (
        sentence.endswith(".")
        and not sentence.strip().startswith(("Who", "What", "Why", "How"))
    )


def has_subject_predicate(sentence: str) -> bool:
    # Very lightweight grammar proxy
    # Looks for noun + verb pattern
    return bool(re.search(r"\b(is|was|were|are|has|have|had|caused|increased|decreased)\b", sentence.lower()))


def contains_subjective_language(sentence: str) -> bool:
    subjective_markers = [
        "i think", "i believe", "we feel", "beautiful", "best", "worst",
        "amazing", "terrible", "shocking", "disappointing"
    ]
    s = sentence.lower()
    return any(m in s for m in subjective_markers)


def is_potentially_verifiable(sentence: str) -> bool:
    # Heuristic: presence of entities, numbers, dates, or proper nouns
    return bool(
        re.search(r"\d", sentence) or
        re.search(r"\b[A-Z][a-z]+\b", sentence)
    )
