# STEP 10 (IMPROVED): Extract only verifiable claims from backstory

import re
from typing import List


ACTION_KEYWORDS = {
    "went", "traveled", "joined", "left", "fought", "escaped",
    "trusted", "betrayed", "refused", "helped", "saved", "attacked",
    "captured", "imprisoned", "guided", "followed"
}


def split_into_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 0]


def is_verifiable(sentence: str, character: str) -> bool:
    s = sentence.lower()
    char = character.lower()

    # Must mention character or clear action
    if char in s:
        return True

    for kw in ACTION_KEYWORDS:
        if kw in s:
            return True

    return False


def extract_claims(backstory_text: str, character: str) -> List[str]:
    """
    Extract only claims that can realistically be verified
    against a long narrative.
    """

    sentences = split_into_sentences(backstory_text)
    claims = []

    for s in sentences:
        cleaned = s.replace("\n", " ").strip()

        if len(cleaned) < 12:
            continue

        if is_verifiable(cleaned, character):
            claims.append(cleaned)

    return claims


if __name__ == "__main__":
    backstory = """
    Thalcave was courageous and honorable.
    He guided the explorers through Patagonia.
    He distrusted all foreigners.
    """

    claims = extract_claims(backstory, "Thalcave")
    print(claims)
