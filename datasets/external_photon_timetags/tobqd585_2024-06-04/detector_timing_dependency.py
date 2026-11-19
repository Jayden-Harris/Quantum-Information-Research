
import numpy as np
import pandas as pd
from pathlib import Path


N_SHUFFLES = 5
RNG = np.random.default_rng(42)

# Collect inter-event intervals and whether adjacent events
# were recorded by the same detector.
all_dt = []
all_same = []
cycle_data = []

SCRIPT_DIR = Path(__file__).resolve().parent
EVENTS_DIR = SCRIPT_DIR / "chronological_events"

csv_files = sorted(EVENTS_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "No chronological_events CSV files found. "
        "Check the dataset folder."
    )

for path in csv_files:
    df = pd.read_csv(path)

    timestamps = df["timestamp_ns"].to_numpy(dtype=np.float64)
    detectors = df["detector"].to_numpy(dtype=np.int64)

    dt = np.diff(timestamps)
    valid = dt > 0

    dt = dt[valid]
    same = (detectors[:-1][valid] == detectors[1:][valid])

    all_dt.append(dt)
    all_same.append(same)
    cycle_data.append((dt, detectors, valid, same))

    print(f"{path.name}: {len(dt):,} valid intervals")

dt = np.concatenate(all_dt)
same = np.concatenate(all_same)

# Use quantile-based time bins so each bin has a useful
# number of observations. Duplicate boundaries are removed.
edges = np.unique(np.quantile(dt, np.linspace(0, 1, 21)))

if len(edges) < 3:
    raise ValueError("Not enough distinct time intervals for binning.")

# Include the largest interval in the final bin.
bin_index = np.digitize(dt, edges[1:-1])

n_bins = len(edges) - 1
counts = np.bincount(bin_index, minlength=n_bins)
same_counts = np.bincount(
    bin_index[same], minlength=n_bins
)

observed_rate = same_counts / counts

# Shuffle detector labels within each cycle, preserving
# each cycle's detector counts and its original timestamps.
shuffle_rates = np.zeros((N_SHUFFLES, n_bins))

for s in range(N_SHUFFLES):
    shuffled_same_all = []

    for dt_cycle, detectors, valid, _ in cycle_data:
        shuffled = RNG.permutation(detectors)
        shuffled_same = (
            shuffled[:-1][valid] == shuffled[1:][valid]
        )
        shuffled_same_all.append(shuffled_same)

    shuffled_same = np.concatenate(shuffled_same_all)

    shuffle_rates[s] = (
        np.bincount(
            bin_index[shuffled_same], minlength=n_bins
        ) / counts
    )

shuffle_mean = shuffle_rates.mean(axis=0)
shuffle_sd = shuffle_rates.std(axis=0, ddof=1)

# Report geometric bin centres, rates and shuffled comparison.
rows = []

for i in range(n_bins):
    if counts[i] == 0:
        continue

    rows.append({
        "interval_start_ns": edges[i],
        "interval_end_ns": edges[i + 1],
        "geometric_centre_ns": np.sqrt(edges[i] * edges[i + 1]),
        "events": counts[i],
        "observed_same_detector": observed_rate[i],
        "shuffled_mean": shuffle_mean[i],
        "shuffled_sd": shuffle_sd[i],
        "excess": observed_rate[i] - shuffle_mean[i],
    })

result = pd.DataFrame(rows)
result.to_csv("detector_timing_dependence.csv", index=False)

print("\nSame-detector probability by inter-event interval")
print(result.to_string(index=False, float_format=lambda x: f"{x:.6f}"))

print("\nSaved: detector_timing_dependence.csv")
