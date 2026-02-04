from typing import Optional

def resolve_pronouns(clause: str, last_entity: Optional[str]) -> str:
    if last_entity and clause.startswith(("He ", "She ", "They ")):
        return clause.replace("He ", f"{last_entity} ", 1)
    return clause
