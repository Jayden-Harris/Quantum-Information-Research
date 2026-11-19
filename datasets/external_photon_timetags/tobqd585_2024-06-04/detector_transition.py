
import glob
import h5py
import numpy as np
import pandas as pd

files = sorted(
    glob.glob("Quantumdata/TobQD585_2024-06-04_c*.hdf5")
)

detectors_list = [4, 5, 8, 9]
detector_index = {d: i for i, d in enumerate(detectors_list)}

# Rows = current detector; columns = next detector
transition_counts = np.zeros((4, 4), dtype=np.int64)

total_valid_transitions = 0
total_ambiguous_pairs = 0

for filename in files:

    with h5py.File(filename, "r") as f:
        timestamps = f["photon_data/timestamps"][:]
        detectors = f["photon_data/detectors"][:]

    # Confirm original records are chronologically ordered
    if np.any(np.diff(timestamps) < 0):
        raise ValueError(f"Unordered timestamps in {filename}")

    # Confirm the expected detector channels
    if not np.all(np.isin(detectors, detectors_list)):
        raise ValueError(f"Unexpected detector channel in {filename}")

    # Convert detector labels to matrix indices
    indices = np.array(
        [detector_index[d] for d in detectors],
        dtype=np.int8
    )

    # Only count pairs with strictly increasing timestamps
    time_differences = np.diff(timestamps)

    valid = time_differences > 0

    ambiguous = time_differences == 0

    # Count transitions
    np.add.at(
        transition_counts,
        (indices[:-1][valid], indices[1:][valid]),
        1
    )

    total_valid_transitions += np.sum(valid)
    total_ambiguous_pairs += np.sum(ambiguous)

    print(f"\nProcessed: {filename}")
    print("Valid transitions:", np.sum(valid))
    print("Equal-timestamp pairs excluded:", np.sum(ambiguous))

# Calculate row-normalised transition probabilities
row_totals = transition_counts.sum(axis=1)

transition_probabilities = np.divide(
    transition_counts,
    row_totals[:, None],
    out=np.zeros((4, 4), dtype=float),
    where=row_totals[:, None] != 0
)

labels = [str(d) for d in detectors_list]

counts_df = pd.DataFrame(
    transition_counts,
    index=labels,
    columns=labels
)

probabilities_df = pd.DataFrame(
    transition_probabilities,
    index=labels,
    columns=labels
)

counts_df.index.name = "Current detector"
probabilities_df.index.name = "Current detector"

print("\nTOTAL TRANSITION COUNTS")
print(counts_df)

print("\nROW-NORMALISED TRANSITION PROBABILITIES")
print(probabilities_df.round(6))

print("\nTotal valid transitions:", total_valid_transitions)
print("Total equal-timestamp pairs excluded:", total_ambiguous_pairs)

counts_df.to_csv("transition_counts.csv")
probabilities_df.to_csv("transition_probabilities.csv")

print("\nSaved transition_counts.csv")
print("Saved transition_probabilities.csv")
