# XR 5G C-DRX Energy Thesis

NS-3 simulation code and analysis scripts for an MSc thesis investigating the energy efficiency of XR traffic over 5G Standalone networks using C-DRX.

## Overview

This repository contains the custom NS-3 simulation, experiment automation, result-processing, and plotting scripts used in the thesis.

The study evaluates:

- Energy consumption
- MAC-layer latency
- Network capacity

The simulations use a 5G Standalone NR setup at 3.5 GHz (FR1) and investigate different XR user densities, channel bandwidths, propagation distances, and C-DRX configurations.

## Experimental Setup

### Baseline configuration

- 5G Standalone
- 3.5 GHz FR1
- Stationary UEs
- Single-cell scenario
- XR traffic
- C-DRX energy analysis

### Network density

20, 40, 60, 80, and 100 UEs

### Channel bandwidth

50 MHz and 100 MHz

### Propagation distance

20 m, 100 m, and 300 m

### C-DRX configurations

The C-DRX sweep evaluates:

- Inactivity Timer: 2, 10, 20, and 50 ms
- Long Cycle: 10, 20, 40, and 80 ms

This results in 16 C-DRX configurations across five UE densities.

## Energy Monitoring

The simulation implements a custom application-layer energy monitoring approach using the received-packet state of the XR traffic sink.

The monitor polls the packet sink at 1 ms intervals and maps the observed state to active and idle device current values used by the NS-3 energy model.

The implementation is contained in:

`xr-thesis.cc`

## Repository Contents

| File | Description |
|---|---|
| `xr-thesis.cc` | Main NS-3 5G XR simulation and custom energy monitor |
| `run_cdrx_sweep.sh` | Automated C-DRX configuration sweep |
| `execute_full_matrix.py` | Automated scenario-dependent simulation matrix |
| `parse_results.py` | Result parsing |
| `parse_xr_results.py` | XR result processing |
| `generate_graphs.py` | Graph generation |
| `plot_cdrx.py` | C-DRX result plotting |
| `plot_heatmap.py` | Heatmap generation |
| `plot_latency.py` | Latency plotting |
| `plot_pareto.py` | Pareto-frontier plotting |
| `plot_results.py` | General result plotting |

## Reproduction

This repository contains the custom thesis code and scripts. The complete NS-3/5G-LENA framework is not included.

The files are intended to be used with an NS-3 installation containing the required 5G NR modules.

Place `xr-thesis.cc` in the appropriate NS-3 `scratch/` directory and place the accompanying Python and shell scripts in the NS-3 working directory.


### C-DRX sweep

From the NS-3 working directory:

chmod +x run_cdrx_sweep.sh
./run_cdrx_sweep.sh

The C-DRX sweep runs combinations of:

- 5 UE densities
- 4 inactivity timers
- 4 C-DRX cycle lengths
for a total of 80 simulation runs.



### Scenario-dependent matrix
From the NS-3 working directory:

python3 execute_full_matrix.py
The full matrix evaluates:
- 5 UE densities
- 2 bandwidth values
- 3 propagation distances
for a total of 30 simulation runs at 3.5 GHz.

## Outputs

Simulation and processing scripts generate result files used for the energy, latency, and capacity analysis presented in the thesis.
Generated data and figures are not included in this repository.

## Thesis

This repository accompanies the MSc thesis:

Energy Efficiency of XR Traffic over 5G Standalone Architecture — Dynamic Power Modeling using NS-3
- Department of Communication Systems
- KTH Royal Institute of Technology
## Author
Sudharshan Yellampalli Kidambi
