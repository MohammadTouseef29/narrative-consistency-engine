# STEP 9: Link dataset rows to novel chunks via Pathway abstraction

import os
import pandas as pd

from novel_loader import load_novel, chunk_text
from pathway_index import index_chunks_with_pathway


def process_row(row, data_dir):
    """
    Given one row from train/test, load and index its novel.
    """
    book_name = row["book_name"]
    char_name = row["char"]

    print(f"\nProcessing character: {char_name}")
    print(f"Book: {book_name}")

    # Load novel
    novel_text = load_novel(book_name, data_dir)

    # Chunk novel
    chunks = chunk_text(novel_text)

    print(f"Total chunks for book: {len(chunks)}")

    # Index using Pathway abstraction
    pathway_table = index_chunks_with_pathway(chunks)

    return pathway_table, chunks


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")

    # Load train.csv
    train_path = os.path.join(data_dir, "train.csv")
    train_df = pd.read_csv(train_path)

    # Test with FIRST row only (important)
    first_row = train_df.iloc[0]

    table = process_row(first_row, data_dir)

    print("\nIndexing result:", table)
