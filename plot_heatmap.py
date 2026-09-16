import os
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# The parameters you swept
timers = [2, 10, 20, 50]
cycles = [10, 20, 40, 80]

# Initialize a matrix to store energy consumed
energy_matrix = np.zeros((len(timers), len(cycles)))

for i, timer in enumerate(timers):
    for j, cycle in enumerate(cycles):
        filepath = f"simulation_results/xr_kpi_timer{timer}_cycle{cycle}.txt"
        remaining_energy = 10000.0 # Starting baseline
        
        try:
            with open(filepath, 'r') as file:
                content = file.read()
                # Parse the standard output for the remaining energy log
                match = re.search(r"Remaining Energy:\s+([\d\.]+)\s+Joules", content)
                if match:
                    remaining_energy = float(match.group(1))
        except FileNotFoundError:
            print(f"File missing: {filepath}")
            
        # Calculate total consumed during the run
        energy_consumed = 10000.0 - remaining_energy
        energy_matrix[i, j] = energy_consumed

# Generate the Heatmap
plt.figure(figsize=(8, 6))
# In plot_heatmap.py
sns.heatmap(energy_matrix, annot=True, fmt=".2f", xticklabels=cycles, yticklabels=timers, cmap="YlOrRd", cbar_kws={'label': 'Total Energy (Joules)'})
plt.title("XR Headset Energy Consumed (Joules)\nby C-DRX Parameters")
plt.xlabel("C-DRX Long Cycle Length (ms)")
plt.ylabel("Inactivity Timer (ms)")
plt.tight_layout()
plt.savefig("cdrx_energy_heatmap.png", dpi=300)
print("Success! Plot saved as cdrx_energy_heatmap.png")
