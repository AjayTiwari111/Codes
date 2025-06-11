import itertools

def generate_hyperedges(n, k, s):
    hyperedges = []
    for i in range(n):
        hyperedge = [i]
        hyperedge += [(i + s + j + 1) % n for j in range(k - 2)]
        hyperedge.append((i + k - 2 + 2 * s + 1) % n)
        hyperedges.append(hyperedge)
    return hyperedges

def find_nonzero_pairs_only_in_zero_edges(hyperedges, s):
    """Finds the number of exclusive nonzero pairs for each vertex in range(1, s+1)."""
    pairs_in_zero = {i: set() for i in range(1, s + 1)}
    pairs_in_nonzero = set()

    for edge in hyperedges:
        pair_set = {tuple(sorted((u, v))) for u, v in itertools.combinations(edge, 2)}
        if 0 in edge:
            for pair in pair_set:
                if 0 not in pair:
                    u, v = pair
                    if u in pairs_in_zero:
                        pairs_in_zero[u].add(pair)
                    if v in pairs_in_zero:
                        pairs_in_zero[v].add(pair)
        else:
            pairs_in_nonzero.update(pair_set)

    # Compute exclusive pairs per vertex
    exclusive_info = {}
    for i in range(1, s + 1):
        exclusive_pairs = pairs_in_zero[i] - pairs_in_nonzero
        exclusive_info[i] = {
            "count": len(exclusive_pairs),
            "pairs": sorted(exclusive_pairs)
        }
    return exclusive_info

# Define test cases
test_cases = [
    (92, 48, 15),
    (93, 50, 15), (94, 52, 15),
    (95, 54, 15),
    (96, 56, 15), (97, 58, 15), (98, 60, 15), (99, 62, 15), (100, 64, 15),
    (101, 66, 15), (102, 68, 15), (103, 70, 15), (104, 72, 15), (105, 74, 15)
]

# Open output file
output_file = "exclusive_pairs_output.txt"
with open(output_file, "w") as f:
    for n, k, s in test_cases:
        hyperedges = generate_hyperedges(n, k, s)
        exclusive_info = find_nonzero_pairs_only_in_zero_edges(hyperedges, s)

        header = f"\nResults for (n={n}, k={k}, s={s}):"
        print(header)
        f.write(header + "\n")

        for v in range(1, s + 1):
            count_line = f"Vertex {v}: {exclusive_info[v]['count']} exclusive pairs"
            print(count_line)
            f.write(count_line + "\n")
            for pair in exclusive_info[v]['pairs']:
                pair_line = f"  {pair}"
                print(pair_line)
                f.write(pair_line + "\n")

print(f"\n Output written to {output_file}")
