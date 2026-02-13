import spacy
from typing import List, Optional

from src.claims.schema import Claim
from src.claims.normalizer import normalize_sentence,canonicalize_claim
from src.claims.scoring import score_objectivity, score_verifiability


nlp = spacy.load("en_core_web_sm")

MIN_TOKENS = 5


# -------------------------------------------------------
# Core Detection Logic
# -------------------------------------------------------

def contains_verifiable_proposition(sent: spacy.tokens.Span) -> bool:
    """
    A sentence is verifiable if it contains:
    - A subject
    - A verb (including copular verbs like is/was)
    """

    has_subject = False
    has_verb = False

    for token in sent:
        if token.dep_ in ("nsubj", "nsubjpass"):
            has_subject = True
        if token.pos_ in ("VERB", "AUX"):
            has_verb = True

    return has_subject and has_verb


def extract_main_subject(sent: spacy.tokens.Span) -> Optional[str]:
    for token in sent:
        if token.dep_ in ("nsubj", "nsubjpass"):
            return " ".join(t.text for t in token.subtree)
    return None


def extract_main_predicate(sent: spacy.tokens.Span) -> Optional[str]:
    for token in sent:
        if token.dep_ == "ROOT":
            return token.lemma_
    return None


# -------------------------------------------------------
# Main Extraction
# -------------------------------------------------------

def extract_claims(text: str) -> List[Claim]:
    doc = nlp(text)
    claims: List[Claim] = []

    last_entity: Optional[str] = None

    for sent in doc.sents:
        original_sentence = sent.text.strip()

        if len(original_sentence.split()) < MIN_TOKENS:
            continue

        if original_sentence.endswith("?"):
            continue

        # Track entities for pronoun grounding
        for ent in sent.ents:
            if ent.label_ in ("PERSON", "ORG", "GPE", "WORK_OF_ART"):
                last_entity = ent.text

        if not contains_verifiable_proposition(sent):
            continue

        subject = extract_main_subject(sent)
        predicate = extract_main_predicate(sent)

        if not subject or not predicate:
            continue

        # Pronoun grounding (minimal and safe)
        if subject.lower() in {"he", "she", "they", "it"} and last_entity:
            subject = last_entity

        claims.append(
            Claim(
                original_sentence=original_sentence,  # FULL sentence
                normalized_claim=canonicalize_claim(sent),
                is_claim=True,
                claim_strength=score_objectivity(sent),
                verifiability=score_verifiability(sent),
                subject=subject,
                predicate=predicate,
            )
        )

    return claims
