---
name: organize-files-by-subject
description: Use this skill to classify and move 100+ PDF/PPTX/DOCX files into 5 subject folders (LLM, trapped_ion_and_qc, black_hole, DNA, music_history) based on content analysis. Handles keyword scoring with filename tiebreaking and music_history as catch-all default.
---

## Organize Files by Subject

Write and execute a Python script that:
1. Scans all PDF, PPTX, DOCX files in the current directory
2. Extracts text content from each file
3. Scores each file against 5 subject keyword sets
4. Moves each file into the correct subject folder
5. Defaults to `music_history` if no strong match is found

### Step 1: Write the classification script

```python
# write_classifier.py
script = r'''
import os
import sys
import shutil
import glob

# ── Text extraction ──────────────────────────────────────────────────────────

def extract_text_pdf(path, max_pages=40):
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                if i >= max_pages:
                    break
                t = page.extract_text()
                if t:
                    text += t + " "
    except Exception:
        pass
    if not text.strip():
        try:
            import PyPDF2
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    if i >= max_pages:
                        break
                    t = page.extract_text()
                    if t:
                        text += t + " "
        except Exception:
            pass
    return text

def extract_text_docx(path):
    text = ""
    try:
        from docx import Document
        doc = Document(path)
        text = " ".join(p.text for p in doc.paragraphs)
    except Exception:
        pass
    return text

def extract_text_pptx(path):
    text = ""
    try:
        from pptx import Presentation
        prs = Presentation(path)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + " "
    except Exception:
        pass
    return text

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_pdf(path)
    elif ext == ".docx":
        return extract_text_docx(path)
    elif ext == ".pptx":
        return extract_text_pptx(path)
    return ""

# ── Keyword definitions ──────────────────────────────────────────────────────

KEYWORDS = {
    "LLM": {
        # high-weight: very distinctive LLM terms
        "high": [
            "large language model", "llm", "gpt", "chatgpt", "gpt-4", "gpt-3",
            "transformer", "bert", "llama", "palm", "claude", "gemini",
            "instruction tuning", "rlhf", "reinforcement learning from human feedback",
            "prompt engineering", "chain of thought", "in-context learning",
            "fine-tuning", "pre-training", "tokenization", "attention mechanism",
            "self-attention", "generative ai", "text generation", "language model",
            "openai", "anthropic", "natural language processing", "nlp",
            "neural language", "autoregressive", "foundation model",
            "retrieval augmented generation", "rag", "hallucination",
        ],
        # medium-weight: supportive but less distinctive
        "medium": [
            "neural network", "deep learning", "machine learning", "embedding",
            "inference", "benchmark", "zero-shot", "few-shot", "dataset",
            "evaluation", "text classification", "question answering",
            "summarization", "dialogue", "chatbot", "tokens", "vocabulary",
        ],
    },
    "trapped_ion_and_qc": {
        "high": [
            "trapped ion", "ion trap", "quantum computing", "qubit", "qubits",
            "quantum gate", "quantum circuit", "quantum error correction",
            "quantum entanglement", "quantum supremacy", "quantum advantage",
            "quantum processor", "quantum hardware", "quantum algorithm",
            "grover", "shor algorithm", "variational quantum",
            "quantum annealing", "quantum simulation", "quantum coherence",
            "decoherence", "laser cooling", "paul trap", "penning trap",
            "ytterbium", "barium ion", "calcium ion", "beryllium ion",
            "motional mode", "sympathetic cooling", "micromotion",
            "quantum memory", "quantum network", "quantum communication",
            "quantum teleportation", "bell state", "quantum speedup",
        ],
        "medium": [
            "quanta", "superposition", "quantum noise", "fidelity",
            "quantum optics", "photon", "spin", "quantum dot",
            "superconducting qubit", "topological qubit", "quantum volume",
            "quantum programming", "quantum software", "quantum compiler",
        ],
    },
    "black_hole": {
        "high": [
            "black hole", "black holes", "event horizon", "singularity",
            "hawking radiation", "schwarzschild", "kerr metric",
            "gravitational wave", "gravitational waves", "general relativity",
            "neutron star", "pulsar", "quasar", "accretion disk",
            "stellar collapse", "white dwarf", "supermassive black hole",
            "ligo", "virgo detector", "spacetime curvature",
            "einstein field equations", "penrose", "hawking", "bekenstein",
            "information paradox", "firewall", "holographic principle",
            "dark matter", "dark energy", "cosmology", "galaxy merger",
            "tidal disruption", "jet emission", "x-ray binary",
            "gravitational lensing", "redshift", "cosmic microwave background",
        ],
        "medium": [
            "astrophysics", "astronomy", "stellar", "solar mass",
            "parsec", "light year", "spectroscopy", "telescope",
            "hubble", "james webb", "electromagnetic spectrum",
            "orbital mechanics", "binary system",
        ],
    },
    "DNA": {
        "high": [
            "dna", "rna", "genome", "genomics", "gene", "genetics",
            "nucleotide", "nucleotides", "base pair", "base pairs",
            "double helix", "replication", "transcription", "translation",
            "mutation", "snp", "crispr", "cas9", "gene editing",
            "epigenetics", "methylation", "histone", "chromatin",
            "chromosome", "allele", "genotype", "phenotype",
            "sequencing", "whole genome sequencing", "next generation sequencing",
            "pcr", "polymerase chain reaction", "primer",
            "mrna", "ribosome", "codon", "protein synthesis",
            "dna repair", "recombination", "plasmid", "vector",
            "stem cell", "cell biology", "molecular biology",
            "bioinformatics", "phylogenetics", "evolution",
        ],
        "medium": [
            "protein", "amino acid", "enzyme", "cell", "nucleus",
            "mitochondria", "bacteria", "virus", "pathogen",
            "cloning", "expression", "knockout", "transgenic",
            "biomarker", "clinical trial", "therapeutic",
        ],
    },
    "music_history": {
        "high": [
            "music history", "musical", "composer", "symphony",
            "orchestra", "baroque", "classical period", "romantic period",
            "renaissance music", "medieval music", "opera", "concerto",
            "sonata", "beethoven", "mozart", "bach", "handel",
            "chopin", "brahms", "tchaikovsky", "wagner", "verdi",
            "haydn", "schubert", "liszt", "debussy", "mahler",
            "stravinsky", "jazz history", "blues history", "rock history",
            "folk music", "musicology", "counterpoint", "polyphony",
            "harmonic", "melody", "rhythm", "tempo", "notation",
            "score", "conductor", "soloist", "chamber music",
            "string quartet", "piano", "violin", "harpsichord",
            "music theory", "music education",
        ],
        "medium": [
            "music", "song", "singer", "album", "recording",
            "concert", "performance", "musician", "instrument",
            "genre", "harmony", "scale", "chord",
        ],
    },
}

FOLDERS = ["LLM", "trapped_ion_and_qc", "black_hole", "DNA", "music_history"]

# Weights
HIGH_WEIGHT = 3
MEDIUM_WEIGHT = 1

# If the best score is below this threshold, default to music_history
MIN_SCORE_THRESHOLD = 3

# ── Scoring ──────────────────────────────────────────────────────────────────

def score_text(text, fname):
    text_lower = text.lower()
    fname_lower = os.path.splitext(fname)[0].lower().replace("_", " ").replace("-", " ")

    scores = {}
    for category, kw_dict in KEYWORDS.items():
        score = 0
        for kw in kw_dict.get("high", []):
            count = text_lower.count(kw)
            score += count * HIGH_WEIGHT
            # Also check filename with higher bonus
            if kw in fname_lower:
                score += HIGH_WEIGHT * 4

        for kw in kw_dict.get("medium", []):
            count = text_lower.count(kw)
            score += count * MEDIUM_WEIGHT
            if kw in fname_lower:
                score += MEDIUM_WEIGHT * 3

        scores[category] = score

    return scores

def classify(path):
    fname = os.path.basename(path)
    text = extract_text(path)
    text_len = len(text.strip())

    scores = score_text(text, fname)

    best_category = max(scores, key=lambda c: scores[c])
    best_score = scores[best_category]

    # Default to music_history if no confident match
    if best_score < MIN_SCORE_THRESHOLD:
        best_category = "music_history"

    return best_category, scores

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    base_dir = os.getcwd()

    # Create folders
    for folder in FOLDERS:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

    # Gather all files (non-recursive, current dir only)
    extensions = ["*.pdf", "*.pptx", "*.docx", "*.PDF", "*.PPTX", "*.DOCX"]
    all_files = []
    for ext in extensions:
        all_files.extend(glob.glob(os.path.join(base_dir, ext)))

    # Exclude files inside the subject folders themselves
    all_files = [
        f for f in all_files
        if os.path.dirname(os.path.abspath(f)) == os.path.abspath(base_dir)
    ]

    if not all_files:
        print("No files found to classify.")
        sys.exit(0)

    print(f"Found {len(all_files)} files to classify.")

    results = []
    for fpath in all_files:
        fname = os.path.basename(fpath)
        category, scores = classify(fpath)
        dest_folder = os.path.join(base_dir, category)
        dest_path = os.path.join(dest_folder, fname)

        # Handle name collision
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(fname)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1

        shutil.move(fpath, dest_path)
        score_summary = {k: v for k, v in sorted(scores.items(), key=lambda x: -x[1])}
        print(f"[{category}] {fname}  scores={score_summary}")
        results.append((fname, category))

    print(f"\nDone. {len(results)} files classified and moved.")

    # Verify all files are moved
    remaining = []
    for ext in extensions:
        remaining.extend(glob.glob(os.path.join(base_dir, ext)))
    remaining = [
        f for f in remaining
        if os.path.dirname(os.path.abspath(f)) == os.path.abspath(base_dir)
    ]
    if remaining:
        print(f"WARNING: {len(remaining)} files were NOT moved: {remaining}")
        sys.exit(1)
    else:
        print("All files successfully moved into subject folders.")
        sys.exit(0)

if __name__ == "__main__":
    main()
'''

with open("classify_files.py", "w", encoding="utf-8") as f:
    f.write(script)

print("Script written to classify_files.py")
```

### Step 2: Install dependencies

```bash
pip install pdfplumber PyPDF2 python-docx python-pptx
```

### Step 3: Run the classifier

```bash
python classify_files.py
```

### Step 4: Verify results

```bash
python -c "
import os
folders = ['LLM', 'trapped_ion_and_qc', 'black_hole', 'DNA', 'music_history']
total = 0
for f in folders:
    if os.path.isdir(f):
        files = [x for x in os.listdir(f) if x.lower().endswith(('.pdf','.pptx','.docx'))]
        print(f'{f}: {len(files)} files')
        total += len(files)
print(f'Total: {total} files')
"
```

### Notes

- `MAX_PAGES=40` ensures enough text is read from long academic PDFs
- High-weight keywords score 3× per occurrence, filename hits score 12× (4× the text weight)
- Medium-weight keywords score 1× per occurrence, filename hits score 3×
- Files scoring below threshold (3 points) default to `music_history` as the catch-all
- Name collisions are handled with a numeric suffix to avoid overwriting