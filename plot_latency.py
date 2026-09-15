import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# The parameters you swept
timers = [2, 10, 20, 50]
cycles = [10, 20, 40, 80]

# Initialize matrix for Average Latency (ms)
latency_matrix = np.zeros((len(timers), len(cycles)))

print("Executing Analytical MAC-Layer Latency Model...")

for i, timer in enumerate(timers):
    for j, cycle in enumerate(cycles):
        # 1. Baseline 5G SA Processing Delay
        baseline_latency = 2.5 
        
        # 2. Probability of entering Sleep State between XR frames (16ms interval)
        p_sleep = max(0.0, 1.0 - (timer / 16.0)) 
        
        # 3. Expected Buffering Delay (Average wait is half the cycle length)
        expected_buffering = cycle / 2.0
        
        # Calculate final analytical average
        avg_latency_ms = baseline_latency + (p_sleep * expected_buffering)
        latency_matrix[i, j] = avg_latency_ms

# Generate the Latency Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(latency_matrix, annot=True, fmt=".2f", xticklabels=cycles, yticklabels=timers, cmap="Blues")
plt.title("XR Headset Average Latency (ms)\n(Analytical 3GPP MAC Model)")
plt.xlabel("C-DRX Long Cycle Length (ms)")
plt.ylabel("Inactivity Timer (ms)")
plt.tight_layout()

plt.savefig("cdrx_latency_analytical.png", dpi=300)
print("Success! Plot saved as cdrx_latency_analytical.png")
