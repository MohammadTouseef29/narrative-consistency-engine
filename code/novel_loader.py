# STEP 7 (POLISHED): Chapter-aware novel loading and chunking

import os
import re
from typing import List, Dict


def load_novel(book_name: str, data_dir: str) -> str:
    """
    Load the full novel text based on book_name.
    """
    if book_name.lower().startswith("the count"):
        filename = "The Count of Monte Cristo.txt"
    elif book_name.lower().startswith("in search"):
        filename = "In search of the castaways.txt"
    else:
        raise ValueError(f"Unknown book name: {book_name}")

    file_path = os.path.join(data_dir, filename)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return text


def split_into_chapters(text: str) -> List[str]:
    """
    Split novel text into chapters using common chapter markers.
    Works for both provided novels.
    """
    # Normalize spacing
    text = text.replace("\r\n", "\n")

    # Regex for CHAPTER headings
    chapter_pattern = re.compile(
        r"\n\s*(CHAPTER\s+[IVXLCDM0-9]+\.?|Chapter\s+[IVXLCDM0-9]+\.?)",
        re.IGNORECASE
    )

    splits = chapter_pattern.split(text)

    chapters = []
    current = ""

    for part in splits:
        if chapter_pattern.match("\n" + part):
            if current.strip():
                chapters.append(current.strip())
            current = part
        else:
            current += part

    if current.strip():
        chapters.append(current.strip())

    return chapters


def chunk_chapter(
    chapter_text: str,
    chapter_id: int,
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[Dict]:
    """
    Chunk a single chapter into overlapping chunks.
    """
    words = chapter_text.split()
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunks.append({
            "chunk_id": f"{chapter_id}_{chunk_id}",
            "chapter_id": chapter_id,
            "start_word": start,
            "end_word": min(end, len(words)),
            "text": " ".join(chunk_words)
        })

        chunk_id += 1
        start += chunk_size - overlap

    return chunks


def chunk_text(text: str) -> List[Dict]:
    """
    Chapter-aware chunking of novel text.
    """
    chapters = split_into_chapters(text)
    all_chunks = []

    for chapter_id, chapter_text in enumerate(chapters):
        chapter_chunks = chunk_chapter(chapter_text, chapter_id)
        all_chunks.extend(chapter_chunks)

    return all_chunks


if __name__ == "__main__":
    # Sanity check
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")

    novel = load_novel("In Search of the Castaways", data_dir)
    chunks = chunk_text(novel)

    print("Total chapters detected:", len(set(c["chapter_id"] for c in chunks)))
    print("Total chunks:", len(chunks))
    print("Sample chunk preview:\n", chunks[0]["text"][:400])
