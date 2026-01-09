# STEP 8 (POLISHED): Mandatory Pathway document indexing

import pathway as pw
from typing import List, Dict


def index_chunks_with_pathway(chunks: List[Dict]):
    """
    Create a real Pathway Table from novel chunks.
    This table acts as a document store and is REQUIRED
    for downstream processing in submission mode.
    """

    # Convert chunks into Pathway-compatible rows
    rows = []
    for c in chunks:
        rows.append({
            "chunk_id": c["chunk_id"],
            "chapter_id": c.get("chapter_id", -1),
            "text": c["text"]
        })

    # Create Pathway table (real, not debug)
    table = pw.Table.from_dicts(rows)

    return table


if __name__ == "__main__":
    # Sanity test (Linux / submission environment)
    sample_chunks = [
        {"chunk_id": "0_0", "chapter_id": 0, "text": "Sample text one"},
        {"chunk_id": "0_1", "chapter_id": 0, "text": "Sample text two"},
    ]

    table = index_chunks_with_pathway(sample_chunks)
    print("Pathway table created with rows:", table)
