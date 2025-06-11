import matplotlib.pyplot as plt

def binom(n):
    return n * (n - 1) // 2

# Original dataset (Formula 1)
s_range = range(0, 21)
m_range = range(4, 21)
s_vals_1, k_vals_1 = [], []
k_set_1 = set()

for s in s_range:
    for m in m_range:
        k = binom(s) + binom(m) - 2 * s
        while k < 160:
            s_vals_1.append(s)
            k_vals_1.append(k)
            k_set_1.add(k)

# Second dataset (Formula 2)
s_vals_2, k_vals_2 = [], []
k_set_2 = set()

for s in range(2, 21):  # s must be at least 2 for t in [0, s-2]
    for t in range(0, s - 1):
        k = binom(s) - 2 * t - 2 * s - 1
        while k<160:
            s_vals_2.append(s)
            k_vals_2.append(k)
            k_set_2.add(k)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(s_vals_1, k_vals_1, color='blue', label=r"$k = \binom{s}{2} + \binom{m}{2} - 2s$", alpha=0.6)
plt.scatter(s_vals_2, k_vals_2, color='red', label=r"$k = \binom{s}{2} - 2t - 2s - 1$", alpha=0.6, marker='x')
plt.xlabel('s')
plt.ylabel('k')
plt.title('Plot of k vs s for Two Formulas')
plt.grid(True)
plt.legend()
plt.xticks(range(0, 21))
plt.show()

# Set comparisons
common_k = sorted(k_set_1 & k_set_2)
only_first_k = sorted(k_set_1 - k_set_2)
only_second_k = sorted(k_set_2 - k_set_1)

# Print results
print("Common k-values:", common_k)
print("\nValues only in the first formula (blue):", only_first_k)
print("\nValues only in the second formula (red):", only_second_k)
