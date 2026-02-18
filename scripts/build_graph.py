import yaml
from pathlib import Path

from src.umls_io import load_mesh_concepts, load_mesh_relationships
from src.seed import find_mesh_seed
from src.expand import expand_mesh
from src.build_tables import build_nodes, build_edges


def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    umls_dir = Path(config["umls"]["dir"])

    # Load MeSH concepts + hierarchy
    concepts = load_mesh_concepts(umls_dir / config["umls"]["mrconso"])
    relationships = load_mesh_relationships(umls_dir / config["umls"]["mrrel"])

    # Find seed CUI
    seed_term = config["seed"]["mesh_strings"][0]
    seed_cui = find_mesh_seed(concepts, seed_term)

    print(f"Seed CUI found: {seed_cui}")

    # Expand hierarchy
    visited_cuis, edge_list = expand_mesh(
        seed_cui,
        relationships,
        hops=config["graph"]["hops"] )

    print(f"Total nodes in graph: {len(visited_cuis)}")
    print(f"Total edges in graph: {len(edge_list)}")

    # Build tables
    nodes_df = build_nodes(concepts, visited_cuis)
    edges_df = build_edges(edge_list)

    # Save outputs
    Path("outputs").mkdir(exist_ok=True)

    nodes_df.to_csv(config["export"]["nodes_csv"], index=False)
    edges_df.to_csv(config["export"]["edges_csv"], index=False)

    print("MeSH graph successfully generated.")

if __name__ == "__main__":
    main()