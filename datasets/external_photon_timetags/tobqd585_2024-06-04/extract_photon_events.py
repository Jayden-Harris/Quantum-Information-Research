
import glob
import h5py
import numpy as np
import pandas as pd
import os

files = sorted(
    glob.glob("Quantumdata/TobQD585_2024-06-04_c*.hdf5")
)

output_folder = "chronological_events"
os.makedirs(output_folder, exist_ok=True)

for filename in files:

    with h5py.File(filename, "r") as f:

        timestamps = f["photon_data/timestamps"][:]
        detectors = f["photon_data/detectors"][:]

        specs = f["photon_data/timestamps_specs"]

        if "timestamps_unit" in specs.attrs:
            unit_s = float(specs.attrs["timestamps_unit"])
        else:
            unit_s = float(specs["timestamps_unit"][()])

    # Keep the four detector channels
    valid = np.isin(detectors, [4, 5, 8, 9])

    timestamps = timestamps[valid]
    detectors = detectors[valid]

    # Sort by timestamp, preserving original order for ties
    order = np.argsort(timestamps, kind="stable")

    timestamps = timestamps[order]
    detectors = detectors[order]

    # Convert ticks to nanoseconds
    time_ns = timestamps * unit_s * 1e9

    # Create chronological event index
    event_index = np.arange(len(timestamps))

    data = pd.DataFrame({
        "event_index": event_index,
        "timestamp_ticks": timestamps,
        "timestamp_ns": time_ns,
        "detector": detectors
    })

    output_name = os.path.basename(filename).replace(
        ".hdf5", ".csv"
    )

    output_path = os.path.join(output_folder, output_name)

    data.to_csv(output_path, index=False)

    print(f"\n{output_name}")
    print("Events:", len(data))
    print("First timestamp (ns):", time_ns[0])
    print("Last timestamp (ns):", time_ns[-1])
    print("Chronological:", np.all(np.diff(timestamps) >= 0))

print("\nExtraction complete.")
