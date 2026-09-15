import xml.etree.ElementTree as ET

print("\n--- XR TRAFFIC MODEL RESULTS ---")
tree = ET.parse('xr-traffic-results.xml')
root = tree.getroot()

for flow in root.findall('.//FlowStats/Flow'):
    txPackets = float(flow.get('txPackets'))
    rxPackets = float(flow.get('rxPackets'))
    
    # Extract times and remove the 'ns' (nanoseconds) string, convert to floats
    delaySum_ns = float(flow.get('delaySum').replace('ns', '').replace('+', ''))
    jitterSum_ns = float(flow.get('jitterSum').replace('ns', '').replace('+', ''))
    
    if rxPackets > 1:
        avgDelay_ms = (delaySum_ns / rxPackets) / 1000000.0
        avgJitter_ms = (jitterSum_ns / (rxPackets - 1)) / 1000000.0
        
        print(f"Packets Sent:     {int(txPackets)}")
        print(f"Packets Received: {int(rxPackets)}")
        print(f"Average Delay:    {avgDelay_ms:.3f} ms")
        print(f"Average Jitter:   {avgJitter_ms:.3f} ms")
print("--------------------------------\n")