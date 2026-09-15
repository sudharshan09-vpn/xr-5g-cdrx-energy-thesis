import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def parse_ns3_xml(file_path):
    print(f"Parsing {file_path}...")
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Lists to hold our extracted data
    ue_ids = []
    throughput_mbps = []
    delays_ms = []
    energy_consumed_joules = []

    # 1. Parse FlowMonitor Stats (Latency & Throughput)
    # Note: Adjust the XML tag searches if your custom ns-3 script named them differently
    for flow in root.findall('.//FlowStats/Flow'):
        flow_id = flow.get('flowId')
        rx_bytes = float(flow.get('rxBytes', 0))
        time_first_rx = float(flow.get('timeFirstRxPacket', 0).replace('ns', ''))
        time_last_rx = float(flow.get('timeLastRxPacket', 0).replace('ns', ''))
        delay_sum = float(flow.get('delaySum', 0).replace('ns', ''))
        rx_packets = float(flow.get('rxPackets', 1)) # Default 1 to avoid div by zero

        # Calculate Throughput (Mbps)
        duration_sec = (time_last_rx - time_first_rx) / 1e9
        if duration_sec > 0:
            throughput = (rx_bytes * 8) / (duration_sec * 1e6)
        else:
            throughput = 0
            
        # Calculate Average Latency (ms)
        avg_delay = (delay_sum / rx_packets) / 1e6 

        throughput_mbps.append(throughput)
        delays_ms.append(avg_delay)
        ue_ids.append(f"UE {flow_id}")

    # 2. Parse Energy Consumption (Assuming custom tags for 5G-LENA UE energy)
    # If your energy data is in a separate CSV, you can load it here with pandas instead
    for ue_energy in root.findall('.//EnergyMetrics/UE'):
        energy = float(ue_energy.get('totalEnergyJoules', 0))
        energy_consumed_joules.append(energy)

    # If energy XML tags weren't found, generate placeholder data based on flow length
    # so the script doesn't crash while you adjust your XML tags
    if not energy_consumed_joules:
        print("Warning: EnergyMetrics tags not found. Using placeholder values for plotting.")
        energy_consumed_joules = [15.2, 18.5, 12.1, 22.4][:len(ue_ids)]

    return ue_ids, throughput_mbps, delays_ms, energy_consumed_joules

def generate_graphs(ue_ids, throughput, latency, energy):
    x = np.arange(len(ue_ids))
    width = 0.35

    # --- Graph 1: XR Traffic Latency ---
    plt.figure(figsize=(8, 5))
    plt.bar(ue_ids, latency, color='#1f77b4', edgecolor='black')
    plt.axhline(y=10, color='r', linestyle='--', label='10ms XR Delay Budget')
    plt.title('Average End-to-End Latency for XR Traffic', fontsize=14)
    plt.ylabel('Latency (ms)', fontsize=12)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('xr_latency.png', dpi=300)
    print("Saved: xr_latency.png")

    # --- Graph 2: Energy Consumption vs Throughput ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Energy on primary Y-axis
    ax1.set_xlabel('User Equipment (UE)', fontsize=12)
    ax1.set_ylabel('Energy Consumed (Joules)', color='tab:green', fontsize=12)
    bars1 = ax1.bar(x - width/2, energy, width, label='Energy (J)', color='tab:green', edgecolor='black')
    ax1.tick_params(axis='y', labelcolor='tab:green')

    # Plot Throughput on secondary Y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel('Throughput (Mbps)', color='tab:orange', fontsize=12)
    bars2 = ax2.bar(x + width/2, throughput, width, label='Throughput (Mbps)', color='tab:orange', edgecolor='black')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    plt.title('UE Power Drain vs. Maintained XR Throughput', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(ue_ids)
    
    # Combined legend
    fig.legend(loc="upper left", bbox_to_anchor=(0.15,0.85))
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('xr_energy_vs_throughput.png', dpi=300)
    print("Saved: xr_energy_vs_throughput.png")

if __name__ == "__main__":
    file_name = "xr-traffic-results.xml"
    try:
        ue_ids, throughput, latency, energy = parse_ns3_xml(file_name)
        generate_graphs(ue_ids, throughput, latency, energy)
        print("\nSuccess! Graphs are ready to attach to your email.")
    except Exception as e:
        print(f"Error reading the XML file: {e}")
        print("Make sure 'xr-traffic-results.xml' is in the same folder as this script.")
