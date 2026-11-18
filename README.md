# Quantum Information Research

**An experimental investigation of informational structure in quantum measurement outcomes.**

## Overview

This project investigates the structure of quantum measurement data through computational experiments, statistical analysis and comparisons across different quantum circuit preparations.

The initial work focuses on standard quantum circuits, including single-qubit superposition, Bell states and GHZ states. These provide established reference cases with well-understood theoretical predictions. From there, the research will extend towards phase-dependent circuits, more complex gate sequences and systems with increasing numbers of entangled qubits.

The central interest is not limited to whether measured frequencies agree with predicted probabilities. It is also to investigate the relationships and informational properties present in the resulting measurement records.

A particular emphasis is placed on properties that can be studied without assuming that individual records are arranged in their original physical chronological order.

This is an exploratory research project. It does not begin with the assumption that standard quantum mechanics is incomplete, nor that any particular underlying physical mechanism has been identified.

## Research Questions

The project is organised around several broad questions:

- What reproducible informational properties can be identified in quantum measurement datasets?
- How do these properties depend on quantum state preparation, gate operations and measurement basis?
- How does the structure of measurement outcomes change when entanglement is introduced?
- Which properties remain consistent as the number of participating qubits increases?
- Are there mathematical relationships shared by datasets generated from different quantum circuits?
- Can higher-order correlations reveal structure that is not apparent from individual outcome frequencies?
- Do experimental datasets exhibit properties beyond those expected from standard quantum predictions and realistic hardware models?

These questions will be approached incrementally, beginning with established experimental configurations.

## Foundational Experimental Work

The initial dataset collection is based on a small catalogue of standard quantum circuits.

| Experiment | Description | Primary interest |
|---|---|---|
| Single-qubit Hadamard | Superposition followed by Z-basis measurement | Baseline outcome distribution |
| Bell state | Two-qubit entangled state | Joint measurement correlations |
| GHZ state | Three-qubit entangled state | Multipartite correlations |
| RX rotations | Single-qubit rotations around the X axis | State-dependent probabilities |
| Phase rotations | Relative phase manipulation | Phase-dependent measurement behaviour |
| Combined rotations | Multiple single-qubit operations | More complex state preparation |

Each experiment will have a defined circuit, expected quantum-mechanical predictions, raw measurement records and execution metadata.

The same circuit preparations will eventually be repeated across available quantum simulators and physical quantum processors, allowing comparisons between idealised predictions, simulated behaviour and hardware observations.

## Extended Research: Exponential Variable-Dimensional GHZ Analysis

An additional research direction will investigate GHZ states as the number of participating qubits increases.

An N-qubit system has a computational basis containing \(2^N\) possible bitstrings. An ideal GHZ state is:

\[
|\mathrm{GHZ}_N\rangle =
\frac{|0\rangle^{\otimes N}+|1\rangle^{\otimes N}}{\sqrt{2}}
\]

When measured in the computational (Z) basis, only two outcomes are possible in the ideal case:

\[
P(00\ldots0)=P(11\ldots1)=\frac{1}{2}
\]

This provides a controlled setting in which the dimensionality of the measurement space increases exponentially while the ideal outcome distribution remains highly constrained.

The proposed investigation will consider:

- Increasing the number of entangled qubits.
- Changes in joint and marginal entropy.
- Pairwise and higher-order correlations.
- Measurement in different bases.
- Differences between entangled and independently prepared qubits.
- The stability of observed properties across system sizes and hardware platforms.

The aim is to understand how informational structure behaves as the dimensionality and correlation structure of the quantum system change.

This programme will be developed subject to available hardware capabilities and circuit execution limits.

## Analytical Framework

A defining methodological constraint of this research is that the ordering of individual measurement records must initially be treated as arbitrary unless independent evidence establishes otherwise.

The order in which results are returned by a provider, stored in a file or presented by an API does not necessarily establish the physical chronological order of the underlying measurement events.

For this reason, the initial analysis will prioritise permutation-invariant methods.

A permutation-invariant analysis produces the same result regardless of how the individual records are rearranged.

Primary analytical areas include:

- Outcome frequencies and joint probability distributions.
- Shannon and joint entropy.
- Marginal and conditional entropy.
- Mutual information.
- Pairwise and higher-order correlations.
- Pattern occurrence and distribution.
- Statistical comparison between independent datasets.
- Cross-circuit and cross-hardware comparisons.

Order-dependent methods, such as autocorrelation, transition analysis, sequential pattern detection and run-length analysis, may also be investigated. However, their physical interpretation will remain conditional on the availability of trustworthy ordering information.

The distinction between acquisition order and physical chronology will be maintained throughout the project.

## Statistical Controls and Validation

Binary measurement records are a simple representation, and patterns will naturally occur as dataset size increases.

The presence of a pattern is therefore not sufficient evidence of an underlying relationship or physical significance.

Candidate findings must be evaluated against appropriate reference models.

These will include:

- Ideal quantum circuit simulations.
- Independent random-bit models where appropriate.
- Quantum probability distributions for the relevant circuit and measurement basis.
- Realistic noise models where available.
- Permuted and shuffled datasets.
- Repeated independent experimental runs.

Statistical significance, uncertainty, finite sample effects and multiple comparisons must be considered when evaluating candidate patterns.

Particular care will be taken to distinguish expected quantum correlations from additional structures that might warrant further investigation.

## Current Experimental Environment

The initial experiments use Python, Qiskit and the Quantum Inspire provider.

The QX emulator is being used to establish the experimental and data-processing workflow. Physical quantum processors will be incorporated as they become available.

The current environment is:

- Python 3.13
- Qiskit
- Qiskit Quantum Inspire
- Quantum Inspire QX emulator

The project is designed to remain accessible through a standard personal computer and remote quantum computing services. Dedicated laboratory equipment is not currently part of the experimental setup.

## Research Position

The project is motivated by an interest in whether quantum measurement outcomes contain reproducible informational properties that can be studied across different physical preparations and experimental configurations.

One longer-term motivation is to investigate whether different quantum phenomena share deeper mathematical or informational structures.

At present, no such common underlying mechanism has been established. Any proposed explanation must remain distinguishable from the predictions of standard quantum mechanics, statistical effects and experimental imperfections.

The research will therefore maintain a separation between experimental observations, established theoretical predictions and speculative interpretation.

The intention is to let the data and the reproducibility of the results determine which questions deserve further investigation.

## Project Status

**Current stage:** Initial experimental framework and dataset development.

The first reference experiments are being established using the Quantum Inspire QX emulator. The next major stage is to repeat these experiments on physical quantum processors, followed by the development of a broader analytical framework.

This is a long-term project. Experimental coverage, analytical methods and theoretical questions will develop progressively as new data becomes available.

---

*Research Philosophy: See [ResearchPhilosophy.md](ResearchPhilosophy.md) for the project's underlying methodological principles.*