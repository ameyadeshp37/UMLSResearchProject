#!/usr/bin/env python3
"""
Extract biomedical concepts from PubMed abstracts using SciSpaCy + UMLS linker.

Output format:
concept | CUI | semantic type | count
"""

import sys
from collections import Counter

import spacy
import scispacy
from scispacy.linking import EntityLinker
from scispacy.abbreviation import AbbreviationDetector


# ------------------------------------------------
# UMLS semantic types to keep
# ------------------------------------------------

ALLOWED_TUIS = {
    "T047",  # Disease or Syndrome
    "T191",  # Neoplastic Process
    "T046",  # Pathologic Function
    "T184",  # Sign or Symptom
    "T121",  # Pharmacologic Substance
    "T200",  # Clinical Drug
    "T061",  # Therapeutic Procedure
    "T060",  # Diagnostic Procedure
}

# ------------------------------------------------
# Generic concepts to remove
# ------------------------------------------------

GENERIC = {
    "patients",
    "persons",
    "condition",
    "diagnosis",
    "disease",
    "complication",
    "therapeutic procedure",
    "pharmacotherapy"
}


# ------------------------------------------------
# Load SciSpaCy model
# ------------------------------------------------

def load_model():

    print("Loading SciSpaCy model...")

    nlp = spacy.load("en_core_sci_md")

    # improves entity linking
    nlp.add_pipe("abbreviation_detector")

    nlp.add_pipe(
        "scispacy_linker",
        config={
            "linker_name": "umls",
            "resolve_abbreviations": True
        }
    )

    return nlp


# ------------------------------------------------
# Extract UMLS concepts
# ------------------------------------------------

def extract_umls_concepts(text, nlp):

    linker = nlp.get_pipe("scispacy_linker")

    counts = Counter()

    docs = nlp.pipe([text], batch_size=50)

    for doc in docs:

        for ent in doc.ents:

            if not ent._.kb_ents:
                continue

            cui, score = ent._.kb_ents[0]

            # lower threshold improves recall
            if score < 0.3:
                continue

            concept = linker.kb.cui_to_entity[cui]

            name = concept.canonical_name.lower()

            if name in GENERIC:
                continue

            semantic_types = concept.types

            if not semantic_types:
                continue

            tui = semantic_types[0]

            if tui not in ALLOWED_TUIS:
                continue

            key = (name, cui, tui)

            counts[key] += 1

    return counts


# ------------------------------------------------
# Main
# ------------------------------------------------

def main():

    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if not text.strip():
        raise SystemExit("No input text provided")

    nlp = load_model()

    print("Extracting biomedical concepts...")

    counts = extract_umls_concepts(text, nlp)

    print("\nTop biomedical concepts:\n")

    for (name, cui, tui), c in counts.most_common(20):

        print(f"{name} | {cui} | {tui} | {c}")


if __name__ == "__main__":
    main()