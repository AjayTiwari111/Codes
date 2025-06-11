import itertools
from itertools import combinations

def generate_hyperedges(n, k, s):
    """
    Construct hyperedges:
    - Take 2 vertices
    - Skip s
    - Take k - 4 vertices
    - Skip s
    - Take 2 vertices
    """
    hyperedges = []
    for i in range(n):
        edge = []

        # First 2 vertices
        for j in range(2):
            edge.append((i + j) % n)

        # Skip s, then take k - 4 vertices
        start_mid = (i + 2 + s) % n
        for j in range(k - 4):
            edge.append((start_mid + j) % n)

        # Skip another s, then take final 2 vertices
        start_end = (start_mid + (k - 4) + s) % n
        for j in range(2):
            edge.append((start_end + j) % n)

        hyperedges.append(edge)

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

def find_valid_parameters(n_start, n_end):
    valid_params = []
    for n in range(n_start, n_end + 1):
        d=int(n/2)
        #for k in range(103, 111, 2):
        for k in range(d, n+1): #replaced n+1
            for s in range(0, 30):
                if k >= 3 and 2 * s + k <= n:  # Basic feasibility condition
                    hyperedges = generate_hyperedges(n, k, s)

                    wiener_full, diameter_full = compute_wiener_index(n, hyperedges)

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

                    wiener_removed, diameter_removed = sum(sum(bfs_distance(v, adjacency_reduced).values()) for v in adjacency_reduced) // 2, \
                                                       max(max(bfs_distance(v, adjacency_reduced).values()) for v in adjacency_reduced)

                    if wiener_full == wiener_removed: #and diameter_full == 1 and diameter_removed == 2:
                        valid_params.append((n, k, s))
                        print(f"Valid case: n={n}, k={k}, s={s}")
                        print(f"  Wiener Index (full): {wiener_full}, Diameter (full): {diameter_full}")
                        print(f"  Wiener Index (removed 0): {wiener_removed}, Diameter (removed 0): {diameter_removed}")


    return valid_params

# Example usage:
n_start = 101  # Starting value of n
n_end = 150   # Ending value of n

valid_values = find_valid_parameters(n_start, n_end)
print("Valid (n, k, s) values where Wiener index is unchanged:", valid_values) #not checking diam(H)=1, diam(Hwithout0)=2



#find 0 pairs
def find_nonzero_pairs_only_in_zero_edges(hyperedges):
    """ Finds pairs (u, v) (where u ≠ 0, v ≠ 0) that appear only in
        hyperedges containing 0 and NOT in hyperedges without 0.
    """
    pairs_in_zero = set()
    pairs_in_nonzero = set()

    for edge in hyperedges:
        pair_set = {tuple(sorted((u, v))) for u, v in itertools.combinations(edge, 2)}
        if 0 in edge:
            pairs_in_zero.update({pair for pair in pair_set if 0 not in pair})
        else:
            pairs_in_nonzero.update(pair_set)

    exclusive_pairs = sorted(pairs_in_zero - pairs_in_nonzero)  # Set difference and sorting

    # Step 3: Identify hyperedges that contain exclusive pairs
    edges_with_exclusive_pairs = []
    for edge in hyperedges:
        edge_pairs = {tuple(sorted((u, v))) for u, v in itertools.combinations(edge, 2)}
        if exclusive_pairs and edge_pairs & set(exclusive_pairs):  # Check if any exclusive pair is in the edge
            edges_with_exclusive_pairs.append(edge)
    # Print the hyperedges containing the exclusive pairs
    print("\nHyperedges containing exclusive pairs:")
    for edge in edges_with_exclusive_pairs:
        print(edge)



    # Print final sets
    print("\nTotal pairs_in_zero:", len(pairs_in_zero))
    print("Total pairs_in_nonzero:", len(pairs_in_nonzero))

    return len(exclusive_pairs), exclusive_pairs

def print_edges_with_additional_pairs(hyperedges, n):
    counted_pairs = set()
    for idx in range(1, n):  # Print in order 1,2,...,n-1,0
        edge = hyperedges[idx % n]
        edge_pairs = {tuple(sorted((u, v))) for u, v in itertools.combinations(edge, 2)}
        new_pairs = edge_pairs - counted_pairs
        counted_pairs.update(new_pairs)
        print(f"{idx}st edge: {edge} additional distinct pairs: {len(new_pairs)}")
        if new_pairs:
            print(", ".join(map(str, sorted(new_pairs))))
        print()

# Example usage (after constructing hypergraph)
n=11
k=5
s=2
hyperedges = generate_hyperedges(n, k, s)
exclusive_count, exclusive_pairs = find_nonzero_pairs_only_in_zero_edges(hyperedges)
print("Number of nonzero pairs appearing only in edges with 0:", exclusive_count)

print_edges_with_additional_pairs(hyperedges, n)

print("Exclusive nonzero pairs (sorted):")
for pair in exclusive_pairs:
    print(pair)
