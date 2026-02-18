import pandas as pd

def build_nodes(concepts_dict, keep_cuis):
    rows = []
    for cui in keep_cuis:
        name = concepts_dict.get(cui)

        if name:
            rows.append({
                "node_id": cui,
                "name": name,
                "node_type": "MeSH" })

    return pd.DataFrame(rows)

def build_edges(edge_list):
    return pd.DataFrame(edge_list,
                        columns=["source", "target", "relationship"])