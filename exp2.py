from collections import deque
import math
import itertools
import networkx as nx

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def construct_hypergraph(n, k, s):
    hyperedges = []
    for i in range(n):
        # Forward hyperedge
        forward_edge = [(i + j) % n for j in range(k - 1)] + [(i + k + s - 1) % n]
        if len(set(forward_edge)) == k:  # Ensure no duplicate vertices
            hyperedges.append(tuple(forward_edge))
    return hyperedges

def calculate_distances(hyperedges, n):
    distances = [[float('inf')] * n for _ in range(n)]
    for start_node in range(n):
        distances[start_node][start_node] = 0
        queue = deque([(start_node, 0)])
        visited = {start_node}

        while queue:
            current_node, current_distance = queue.popleft()
            for edge in hyperedges:
                if current_node in edge:
                    for neighbor in edge:
                        neighbor_index = neighbor
                        if neighbor_index not in visited:
                            distances[start_node][neighbor_index] = min(distances[start_node][neighbor_index], current_distance + 1)
                            queue.append((neighbor_index, current_distance + 1))
                            visited.add(neighbor_index)
    return distances

def remove_vertex(hyperedges, vertex):
    new_hyperedges = []
    for edge in hyperedges:
        if vertex not in edge:
            new_hyperedges.append(edge)
    return new_hyperedges

def wiener_index_change(n, k, s, vertex_to_remove):
    hyperedges = create_hypergraph(n, k, s)
    distances_original = calculate_distances(hyperedges, n)
    wiener_original = wiener_index(distances_original)

    hyperedges_removed = remove_vertex(hyperedges, vertex_to_remove)
    distances_removed = calculate_distances(hyperedges_removed, n)
    wiener_removed = wiener_index(distances_removed)

    return wiener_removed - wiener_original

def visualize_hypergraph(hyperedges):
    for i, edge in enumerate(hyperedges):
        print(f"Edge {i + 1}: {edge}")

def is_connected(hyperedges, n):
    visited = {0}
    queue = deque([0])
    while queue:
        current_node = queue.popleft()
        for edge in hyperedges:
            if current_node in edge:
                for neighbor in edge:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
    return len(visited) == n

def compute_wiener_index(hyperedges, n):
    G = nx.Graph()
    for edge in hyperedges:
        for u, v in itertools.combinations(edge, 2):
            G.add_edge(u, v)

    wiener_index = sum(nx.shortest_path_length(G, source=u, target=v)
                        for u, v in itertools.combinations(G.nodes, 2))
    return wiener_index

def compute_wiener_index_after_deletion(hyperedges, n, v):
    G = nx.Graph()
    for edge in hyperedges:
        if v not in edge:
            for u, w in itertools.combinations(edge, 2):
                G.add_edge(u, w)

    wiener_index = sum(nx.shortest_path_length(G, source=u, target=w)
                        for u, w in itertools.combinations(G.nodes, 2))
    return wiener_index

def compute_distance_distribution(hyperedges, n, graph_name):
    G = nx.Graph()
    for edge in hyperedges:
        for u, v in itertools.combinations(edge, 2):
            G.add_edge(u, v)

    # Compute shortest path lengths for all vertex pairs
    shortest_paths = dict(nx.all_pairs_shortest_path_length(G))

    # Find the diameter of the graph
    diameter = max(max(lengths.values()) for lengths in shortest_paths.values())

    # Count vertex pairs at each distance
    distance_count = {d: 0 for d in range(1, diameter + 1)}

    for u in G.nodes:
        for v in G.nodes:
            if u < v:  # Avoid double counting
                d = shortest_paths[u][v]
                if d in distance_count:
                    distance_count[d] += 1

    # Print results
    print(f"\nDistance distribution for {graph_name}:")
    for d, count in distance_count.items():
        print(f"Pairs at distance {d}: {count}")

    print(f"Diameter of {graph_name}: {diameter}")

    return diameter


def compute_sigma_v(hyperedges_removed, n):
    G = nx.Graph()
    for edge in hyperedges_removed:
        for u, v in itertools.combinations(edge, 2):
            G.add_edge(u, v)

    sigma_values = {}
    for v in G.nodes:
        sigma_v = sum(nx.shortest_path_length(G, source=v, target=u) for u in G.nodes if u != v)
        sigma_values[v] = sigma_v

    print("Sigma(v) values in the vertex-deleted graph:")
    for v, sigma_v in sigma_values.items():
        print(f"σ({v}) = {sigma_v}")


def pairs_in_edge(hyperedges, v, u):
    G=nx.Graph()
    c=0
    for edge in hyperedges:
        if v in edge and u in edge:
            c+=1
    print(f"pair {v} {u} in: ", c)

# Example usage
vertex_to_remove = 0

# Test with n = 12, k = 7, s = 2
n = 14
k = 5
s = 3

#hyperedges = construct_hypergraph(n, k, s)
#for n in range(10, 20):
#    for k in range(3, n):  # k > 2
#        for s in range(n):
hyperedges = construct_hypergraph(n, k, s)
hyperedges_removed = remove_vertex(hyperedges, vertex_to_remove)
def count_distinct_nonzero_pairs(hyperedges):
    """ Counts distinct vertex pairs (u, v) in hyperedges containing 0, excluding pairs with 0. """
    pairs_set = set()
    for edge in hyperedges:
        if 0 in edge:  # Consider only hyperedges that include 0
            nonzero_vertices = [v for v in edge if v != 0]  # Exclude 0
            for u, v in itertools.combinations(nonzero_vertices, 2):  # Unique (u, v) pairs
                pairs_set.add(tuple(sorted((u, v))))  # Store (u, v) uniquely

    sorted_pairs = sorted(pairs_set)  # Sort pairs by first vertex
    return len(sorted_pairs), sorted_pairs

# Example usage (after constructing hypergraph)
distinct_count, distinct_pairs = count_distinct_nonzero_pairs(hyperedges)
print("Number of distinct nonzero pairs:", distinct_count)
print("Distinct nonzero pairs (sorted):")
for pair in distinct_pairs:
    print(pair)


def count_distinct_pairs_excluding_zero(hyperedges):
    """ Finds distinct vertex pairs (u, v) in edges that do NOT contain 0. """
    pairs_set = set()
    for edge in hyperedges:
        if 0 not in edge:  # Only consider hyperedges that do NOT contain 0
            for u, v in itertools.combinations(edge, 2):  # Unique (u, v) pairs
                pairs_set.add(tuple(sorted((u, v))))  # Store (u, v) uniquely

    sorted_pairs = sorted(pairs_set)  # Sort pairs by first vertex
    return len(sorted_pairs), sorted_pairs

# Example usage (after constructing hypergraph)
distinct_count_excl_zero, distinct_pairs_excl_zero = count_distinct_pairs_excluding_zero(hyperedges)
print("Number of distinct pairs in edges NOT containing 0:", distinct_count_excl_zero)
print("Distinct pairs (sorted):")
for pair in distinct_pairs_excl_zero:
    print(pair)


#print(hyperedges)
#if not hyperedges:  # Skip invalid cases
 #   continue
#            w_h = compute_wiener_index(hyperedges, n)
 #           w_h_v = compute_wiener_index_after_deletion(hyperedges, n, 0)
  #          if w_h - w_h_v == 0 and w_h==math.comb(n, 2):

   #             print("----start----")
    #            print(n,k,s)
     #           diameter_original = compute_distance_distribution(hyperedges, n, "Original Graph")
      #          diameter_deleted = compute_distance_distribution(hyperedges_removed, n, "Vertex-Deleted Graph")
       #         print("----break----")
