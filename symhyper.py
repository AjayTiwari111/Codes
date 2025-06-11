import itertools
import networkx as nx
import math

def construct_hypergraph(n, k, s):
    hyperedges = []
    for i in range(n):
        # Forward hyperedge
        forward_edge = [(i + j) % n for j in range(k - 1)] + [(i + k + s - 1) % n]
        if len(set(forward_edge)) == k:  # Ensure no duplicate vertices
            hyperedges.append(tuple(forward_edge))

        # Backward hyperedge
        backward_edge = [(i - j) % n for j in range(k - 1)] + [(i - (k + s - 1)) % n]
        if len(set(backward_edge)) == k:  # Ensure no duplicate vertices
            hyperedges.append(tuple(backward_edge))

    return hyperedges

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

def compute_vertex_degrees(hyperedges, n):
    degrees = {i: 0 for i in range(n)}
    for edge in hyperedges:
        for v in edge:
            degrees[v] += 1
    return degrees

def compute_vertex_degrees_after_deletion(hyperedges, n, v):
    degrees = {i: 0 for i in range(n)}
    for edge in hyperedges:
        if v not in edge:
            for u in edge:
                degrees[u] += 1
    return degrees

# Fixed n = 10
n = 28
#k=28
#s=8
valid_configs = []
for n in range(10,40):
    for k in range(3, n):  # k > 2
        for s in range(n):
            hyperedges = construct_hypergraph(n, k, s)
#print(hyperedges)
            #if not hyperedges:  # Skip invalid cases
           # continue
            w_h = compute_wiener_index(hyperedges, n)
            w_h_v = compute_wiener_index_after_deletion(hyperedges, n, 0)
            if w_h - w_h_v == 0 and w_h==math.comb(n, 2):
                print("original: ",n,k,s,w_h)
                print("deleted: ",w_h_v)
                print(n,k,s)
            #if w_h - w_h_v == 0 and w_h==math.comb(n, 2):
#            valid_configs.append((n, k, s))

# Print valid configurations
#for config in valid_configs:
 #   print("Valid (n, k, s):", config)

# Print vertex degrees for n=10
#print("Vertex degrees in original graph:")
#hyperedges = construct_hypergraph(n, 2, 1)  # Example values for k and s
#degrees = compute_vertex_degrees(hyperedges, n)
#print(degrees)

#print("Vertex degrees after deletion of vertex 0:")
#degrees_after_deletion = compute_vertex_degrees_after_deletion(hyperedges, n, 0)
#print(degrees_after_deletion)
