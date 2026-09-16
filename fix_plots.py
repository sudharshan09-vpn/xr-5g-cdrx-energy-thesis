import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

timers = [2, 10, 20, 50]
cycles = [10, 20, 40, 80]

energy_data = np.array([
    [1.84, 1.84, 1.84, 1.84],
    [5.74, 5.74, 5.74, 5.74],
    [8.51, 8.51, 8.51, 8.51],
    [8.55, 8.55, 8.55, 8.55]
])

latency_data = np.array([
    [6.88, 11.25, 20.00, 37.50],
    [4.38, 6.25, 10.00, 17.50],
    [2.50, 2.50, 2.50, 2.50],
    [2.50, 2.50, 2.50, 2.50]
])

# 1. Plot Energy
plt.figure(figsize=(8, 6))
sns.heatmap(energy_data, annot=True, fmt=".2f", xticklabels=cycles, yticklabels=timers, cmap="YlOrRd", cbar_kws={'label': 'Total Energy (Joules)'})
plt.title("XR Headset Energy Consumed (Joules)\nby C-DRX Parameters")
plt.xlabel("C-DRX Long Cycle Length (ms)")
plt.ylabel("Inactivity Timer (ms)")
plt.tight_layout()
plt.savefig("cdrx_energy_heatmap_fixed.png", dpi=300)
plt.close()

# 2. Plot Latency
plt.figure(figsize=(8, 6))
sns.heatmap(latency_data, annot=True, fmt=".2f", xticklabels=cycles, yticklabels=timers, cmap="Blues", cbar_kws={'label': 'Average Latency (ms)'})
plt.title("XR Headset Average Latency (ms)\nby C-DRX Parameters")
plt.xlabel("C-DRX Long Cycle Length (ms)")
plt.ylabel("Inactivity Timer (ms)")
plt.tight_layout()
plt.savefig("cdrx_latency_heatmap_fixed.png", dpi=300)
plt.close()

print("Success! Fixed heatmaps generated.")
