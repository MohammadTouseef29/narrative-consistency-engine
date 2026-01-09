# STEP 11 (IMPROVED): Retrieve relevant novel chunks for each claim

from typing import List, Dict
import re


STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for",
    "with", "was", "were", "is", "are", "as", "by", "that", "this",
    "he", "she", "they", "his", "her", "their", "it", "at", "from"
}

NEGATION_WORDS = {"not", "never", "no", "denied", "refused", "rejected"}


def tokenize(text: str):
    return [w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS]


def score_chunk(claim_tokens, chunk_tokens):
    """
    Weighted overlap score:
    - more overlap → higher score
    """
    overlap = claim_tokens & chunk_tokens
    return len(overlap)


def retrieve_evidence_for_claim(
    claim: str,
    chunks: List[Dict],
    character: str,
    top_k: int = 5
) -> List[Dict]:
    """
    Improved retrieval:
    - character-aware
    - stopword filtered
    - overlap-based
    """

    claim_tokens = set(tokenize(claim))
    character = character.lower()

    scored_chunks = []

    for c in chunks:
        text = c["text"].lower()

        # --- Character filter ---
        if character not in text:
            continue

        chunk_tokens = set(tokenize(text))
        score = score_chunk(claim_tokens, chunk_tokens)

        if score == 0:
            continue

        has_negation = any(neg in chunk_tokens for neg in NEGATION_WORDS)

        scored_chunks.append({
            "chunk_id": c["chunk_id"],
            "score": score,
            "has_negation": has_negation,
            "text": c["text"]
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]


if __name__ == "__main__":
    # Simple sanity test
    claim = "Thalcave distrusted foreign explorers"
    character = "Thalcave"

    chunks = [
        {"chunk_id": 1, "text": "Thalcave never trusted the foreign explorers."},
        {"chunk_id": 2, "text": "The group traveled across Patagonia."},
        {"chunk_id": 3, "text": "Thalcave watched the strangers with suspicion."}
    ]

    results = retrieve_evidence_for_claim(claim, chunks, character)

    for r in results:
        print(r["chunk_id"], r["score"], r["has_negation"])
