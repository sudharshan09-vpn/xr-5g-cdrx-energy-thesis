import pandas as pd
import glob
import re
import xml.etree.ElementTree as ET

print("==================================================")
print("INITIATING PHASE 2 PARSING: EE vs. CAPACITY MATRIX")
print("==================================================")

# 1. PARSE ENERGY EFFICIENCY (EE) FROM CSVs
csv_files = glob.glob("power_logs/*.csv")
energy_results = {}

for file in csv_files:
    match = re.search(r'ues(\d+)_timer(\d+)_cycle(\d+)', file)
    if match:
        n_ues, timer, cycle = int(match.group(1)), int(match.group(2)), int(match.group(3))
        
        # ERROR HANDLING INJECTED HERE
        try:
            df = pd.read_csv(file)
            df['Energy_J'] = (df['Current_mA'] / 1000.0) * 3.8 * 0.001
            avg_energy = df.groupby('UE_ID')['Energy_J'].sum().mean()
            energy_results[(n_ues, timer, cycle)] = avg_energy
        except pd.errors.EmptyDataError:
            print(f"Skipping crashed run (Empty File): {file}")
            continue

# 2. PARSE CAPACITY / LATENCY (Pi) FROM XMLs
xml_files = glob.glob("simulation_results/*.xml")
final_results = []

for file in xml_files:
    match = re.search(r'ues(\d+)_timer(\d+)_cycle(\d+)', file)
    if match:
        n_ues, timer, cycle = int(match.group(1)), int(match.group(2)), int(match.group(3))
        
        tree = ET.parse(file)
        root = tree.getroot()
        
        total_tx = 0
        total_rx = 0
        delay_sum_ns = 0.0
        
        # Aggregate flow metrics to calculate latency and reliability
        for flow in root.findall('.//Flow'):
            total_tx += int(flow.get('txPackets', 0))
            total_rx += int(flow.get('rxPackets', 0))
            
            delay_str = flow.get('delaySum')
            if delay_str:
                # ns-3 formats delays as '+10000.0ns'
                delay_ns = float(delay_str.replace('+', '').replace('ns', ''))
                delay_sum_ns += delay_ns
                
        pdr = (total_rx / total_tx) * 100 if total_tx > 0 else 0.0
        avg_latency_ms = (delay_sum_ns / total_rx) / 1e6 if total_rx > 0 else float('inf')
        
        # Link the Energy data to the Latency data
        avg_energy = energy_results.get((n_ues, timer, cycle), float('nan'))
        
        final_results.append({
            'N_UEs': n_ues,
            'Timer_ms': timer,
            'Cycle_ms': cycle,
            'Avg_Energy_J': round(avg_energy, 4),
            'Avg_Latency_ms': round(avg_latency_ms, 2),
            'PDR_%': round(pdr, 2)
        })

# 3. BUILD THE MATRIX AND EXPORT
master_df = pd.DataFrame(final_results)
master_df = master_df.sort_values(by=['N_UEs', 'Timer_ms', 'Cycle_ms'])

print(master_df.to_string(index=False, max_rows=15))
print("...")
print(f"Total metrics compiled: {len(master_df)}")

master_df.to_csv("phase2_pareto_data.csv", index=False)
print(">>> EXPORTED MASTER DATA TO: phase2_pareto_data.csv")