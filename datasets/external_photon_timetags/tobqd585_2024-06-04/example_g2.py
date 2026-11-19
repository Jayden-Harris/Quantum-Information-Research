# Example: read photon arrival times from the Photon-HDF5 files and build a
# cross-correlation histogram g2(tau) between two detectors, summed over all cycles of a run.
# Requires only numpy and h5py (pip install numpy h5py). Usage (next to the Quantumdata/ folder): python example_g2.py TabQD585_c01  (or TobQD585_2024-06-04, TabQD585_run550)
import glob
import sys

import h5py
import numpy as np

run = sys.argv[1] if len(sys.argv) > 1 else "TabQD585_c01"   # measurement: TobQD585_2024-06-04, TabQD585_c01 or TabQD585_run550
det_a, det_b = 4, 5                       # detector channels: 4, 5, 8, 9
tau_max, bin_ns = 100.0, 1.0              # +-100 ns, 1 ns bins

edges = np.arange(-tau_max, tau_max + bin_ns, bin_ns)
g2 = np.zeros(edges.size - 1)
for fname in sorted(glob.glob(f"Quantumdata/{run}_c*.hdf5")):  # one file per acquisition cycle
    with h5py.File(fname, "r") as f:
        t = f["photon_data/timestamps"][:]                             # arrival times in ticks
        det = f["photon_data/detectors"][:]                            # detector channel per photon
        unit = f["photon_data/timestamps_specs/timestamps_unit"][()]   # 164.61e-12 s per tick
    a, b = t[det == det_a], t[det == det_b]
    w = int(tau_max * 1e-9 / unit)
    lo, hi = np.searchsorted(b, a - w), np.searchsorted(b, a + w)
    dt = np.concatenate([b[l:h] - x for x, l, h in zip(a, lo, hi)]) * unit * 1e9  # ns
    g2 += np.histogram(dt, bins=edges)[0]

for tau, n in zip(edges[:-1], g2):
    print(f"{tau:7.1f} ns  {int(n)}")
