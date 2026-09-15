#!/bin/bash

echo "=================================================="
echo "INITIATING PHASE 2: MAX DENSITY SATURATION SWEEP"
echo "=================================================="

# Create directories for outputs if they don't exist
mkdir -p simulation_results
mkdir -p power_logs

# Define the escalated parameter arrays to force PRB saturation
UES=(20 40 60 80 100)
TIMERS=(2 10 20 50)
CYCLES=(10 20 40 80)

# Calculate total runs for the progress tracker
TOTAL_RUNS=$((${#UES[@]} * ${#TIMERS[@]} * ${#CYCLES[@]}))
CURRENT_RUN=1

for ue in "${UES[@]}"; do
  for timer in "${TIMERS[@]}"; do
    for cycle in "${CYCLES[@]}"; do
      
      echo ">>> Executing Run $CURRENT_RUN of $TOTAL_RUNS | UEs: $ue | Timer: $timer ms | Cycle: $cycle ms"
      
      # Execute the ns-3 simulation
      ./ns3 run "xr-thesis --nUes=$ue --inactivityTimer=$timer --cycleLength=$cycle"
      
      # Safely move and rename the generated CSV to prevent overwriting
      if [ -f "parsed_power_data.csv" ]; then
        mv parsed_power_data.csv "power_logs/power_ues${ue}_timer${timer}_cycle${cycle}.csv"
      fi

      ((CURRENT_RUN++))
    done
  done
done

echo "=================================================="
echo "PHASE 2 SWEEP COMPLETE. DATA STORED IN /power_logs"
echo "=================================================="