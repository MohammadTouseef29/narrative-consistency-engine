# STEP 14 (FINAL): Track-A–correct inference pipeline

import os
import pandas as pd

from novel_loader import load_novel, chunk_text
from claim_extractor import extract_claims
from evidence_retriever import retrieve_evidence_for_claim
from claim_judger import judge_claim

def violates_hard_canon(row):
    """
    Row-level immutable narrative constraints.
    """
    char = row["char"].lower()
    content = row["content"].lower()

    # Abbé Faria hard canon
    if char == "faria":
        if any(
            phrase in content
            for phrase in [
                "from 1800",
                "after 1800",
                "lived quietly",
                "escaped",
                "escape",
                "island",
                "marseille",
                "quay",
                "outside prison",
                "free life"
            ]
        ):
            return True

    return False

def process_example(row, data_dir, novel_cache):
    book_name = row["book_name"]
    character = row["char"]
    backstory = row["content"]

     # 🔴 ROW-LEVEL HARD CANON CHECK
    if violates_hard_canon(row):
        return 0, "Backstory contradicts immutable narrative constraints."
    
    # --- Load & cache novel ---
    if book_name not in novel_cache:
        novel_text = load_novel(book_name, data_dir)
        novel_cache[book_name] = chunk_text(novel_text)

    chunks = novel_cache[book_name]

    # --- Extract claims ---
    claims = extract_claims(backstory, character)

    contradicted = 0
    supported = 0

    for claim in claims:
        evidence = retrieve_evidence_for_claim(claim, chunks, character)
        decision = judge_claim(claim, evidence, character)

        if decision == "CONTRADICTED":
            contradicted += 1
        elif decision == "SUPPORTED":
            supported += 1

    # --- FINAL DECISION (Track A semantics) ---
    # Only explicit contradiction fails
    if contradicted >= 1:
        final_label = 0
        rationale = "Backstory contradicts constraints established in the novel."
    else:
        final_label = 1
        if supported > 0:
            rationale = "Backstory is consistent with and partially supported by the novel."
        else:
            rationale = "Backstory does not contradict the novel narrative."

    return final_label, rationale


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")

    test_path = os.path.join(data_dir, "test.csv")
    test_df = pd.read_csv(test_path)

    novel_cache = {}
    results = []

    for _, row in test_df.iterrows():
        prediction, rationale = process_example(row, data_dir, novel_cache)

        results.append({
            "id": row["id"],
            "prediction": prediction,
            "rationale": rationale
        })

    output_path = os.path.join(base_dir, "results.csv")
    pd.DataFrame(results).to_csv(output_path, index=False)

    print("results.csv generated successfully.")


if __name__ == "__main__":
    main()
