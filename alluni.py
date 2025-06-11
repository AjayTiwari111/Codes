from itertools import combinations
from collections import defaultdict

def generate_hyperedges(n, k, s):
    """Construct k-uniform hyperedges based on n, k, s."""
    hyperedges = []
    for i in range(n):
        hyperedge = [i]
        hyperedge += [(i + s + j + 1) % n for j in range(k - 2)]
        hyperedge.append((i + k - 2 + 2 * s + 1) % n)
        hyperedges.append(hyperedge)
    return hyperedges

def bfs_distance(start, adjacency):
    """Standard BFS to compute shortest path distances from start."""
    queue = [(start, 0)]
    visited = {start: 0}
    while queue:
        node, dist = queue.pop(0)
        for neighbor in adjacency.get(node, []):
            if neighbor not in visited:
                visited[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))
    return visited

def compute_wiener_index(n, hyperedges):
    """Compute the Wiener index and diameter of the hypergraph."""
    adjacency = {i: set() for i in range(n)}
    for edge in hyperedges:
        for u, v in combinations(edge, 2):
            adjacency[u].add(v)
            adjacency[v].add(u)

    wiener_index = sum(sum(bfs_distance(v, adjacency).values()) for v in adjacency) // 2
    diameter = max(max(bfs_distance(v, adjacency).values()) for v in adjacency)
    return wiener_index, diameter

def find_valid_parameters_by_s(s):
    """Fix s and search over k in a derived range, and n in range [k + 2s, k + 3s]."""
    from math import comb

    valid_results = []
    k_start = comb(s-2, 2)-2
    k_end = comb(s-2, 2)+2

    for k in range(k_start, k_end + 1):
        for n in range(k + 2 * (s-2), k + 4*(s-2)):
            if k >= 3 and 2 * (s-2) + k <= n:  # Feasibility check
                hyperedges = generate_hyperedges(n, k, s-2)
                wiener_full, diameter_full = compute_wiener_index(n, hyperedges)

                # Remove vertex 0
                hyperedges_wo_0 = [list(filter(lambda v: v != 0, edge)) for edge in hyperedges if 0 not in edge]
                remaining_vertices = set(range(1, n))
                adjacency_reduced = {v: set() for v in remaining_vertices}
                for edge in hyperedges_wo_0:
                    for u, v in combinations(edge, 2):
                        if u in adjacency_reduced and v in adjacency_reduced:
                            adjacency_reduced[u].add(v)
                            adjacency_reduced[v].add(u)

                wiener_removed = sum(sum(bfs_distance(v, adjacency_reduced).values()) for v in adjacency_reduced) // 2
                diameter_removed = max(max(bfs_distance(v, adjacency_reduced).values()) for v in adjacency_reduced)

                if wiener_full == wiener_removed:
                    valid_results.append((n, k, s-2))
                    print(f"Valid (n={n}, k={k}, s={s})")
                    print(f"  Wiener Index (full): {wiener_full}, Diameter (full): {diameter_full}")
                    print(f"  Wiener Index (removed 0): {wiener_removed}, Diameter (removed 0): {diameter_removed}")

    return valid_results

s = 13  # Change this to any fixed s value
valid_triplets = find_valid_parameters_by_s(s)

print(f"\n=== All valid (n, k, s={s}) parameters ===")
print(valid_triplets)

"""
# === Display results grouped and sorted by k ===
all_valid_params = []

print("\n=== Valid Parameters Grouped by k ===")
for k in sorted(valid_results):
    params = sorted(valid_results[k])  # sort by (n, s)
    print(f"\nk = {k}:")
    for n, _, s in params:
        print(f"  (n={n}, s={s})")
        all_valid_params.append((n, k, s))

# === Report k values with no valid parameters ===
k_with_no_results = [k for k in k_values if k not in valid_results]
print("\n=== k values with NO valid parameters ===")
print(k_with_no_results)

# === Flattened list of all valid (n, k, s) triples ===
print("\n=== All valid (n, k, s) parameters ===")
print(all_valid_params)"""
