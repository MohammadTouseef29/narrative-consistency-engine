# STEP 13 (FIXED): Aggregate claim-level decisions into final consistency label

from typing import List


def aggregate_claims(claim_decisions: List[str]) -> int:
    """
    Evidence-weighted aggregation.

    Returns:
      1 -> consistent
      0 -> contradiction
    """

    total = len(claim_decisions)

    if total == 0:
        return 0  # no evidence → fail safely

    supported = claim_decisions.count("SUPPORTED")
    contradicted = claim_decisions.count("CONTRADICTED")
    unclear = claim_decisions.count("UNCLEAR")

    # --- Strong contradiction case ---
    if contradicted >= 2:
        return 0

    # --- Weak contradiction but strong support ---
    if contradicted == 1 and supported >= 2:
        return 1

    # --- Clear support dominates ---
    if supported > contradicted and supported >= 1:
        return 1

    # --- Mostly unclear or weak evidence ---
    return 0


if __name__ == "__main__":
    # Sanity tests
    print(aggregate_claims(["SUPPORTED", "SUPPORTED", "UNCLEAR"]))      # 1
    print(aggregate_claims(["SUPPORTED", "CONTRADICTED", "SUPPORTED"])) # 1
    print(aggregate_claims(["CONTRADICTED", "UNCLEAR"]))                # 0
    print(aggregate_claims(["UNCLEAR", "UNCLEAR"]))                     # 0
