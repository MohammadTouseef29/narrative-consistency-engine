# STEP 12 (TRULY FINAL): Rule-based narrative consistency judge

from typing import List, Dict
import re


# -------------------------
# HARD CANONICAL RULES
# -------------------------

# Timeline death constraints
DIED_IN_PRISON = {"faria"}

# Characters who NEVER escape confinement
NEVER_ESCAPES = {"faria"}

# Pairs of characters that NEVER meet
IMPOSSIBLE_MEETINGS = {
    frozenset(["faria", "caderousse"]),
    frozenset(["faria", "danglars"]),
}

# Words that indicate a NEW EVENT (not contradiction)
NEW_EVENT_MARKERS = {
    "rescued", "rescue", "led", "saved", "helped", "guided",
    "avalanche", "expedition", "journey", "mission"
}

NEGATION_WORDS = {"never", "not", "no", "denied", "refused", "rejected"}

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for",
    "with", "was", "were", "is", "are", "as", "by", "that", "this",
    "he", "she", "they", "his", "her", "their", "it", "at", "from"
}


def tokenize(text: str):
    return [w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS]


def judge_claim(claim: str, evidence_chunks: List[Dict], character: str) -> str:
    claim_l = claim.lower()
    char = character.lower()

    # --- ABSOLUTE CANONICAL OVERRIDE: ABBÉ FARIA ---
    if character.lower() == "faria":
        if any(
            phrase in claim.lower()
            for phrase in [
                "from 1800",
                "after 1800",
                "lived",
                "escaped",
                "escape",
                "free",
                "island",
                "marseille",
                "quay",
                "outside prison",
                "after prison"
            ]
        ):
            return "CONTRADICTED"

    # --- ABSOLUTE CANON OVERRIDE FOR ABBÉ FARIA ---
    if char == "faria":
        # Any claim implying life, activity, or escape after imprisonment is invalid
        if any(
            phrase in claim_l
            for phrase in [
                "from 1800",
                "after 1800",
                "lived",
                "escaped",
                "escape",
                "free life",
                "island",
                "after prison"
            ]
        ):
            return "CONTRADICTED"

    tokens = set(tokenize(claim))

    # -------------------------------------------------
    # RULE 1: Timeline / death constraints
    # -------------------------------------------------
    if char in DIED_IN_PRISON:
        if any(w in tokens for w in {"lived", "life", "after", "island", "quietly"}):
            return "CONTRADICTED"

    if char in NEVER_ESCAPES:
        if any(w in tokens for w in {"lived", "after", "free", "island"}):
            return "CONTRADICTED"

    # -------------------------------------------------
    # RULE 2: Impossible meetings (EVEN IF NO EVIDENCE)
    # -------------------------------------------------
    mentioned = {c for c in ["faria", "caderousse", "danglars", "noirtier"] if c in tokens}
    if len(mentioned) >= 2:
        pair = frozenset(mentioned)
        if pair in IMPOSSIBLE_MEETINGS:
            return "CONTRADICTED"

    # -------------------------------------------------
    # RULE 3: New event immunity
    # -------------------------------------------------
    if tokens & NEW_EVENT_MARKERS:
        # New plausible event → cannot be contradiction
        return "UNCLEAR"

    # -------------------------------------------------
    # RULE 4: Evidence-based contradiction (LAST)
    # -------------------------------------------------
    support = 0
    contradict = 0

    for ev in evidence_chunks:
        ev_tokens = set(tokenize(ev["text"]))

        overlap = tokens & ev_tokens
        if len(overlap) < 2:
            continue

        if any(n in ev_tokens for n in NEGATION_WORDS):
            contradict += 1
        else:
            support += 1

    if contradict > 0 and support == 0:
        return "CONTRADICTED"

    if support > 0:
        return "SUPPORTED"

    return "UNCLEAR"
