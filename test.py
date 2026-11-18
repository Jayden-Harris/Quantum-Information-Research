
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone
import json

from qiskit import QuantumCircuit
from qiskit_quantuminspire.qi_provider import QIProvider


# Connect to Quantum Inspire
provider = QIProvider()
simulator_backend = provider.get_backend("QX emulator")


# Experiment settings
experiment_id = "ghz_qx_emulator"
shots_requested = 2000


# Create three-qubit GHZ circuit
qc = QuantumCircuit(3, 3)

qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)

qc.measure([0, 1, 2], [0, 1, 2])

print(qc)


# Submit experiment
job = simulator_backend.run(
    qc,
    shots=shots_requested,
    memory=True
)


# Retrieve individual measurement results
result = job.result()
all_shots = result.get_memory()


# Create experiment dataset folder
dataset_dir = (
    Path("datasets")
    / "ghz_states"
    / "ghz_qx_emulator"
)

dataset_dir.mkdir(parents=True, exist_ok=True)


# Combine individual results into a continuous binary string
binary_string = "".join(all_shots)


# 1. Save continuous binary string
with open(dataset_dir / "binary_string.txt", "w") as file:
    file.write(binary_string)


# 2. Save individual measurement records
with open(dataset_dir / "measurement_records.json", "w") as file:
    json.dump(all_shots, file, indent=2)


# Calculate measurement counts
counts = Counter(all_shots)


# 3. Save experiment metadata
metadata = {
    "experiment_id": experiment_id,
    "experiment_type": "Three-qubit GHZ state",
    "backend": "QX emulator",
    "shots_requested": shots_requested,
    "shots_returned": len(all_shots),
    "qubits": 3,
    "classical_bits": 3,
    "initial_state": "|000>",
    "prepared_state": "(|000> + |111>) / sqrt(2)",
    "circuit": [
        "H(0)",
        "CX(0,1)",
        "CX(0,2)",
        "Measure(0,0)",
        "Measure(1,1)",
        "Measure(2,2)"
    ],
    "measurement_basis": "ZZZ",
    "expected_probabilities": {
        "000": 0.5,
        "111": 0.5
    },
    "measurement_counts": dict(counts),
    "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
    "binary_string_length": len(binary_string)
}

with open(dataset_dir / "experiment_metadata.json", "w") as file:
    json.dump(metadata, file, indent=2)


# Display results
print("\nMeasurement counts:")
print(dict(counts))

print("\nTotal measurements:", len(all_shots))

print("\nFirst 30 measurements:")
print(all_shots[:30])

print("\nBinary string length:", len(binary_string))
print("\nFirst 100 bits:", binary_string[:100])

print("\nDataset saved to:", dataset_dir)

