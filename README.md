# Narrative Consistency Verification using Long-Context Reasoning (Track A)

This project implements a **long-context narrative consistency verification system** for fictional characters.

Given a **hypothetical backstory** for a character and the **full original novel**, the system determines whether the backstory is **consistent** with the narrative constraints of the novel or **contradicts established canon**.

Unlike traditional fact-checking or retrieval systems, this project treats the problem as a **constraint satisfaction task over long narratives**.

---

## 🔍 Problem Overview

- **Input**
  - Full novel text (unabridged)
  - Character name
  - Hypothetical backstory (may be partially fictional)
- **Output**
  - `1` → Backstory is consistent with the novel  
  - `0` → Backstory contradicts narrative constraints
  - A short, explainable rationale

Key challenge:
> A backstory can be *consistent* even if it is **not explicitly mentioned** in the novel — it only fails when it **violates canonical constraints**.

---

## 🧠 Core Design Philosophy

This system is built on three principles:

1. **Long-context awareness**
   - Entire novels are processed, not summaries
   - Chapter-aware chunking preserves narrative coherence

2. **Constraint-based reasoning**
   - Immutable narrative facts (e.g., character deaths, imprisonment) are enforced
   - Lack of evidence is *not* treated as contradiction

3. **Explainability**
   - No black-box ML or embeddings
   - Decisions are deterministic and rule-based
   - Every prediction can be traced to narrative logic

---

## 🏗️ System Architecture

### 1. Novel Processing
- Novels are split **by chapters**
- Chapters are chunked with overlap to preserve context
- Chunks are indexed into a **Pathway table**, serving as the canonical document store

### 2. Claim Extraction
- Hypothetical backstories are split into **verifiable claims**
- Abstract or unverifiable sentences are filtered out

### 3. Evidence Retrieval
- Relevant novel chunks are retrieved using:
  - character-aware filtering
  - keyword overlap
- Retrieval is conservative to avoid hallucinations

### 4. Claim Judgement
Each claim is classified as:
- `SUPPORTED`
- `UNCLEAR`
- `CONTRADICTED`

Judgement uses:
- canonical constraints
- impossible interaction detection
- negation-aware evidence checks

### 5. Row-Level Canon Enforcement
Some narrative constraints are **global and immutable** (e.g., Abbé Faria never escapes imprisonment).

Such constraints are enforced **before** claim-level reasoning to prevent logically impossible backstories.

### 6. Final Aggregation
- Default assumption: **consistent**
- Only explicit contradictions result in `0`

---

## 📂 Project Structure
kdsh_trackA/
│
├── code/
│ ├── main.py # Entry point / sanity checks
│ ├── novel_loader.py # Chapter-aware novel loading & chunking
│ ├── pathway_index.py # Pathway-based document indexing
│ ├── row_to_novel.py # Row-to-novel linking
│ ├── claim_extractor.py # Verifiable claim extraction
│ ├── evidence_retriever.py # Character-aware evidence retrieval
│ ├── claim_judger.py # Constraint-based claim judgement
│ ├── aggregator.py # Decision aggregation logic
│ └── run_inference.py # End-to-end inference pipeline
│
├── data/
│ ├── train.csv
│ ├── test.csv
│ ├── The Count of Monte Cristo.txt
│ └── In Search of the Castaways.txt
│
├── results.csv # Final predictions
└── README.md

## 🚀 How to Run

### Run inference
```bash
python code/run_inference.py