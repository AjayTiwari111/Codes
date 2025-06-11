def construct_hypergraph(n, k, s):
    hyperedges = []
    for i in range(n):
        edge = []
        index = i
        edge.append(index % n)

        # Step 1: skip s, include 1
        index += s + 1
        edge.append(index % n)

        # Step 2: skip s, include (k - 4)
        index += s
        for _ in range(max(0, k - 4)):
            index += 1
            edge.append(index % n)

        # Step 3: skip s, include 1
        index += s + 1
        edge.append(index % n)

        # Step 4: skip s, include 1
        index += s + 1
        edge.append(index % n)

        edge = sorted(set(edge))  # remove duplicates
        hyperedges.append(edge)

    return hyperedges

def remove_vertex_completely(hyperedges, vertex_to_remove):
    return [edge for edge in hyperedges if vertex_to_remove not in edge]

# Parameters
n = 11
k = 6
s = 2

# Construct original hypergraph
hypergraph = construct_hypergraph(n, k, s)

# Construct H \ 0 (delete all edges containing vertex 0)
hypergraph_without_0 = remove_vertex_completely(hypergraph, 0)

# Print original hyperedges
print("Original hyperedges:")
for i, edge in enumerate(hypergraph):
    print(f"Edge {i}: {edge}")

# Print hyperedges after deleting vertex 0
print("\nHyperedges after deleting vertex 0 (i.e., all edges not containing 0):")
for i, edge in enumerate(hypergraph_without_0):
    print(f"Edge {i}: {edge}")
