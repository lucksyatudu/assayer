import spacy
from typing import List
from .schema import Claim

from src.claims.normalizer import normalize_sentence
from src.claims.scoring import score_objectivity, score_verifiability

nlp = spacy.load("en_core_web_sm")

MIN_TOKENS = 6

def extract_claims(text: str) -> List[Claim]:
    doc = nlp(text)
    claims: List[Claim] = []

    for sent in doc.sents:
        sent_text = sent.text.strip()

        # ---- HARD FILTERS (language-agnostic) ----
        if len(sent_text.split()) < MIN_TOKENS:
            continue

        if sent_text.endswith("?"):
            continue  # questions ≠ claims

        # ---- SYNTACTIC VALIDATION ----
        subject = None
        predicate = None
        has_verb = False

        for token in sent:
            if token.dep_ in ("nsubj", "nsubjpass") and subject is None:
                subject = token.text
            if token.pos_ == "VERB":
                has_verb = True
                predicate = token.lemma_

        if not subject or not has_verb:
            continue

        # ---- NORMALIZATION (NON-DESTRUCTIVE) ----
        normalized = normalize_sentence(sent)

        claims.append(
            Claim(
                original_sentence=sent_text,
                normalized_claim=normalized,
                is_claim=True,
                claim_strength=score_objectivity(sent),
                verifiability=score_verifiability(sent),
                subject=subject,
                predicate=predicate,
            )
        )

    return claims
