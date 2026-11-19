
import glob
import h5py
import numpy as np

files = sorted(
    glob.glob("Quantumdata/TobQD585_2024-06-04_c*.hdf5")
)

det_a = 4
det_b = 5

tau_max_ns = 100.0
bin_ns = 1.0

edges = np.arange(
    -tau_max_ns,
    tau_max_ns + bin_ns,
    bin_ns
)

combined_counts = np.zeros(len(edges) - 1)

for filename in files:

    with h5py.File(filename, "r") as f:

        timestamps = f["photon_data/timestamps"][:]
        detectors = f["photon_data/detectors"][:]

        specs = f["photon_data/timestamps_specs"]

        if "timestamps_unit" in specs.attrs:
            unit_s = float(specs.attrs["timestamps_unit"])
        else:
            unit_s = float(specs["timestamps_unit"][()])

        a = timestamps[detectors == det_a] * unit_s * 1e9
        b = timestamps[detectors == det_b] * unit_s * 1e9

    differences = []

    for t in a:
        left = np.searchsorted(b, t - tau_max_ns)
        right = np.searchsorted(b, t + tau_max_ns)

        differences.extend(b[left:right] - t)

    counts, _ = np.histogram(differences, bins=edges)

    combined_counts += counts

# Remove the average count level
signal = combined_counts - np.mean(combined_counts)

# Fourier transform
spectrum = np.abs(np.fft.rfft(signal))
frequencies = np.fft.rfftfreq(len(signal), d=bin_ns)

# Search for a periodicity between 5 and 25 ns
valid = (frequencies >= 1/25) & (frequencies <= 1/5)

best_index = np.where(valid)[0][np.argmax(spectrum[valid])]

frequency = frequencies[best_index]
period = 1 / frequency

print("Dominant frequency:", frequency, "cycles/ns")
print("Estimated period:", period, "ns")
print("Expected laser period: 12.5 ns")
