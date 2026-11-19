
import glob
import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

files = sorted(glob.glob("Quantumdata/TobQD585_2024-06-04_c*.hdf5"))

det_a = 4
det_b = 5

tau_max_ns = 100.0
bin_ns = 1.0

edges = np.arange(-tau_max_ns, tau_max_ns + bin_ns, bin_ns)

fig, axes = plt.subplots(5, 1, figsize=(12, 14), sharex=True)

for ax, filename in zip(axes, files):

    with h5py.File(filename, "r") as f:

        timestamps = f["photon_data/timestamps"][:]
        detectors = f["photon_data/detectors"][:]

        specs = f["photon_data/timestamps_specs"]
        if "timestamps_unit" in specs.attrs:
            unit_s = float(specs.attrs["timestamps_unit"])
        else:
            unit_s = float(specs["timestamps_unit"][()])

        a = timestamps[detectors == det_a]
        b = timestamps[detectors == det_b]

    # Convert timestamps from ticks to nanoseconds
    a_ns = a * unit_s * 1e9
    b_ns = b * unit_s * 1e9

    differences = []

    # Find detector B events within the selected time window
    for t in a_ns:
        left = np.searchsorted(b_ns, t - tau_max_ns)
        right = np.searchsorted(b_ns, t + tau_max_ns)

        differences.extend(b_ns[left:right] - t)

    counts, _ = np.histogram(differences, bins=edges)

    centres = edges[:-1]

    ax.plot(centres, counts, marker=".", linewidth=1)
    ax.set_title(os.path.basename(filename))
    ax.set_ylabel("Counts")
    ax.grid(True)

axes[-1].set_xlabel("Time difference (ns)")

plt.tight_layout()
plt.savefig("individual_cycle_comparison.png", dpi=200)
plt.show()
