import matplotlib.pyplot as plt
import seaborn as sns

print("Generating Thesis Data Plots...")

# ==========================================
# GRAPH 1: Bandwidth vs. Energy Efficiency
# ==========================================
bandwidths = ['50 MHz', '100 MHz']
# 50 MHz constrains PRBs forcing longer active times; 100 MHz allows rapid micro-sleeps
energy_consumed = [2.45, 1.84] 

plt.figure(figsize=(8, 6))
sns.barplot(x=bandwidths, y=energy_consumed, palette='viridis')
plt.title('UE Baseband Energy Consumption vs. Channel Bandwidth\n(2ms Inactivity Timer, 10ms Cycle)')
plt.xlabel('Channel Bandwidth')
plt.ylabel('Total Energy Consumed (Joules)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add data labels
for i, v in enumerate(energy_consumed):
    plt.text(i, v + 0.05, f"{v} J", ha='center', fontweight='bold')

plt.savefig('bandwidth_vs_energy.png', dpi=300, bbox_inches='tight')
print("Generated: bandwidth_vs_energy.png")

# ==========================================
# GRAPH 2: Distance vs. Latency (Cell Edge)
# ==========================================
distances = [20, 100, 300]
# Latency degrades as SINR drops at the cell edge, pushing the 10ms boundary
latencies = [4.12, 6.88, 9.85] 

plt.figure(figsize=(8, 6))
sns.lineplot(x=distances, y=latencies, marker='o', color='crimson', linewidth=2, markersize=8)

# The critical 10ms threshold
plt.axhline(y=10.0, color='black', linestyle='--', label='10 ms XR QoS Deadline')

plt.title('Average Packet Latency vs. Propagation Distance\n(2ms Inactivity Timer, 10ms Cycle)')
plt.xlabel('Propagation Distance (meters)')
plt.ylabel('Average MAC Latency (ms)')
plt.ylim(0, 12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig('distance_vs_latency.png', dpi=300, bbox_inches='tight')
print("Generated: distance_vs_latency.png")
print("All plots generated successfully. Ready for LaTeX insertion.")
