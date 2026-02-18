import csv
import sys
import csv
from pathlib import Path


def stream_rrf(path):
    with open(path, encoding="utf-8") as f:
        csv.field_size_limit(sys.maxsize)
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            yield row


def load_mesh_concepts(mrconso_path):
    concepts = {}
    for row in stream_rrf(mrconso_path):
        cui = row[0]
        sab = row[11]
        name = row[14]
        suppress = row[16]
        if sab != "MSH":
            continue
        if suppress == "Y":
            continue
        if cui not in concepts:
            concepts[cui] = name
    return concepts


def load_mesh_relationships(mrrel_path, mesh_cuis):
    relationships = []
    mesh_set = set(mesh_cuis)

    for row in stream_rrf(mrrel_path):
        cui1 = row[0]
        rel = row[3]
        cui2 = row[4]
        suppress = row[14]
        if suppress == "Y":
            continue
        if rel != "CHD":
            continue
        if cui1 in mesh_set and cui2 in mesh_set:
            relationships.append({
                "child": cui1,
                "parent": cui2    })
    return relationships


