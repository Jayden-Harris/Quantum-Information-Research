
import glob
import h5py
import numpy as np

FILES = sorted(
    glob.glob("Quantumdata/TobQD585_2024-06-04_c*.hdf5")
)

HISTORY_LENGTHS = range(5)
NUMBER_OF_SHUFFLES = 5

rng = np.random.default_rng(2026)


def entropy_from_counts(counts):
    """Shannon entropy in bits."""
    counts = counts[counts > 0]

    if len(counts) == 0:
        return 0.0

    probabilities = counts / counts.sum()

    return -np.sum(
        probabilities * np.log2(probabilities)
    )


def analyse_sequence(cycle_data, max_history=4):
    """
    Calculate H(next detector | previous k detectors).

    Equal-timestamp adjacent events are excluded from
    every window that contains them.
    """

    joint_counts = {
        k: np.zeros(4 ** (k + 1), dtype=np.int64)
        for k in range(max_history + 1)
    }

    history_counts = {
        k: np.zeros(4 ** k, dtype=np.int64)
        for k in range(1, max_history + 1)
    }

    for timestamps, detectors in cycle_data:

        # Map detector labels 4,5,8,9 to symbols 0,1,2,3
        symbols = np.searchsorted(
            [4, 5, 8, 9], detectors
        ).astype(np.int64)

        time_steps = np.diff(timestamps)
        n = len(symbols)

        for k in range(max_history + 1):

            m = n - k

            if m <= 0:
                continue

            # A valid window must have strictly increasing
            # timestamps throughout.
            valid = np.ones(m, dtype=bool)

            for offset in range(k):
                valid &= time_steps[offset:offset + m] > 0

            # Encode the previous k detector symbols
            if k == 0:
                target = symbols[:m]
                codes = target
            else:
                history = symbols[:m].copy()

                for offset in range(1, k):
                    history = (
                        history * 4 + symbols[offset:offset + m]
                    )

                target = symbols[k:k + m]

                codes = history * 4 + target

                history_counts[k] += np.bincount(
                    history[valid],
                    minlength=4 ** k
                )

            joint_counts[k] += np.bincount(
                codes[valid],
                minlength=4 ** (k + 1)
            )

    # Calculate conditional entropy
    results = {}

    baseline = entropy_from_counts(joint_counts[0])

    for k in HISTORY_LENGTHS:

        joint_entropy = entropy_from_counts(
            joint_counts[k]
        )

        if k == 0:
            conditional_entropy = joint_entropy
        else:
            history_entropy = entropy_from_counts(
                history_counts[k]
            )

            conditional_entropy = (
                joint_entropy - history_entropy
            )

        information = baseline - conditional_entropy

        results[k] = (
            conditional_entropy,
            information
        )

    return results


# Load the original timestamp and detector records
original_data = []

for filename in FILES:

    with h5py.File(filename, "r") as f:
        timestamps = f["photon_data/timestamps"][:]
        detectors = f["photon_data/detectors"][:]

    original_data.append((timestamps, detectors))

print("Analysing original chronological records...")

original_results = analyse_sequence(original_data)

print("\nORIGINAL DATA")
print("History | Conditional entropy | Information gained")

for k, (h, info) in original_results.items():
    print(f"{k:>7} | {h:>18.8f} | {info:>16.8f}")

# Generate shuffled comparison datasets
shuffle_results = {
    k: [] for k in HISTORY_LENGTHS
}

print("\nAnalysing shuffled comparison datasets...")

for iteration in range(NUMBER_OF_SHUFFLES):

    shuffled_data = []

    for timestamps, detectors in original_data:

        shuffled_detectors = rng.permutation(detectors)

        shuffled_data.append(
            (timestamps, shuffled_detectors)
        )

    result = analyse_sequence(shuffled_data)

    for k in HISTORY_LENGTHS:
        shuffle_results[k].append(result[k][1])

    print(f"Completed shuffle {iteration + 1}")

print("\nSHUFFLED COMPARISON")
print("History | Mean information | Standard deviation")

for k in HISTORY_LENGTHS:

    values = np.array(shuffle_results[k])

    print(
        f"{k:>7} | "
        f"{np.mean(values):>16.8f} | "
        f"{np.std(values):>19.8f}"
    )

print("\nAnalysis complete.")
