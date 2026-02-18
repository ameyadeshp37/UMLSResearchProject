
def find_mesh_seed(concepts_dict, keyword):
    for cui, name in concepts_dict.items():
        if keyword.lower() in name.lower():
            return cui
    raise ValueError(f"Seed term '{keyword}' not found in MeSH concepts.")