#Deque Import Needed
from collections import deque

def expand_mesh(seed_cui, relationships, hops=3):
    visited = {seed_cui}
    queue = deque([(seed_cui, 0)])
    edges = []

    children_map = {}

    for rel in relationships:
        parent = rel["parent"]
        child = rel["child"]
        children_map.setdefault(parent, []).append(child)

    while queue:
        current_cui, depth = queue.popleft()
        if depth >= hops:
            continue
        for child in children_map.get(current_cui, []):
            edges.append((current_cui, child, "IS_A"))
            if child not in visited:
                visited.add(child)
                queue.append((child, depth + 1))

    return visited, edges