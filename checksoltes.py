import itertools
from itertools import combinations

def generate_hyperedges(n, k, s):
    hyperedges = []
    for i in range(n):
        hyperedge = [i]
        hyperedge += [(i + s + j + 1) % n for j in range(k - 2)]
        hyperedge.append((i + k - 2 + 2 * s + 1) % n)
        hyperedges.append(hyperedge)
    return hyperedges

def bfs_distance(start, adjacency):
    queue = [(start, 0)]
    visited = {start: 0}
    while queue:
        node, dist = queue.pop(0)
        for neighbor in adjacency.get(node, []):  # Handle missing keys
            if neighbor not in visited:
                visited[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))
    return visited

def compute_wiener_index(n, hyperedges):
    """Compute the Wiener index of the hypergraph."""
    adjacency = {i: set() for i in range(n)}
    for edge in hyperedges:
        for u, v in combinations(edge, 2):
            adjacency[u].add(v)
            adjacency[v].add(u)

    wiener_index = sum(sum(bfs_distance(v, adjacency).values()) for v in adjacency) // 2
    diameter = max(max(bfs_distance(v, adjacency).values()) for v in adjacency)
    return wiener_index, diameter

def check_soltes_condition(n, k, s, verbose=True):
    if k < 3 or 2 * s + k > n:
        if verbose:
            print(f"Invalid parameters: n={n}, k={k}, s={s} (violates feasibility)")
        return False

    hyperedges = generate_hyperedges(n, k, s)

    wiener_full, diameter_full = compute_wiener_index(n, hyperedges)
    print (wiener_full)
    print (diameter_full)
    # Create new hyperedges excluding vertex 0
    hyperedges_without_0 = [list(filter(lambda v: v != 0, edge)) for edge in hyperedges if 0 not in edge]
    remaining_vertices = set(range(1, n))  # Exclude 0

    # Recompute adjacency for the new graph
    adjacency_reduced = {v: set() for v in remaining_vertices}
    for edge in hyperedges_without_0:
        for u, v in combinations(edge, 2):
            if u in adjacency_reduced and v in adjacency_reduced:
                adjacency_reduced[u].add(v)
                adjacency_reduced[v].add(u)

    # Compute Wiener index and diameter after removing vertex 0
    wiener_removed = sum(sum(bfs_distance(v, adjacency_reduced).values()) for v in adjacency_reduced) // 2
    diameter_removed = max(max(bfs_distance(v, adjacency_reduced).values()) for v in adjacency_reduced)
    print (wiener_removed)
    print (diameter_removed)
    if wiener_full == wiener_removed:
        if verbose:
            print(f"✔ Valid: n={n}, k={k}, s={s}")
            print(f"  Wiener Index: {wiener_full} (same after removal)")
            print(f"  Diameters: full={diameter_full}, after removal={diameter_removed}")
        return True
    else:
       # if verbose:
        #    print(f"✘ Invalid: n={n}, k={k}, s={s}")
         #   print(f"  Wiener Index (full): {wiener_full}")
          #  print(f"  Wiener Index (removed 0): {wiener_removed}")
           # print(f"  Diameters: full={diameter_full}, after removal={diameter_removed}")
        return False
#for n in range(180,200):
  #  s_values=[18,19,20,21,22,23]
   # k_values=[134,136,138,140,142,144, 146, 148, 150, 152, 154, 156]
   # for k in k_values:
    #    for s in s_values:
check_soltes_condition(258, 194, 16)
