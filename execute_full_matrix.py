import subprocess
import time

# The Expanded Scenario-Dependent Matrix
ue_densities = [20, 40, 60, 80, 100]
bandwidths = [50.0, 100.0]
distances = [20.0, 100.0, 300.0]
frequency = 3.5e9  # 3.5 GHz baseline (FR1)

print("==================================================")
print("STARTING FULL SCENARIO-DEPENDENT MATRIX")
print("==================================================")

for bw in bandwidths:
    for dist in distances:
        for ues in ue_densities:
            print(f"\n---> Running: {ues} UEs | {bw} MHz | {dist}m")
            
            # Construct the exact terminal command
            command = f'./ns3 run "xr-thesis --nUes={ues} --bandwidth={bw} --frequency={frequency} --distance={dist}"'
            
            # Execute the command
            subprocess.run(command, shell=True)
            
            # Brief pause to clear MAC queues between runs
            time.sleep(1) 

print("\n==================================================")
print("MATRIX COMPLETE. DATA GENERATED.")
print("==================================================")
