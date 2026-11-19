
import glob
import h5py
import numpy as np

files = sorted(
    glob.glob("Quantumdata/TobQD585_2024-06-04_c*.hdf5")
)

rng = np.random.default_rng(42)

observed_same = 0
total_transitions = 0
cycle_data = []

# Load the original detector sequences
for filename in files:

    with h5py.File(filename, "r") as f:
        timestamps = f["photon_data/timestamps"][:]
        detectors = f["photon_data/detectors"][:]

    # Exclude adjacent events with equal timestamps
    valid = np.diff(timestamps) > 0

    same = (
        (detectors[:-1] == detectors[1:]) & valid
    )

    observed_same += np.sum(same)
    total_transitions += np.sum(valid)

    cycle_data.append((detectors, valid))

print("Observed same-detector transitions:", observed_same)
print("Total valid transitions:", total_transitions)

observed_rate = observed_same / total_transitions

print("Observed same-detector rate:", observed_rate)

# Generate shuffled comparison datasets
shuffle_results = []

number_of_shuffles = 20

for iteration in range(number_of_shuffles):

    shuffled_same = 0

    for detectors, valid in cycle_data:

        shuffled = rng.permutation(detectors)

        same = (
            (shuffled[:-1] == shuffled[1:]) & valid
        )

        shuffled_same += np.sum(same)

    shuffled_rate = shuffled_same / total_transitions
    shuffle_results.append(shuffled_rate)

    print(
        f"Shuffle {iteration + 1}: "
        f"{shuffled_rate:.6f}"
    )

shuffle_results = np.array(shuffle_results)

print("\nRESULTS")
print("Observed rate:", observed_rate)
print("Mean shuffled rate:", np.mean(shuffle_results))
print("Minimum shuffled rate:", np.min(shuffle_results))
print("Maximum shuffled rate:", np.max(shuffle_results))
print(
    "Observed excess:",
    observed_rate - np.mean(shuffle_results)
)
