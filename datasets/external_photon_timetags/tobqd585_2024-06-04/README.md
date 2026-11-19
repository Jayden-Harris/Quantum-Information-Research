# Time-tagged photon data (Photon-HDF5) for "Utilizing quantum fingerprints in plant cells to evaluate plant productivity"

Ranasinghe, Stressinger, Xu, Sarhan, Harrington, Berry, Thomay, *Analyst* 2025, 150, 5394–5402, doi:10.1039/D5AN00326A

## Contents

Photon arrival times from CdSe/ZnS quantum dots (585 nm) delivered into *Nicotiana tabacum* leaves, recorded with a four-detector Hanbury Brown–Twiss setup (80 MHz pulsed excitation, avalanche photodiodes) and a Becker & Hickl DPC-230 time-to-digital converter. One file per acquisition cycle.

All files are in the folder `Quantumdata/`. The file name gives the measurement and the cycle number:

| File names | Files | Acquisition |
|---|---|---|
| `TobQD585_2024-06-04_c01.hdf5` … `TobQD585_2024-06-04_c05.hdf5` | 5 | one continuous measurement, 5 cycles × 240 s, 2024-06-04 |
| `TabQD585_c01_c01.hdf5` … `TabQD585_c01_c75.hdf5` | 75 | one continuous measurement, 75 cycles × 240 s, 2024-08-13 |
| `TabQD585_run550_c01.hdf5` … `TabQD585_run550_c36.hdf5` | 36 | one continuous measurement (originally recorded as `run550`), 36 cycles of ~300 s |

Total: 116 files, 134 358 735 photons.

The three measurements are also provided as separate archives (`TobQD585_2024-06-04.zip`, `TabQD585_c01.zip`, `TabQD585_run550.zip`); each contains this README, `example_g2.py` and the files of that measurement in `Quantumdata/`.

## File format

[Photon-HDF5](https://photon-hdf5.github.io/photon-hdf5/) v0.5 (open HDF5-based format for time-tagged photon data).

| Field | Meaning |
|---|---|
| `photon_data/timestamps` | arrival time of each photon since the start of the cycle, integer ticks |
| `photon_data/timestamps_specs/timestamps_unit` | tick length in seconds (164.61 ps) |
| `photon_data/detectors` | detector channel of each photon: 4, 5, 8 or 9 |
| `photon_data/nanotimes` | delay of each photon after the preceding laser reference tick, in ticks of 164.61 ps; the last bin (`user/dpc230/invalid_nanotime_marker`) marks the few photons without a valid reference (48 in total; their timestamps are exact) |
| `setup/laser_repetition_rates` | measured rate of the laser-derived reference clock |
| `user/dpc230` | acquisition and conversion details (original time unit, reference channel, reference period, number of reference ticks) |

Timestamps restart at zero in every cycle file.

## Reading the data

The files open with any HDF5 tool, e.g. Python `h5py` or the Photon-HDF5 library `phconvert`. Example: cross-correlation histogram g²(τ) of detectors 4 and 5, summed over all cycles of one measurement (needs only numpy and h5py; run next to the `Quantumdata/` folder as `python example_g2.py TobQD585_2024-06-04`, `python example_g2.py TabQD585_c01` or `python example_g2.py TabQD585_run550`):

```python
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
        t = f["photon_data/timestamps"][:]
        det = f["photon_data/detectors"][:]
        unit = f["photon_data/timestamps_specs/timestamps_unit"][()]
    a, b = t[det == det_a], t[det == det_b]
    w = int(tau_max * 1e-9 / unit)
    lo, hi = np.searchsorted(b, a - w), np.searchsorted(b, a + w)
    dt = np.concatenate([b[l:h] - x for x, l, h in zip(a, lo, hi)]) * unit * 1e9  # ns
    g2 += np.histogram(dt, bins=edges)[0]

for tau, n in zip(edges[:-1], g2):
    print(f"{tau:7.1f} ns  {int(n)}")
```

For `TobQD585_2024-06-04` and `TabQD585_c01` the histogram shows the 12.5 ns comb of the 80 MHz excitation laser; single cycles are too short for a visible signal. The same script is included as `example_g2.py`.

## Provenance

Recorded with Becker & Hickl SPCM in FIFO mode (`.spc` files); decoded and converted to Photon-HDF5 without changing any photon time. Per-detector photon counts of every file were checked against an independent count of the original `.spc` files.

## License

CC0 1.0
