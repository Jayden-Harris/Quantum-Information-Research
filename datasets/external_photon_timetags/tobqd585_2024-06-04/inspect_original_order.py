
import glob
import h5py
import numpy as np
import os

files = sorted(
    glob.glob("Quantumdata/TobQD585_2024-06-04_c*.hdf5")
)

for filename in files:

    with h5py.File(filename, "r") as f:

        timestamps = f["photon_data/timestamps"][:]
        detectors = f["photon_data/detectors"][:]

    # Check the original timestamp order BEFORE sorting
    differences = np.diff(timestamps)

    chronological = np.all(differences >= 0)
    backwards_steps = np.sum(differences < 0)
    equal_adjacent = np.sum(differences == 0)

    print("\n", os.path.basename(filename))
    print("Total recorded events:", len(timestamps))
    print("Original timestamps chronological:", chronological)
    print("Backwards timestamp steps:", backwards_steps)
    print("Adjacent equal timestamps:", equal_adjacent)

    print("Detector counts:")

    for detector in [4, 5, 8, 9]:
        print(
            f"  Detector {detector}:",
            np.sum(detectors == detector)
        )
