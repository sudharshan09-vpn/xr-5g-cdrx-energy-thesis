import pandas as pd
import matplotlib.pyplot as plt

print("==================================================")
print("GENERATING PARETO FRONTIER VISUALIZATIONS")
print("==================================================")

# 1. LOAD THE MATRIX
try:
    df = pd.read_csv("phase2_pareto_data.csv")
except FileNotFoundError:
    print("Error: phase2_pareto_data.csv not found. Run generate_graphs.py first.")
    exit()

# 2. INITIALIZE PLOT ARCHITECTURE
fig, ax = plt.subplots(figsize=(12, 7))

# 3. PLOT THE DATA POINTS (Colored by UE Density)
# Using a colormap to clearly separate 20, 40, 60, 80, and 100 UE blocks
scatter = ax.scatter(
    df['Avg_Energy_J'], 
    df['Avg_Latency_ms'], 
    c=df['N_UEs'], 
    cmap='viridis', 
    s=120, 
    alpha=0.85, 
    edgecolors='black',
    linewidth=0.75,
    zorder=3
)

# 4. DRAW THE XR BOUNDARY CONDITION
# The absolute physical limit for motion-to-photon delay
ax.axhline(y=10.0, color='red', linestyle='--', linewidth=2, zorder=2, label='XR Latency Threshold (10 ms)')

# 5. FORMATTING & AESTHETICS
ax.set_title('5G Standalone Capacity Constraint: Energy Efficiency vs. XR Latency', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Baseband Energy Consumption (Joules)', fontsize=12, fontweight='bold')
ax.set_ylabel('Average MAC Layer Latency (ms)', fontsize=12, fontweight='bold')

# Add the colorbar legend for UE Density
cbar = plt.colorbar(scatter)
cbar.set_label('Network Density (Number of UEs)', fontsize=12, fontweight='bold')

# Clean grid for readability
ax.grid(True, linestyle=':', alpha=0.6, zorder=1)
ax.legend(loc='upper left', fontsize=11)

# 6. EXPORT THE MASTER VISUAL
output_filename = "pareto_frontier_XR_capacity.png"
plt.tight_layout()
plt.savefig(output_filename, dpi=300)

print(f">>> VISUAL SUCCESSFULLY EXPORTED TO: {output_filename}")
