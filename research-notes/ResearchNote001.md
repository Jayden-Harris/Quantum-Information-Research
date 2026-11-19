# Research Notebook — Note 001
## First look at real photon detection data

**Date:** 19 November 2026  
**Project:** Quantum Information Research  
**Status:** Early exploratory investigation

### 1. What am I trying to understand?

I'm interested in whether there are patterns or structures in the information produced when physical systems are measured.

In simple terms, when we measure something in nature, we get an outcome. I want to explore whether those outcomes are entirely random, or whether they contain relationships and patterns that might tell us something interesting about the physical processes behind them.

I don't have a fixed answer in mind. I'm starting by examining real experimental data and seeing what it tells me.

### 2. Where did the data come from?

For this first investigation, I chose publicly available data from a real laboratory experiment.

The researchers studied tiny light-emitting particles called quantum dots, introduced into tobacco plant leaves. They illuminated the sample with a pulsed laser and recorded individual photon detections using four detector channels.

A photon is a quantum of light. The equipment recorded when a photon was detected and which detector registered it.

I downloaded five measurement files, each approximately four minutes long.

Together, these files contain around **26.5 million photon detections**.

Some useful details:

- There are four detector channels: 4, 5, 8 and 9.
- Each detection has a timestamp.
- The timestamps have a resolution of approximately 164.61 picoseconds.
- The laser operates at 80 million pulses per second.
- This means the laser pulses are separated by approximately 12.5 nanoseconds.

This is real experimental data, not a computer simulation.

### 3. What have I investigated so far?

I've carried out four initial investigations.

#### Investigation A — Looking for patterns in photon arrival times

First, I looked at the time differences between photon detections recorded by two detector channels.

I plotted these differences on a graph.

The graph showed a repeating series of peaks, separated by approximately 12.5 nanoseconds.

**What does that mean?**

The detections appear to follow the repeating rhythm of the laser pulses.

This makes sense because the laser is deliberately pulsed at regular intervals. The result is consistent with the experimental setup.

It was a useful first step because it showed that the timestamps contain a recognisable pattern.

#### Investigation B — Looking at which detector records each photon

Next, I stopped looking only at the arrival times and examined the order in which the four detectors recorded photons.

Imagine a sequence like this:

`4, 8, 8, 5, 9, 9, 9, 4, 8, 5`

I wanted to know whether the same detector appeared consecutively more often than we might expect if the detector labels were randomly rearranged.

I compared the actual sequence with versions in which the detector labels had been shuffled, while keeping the number of detections from each detector the same.

The results were:

| Measurement | Same detector twice in a row |
|---|---:|
| Actual sequence | 29.58% |
| Shuffled comparison | 26.36% |

**What does that mean?**

In the actual recording, consecutive detections were more likely to come from the same detector than in our shuffled comparisons.

This suggests that the order of the detector records contains some structure.

It doesn't yet tell us why.

#### Investigation C — Using information theory

I then explored a mathematical way of measuring how much information one detection might give us about the next.

This is where we encountered the word *entropy*.

For now, think of entropy as a measure of uncertainty.

If I don't know which detector will record the next photon, I have some uncertainty. If I know which detector recorded the previous photon, perhaps that uncertainty becomes slightly smaller.

We tested how much knowing the previous one, two, three or four detector identities helped.

The results suggested:

- Knowing the immediately preceding detector reduces uncertainty slightly.
- Knowing two previous detectors adds very little extra information.
- Knowing three or four previous detectors adds even less.

**What does that mean?**

The detectable predictive structure seems to be mostly associated with the immediately preceding detection, rather than a long sequence of previous detections.

This is interesting because it gives us a way to describe the pattern mathematically, rather than just looking at a graph.

It is important to remember that these are estimates from the data, and more rigorous statistical testing will be needed before making strong claims.

#### Investigation D — Does the time between detections matter?

This was our latest investigation.

We already knew that consecutive detections were more likely to come from the same detector. But we hadn't asked whether this depended on how close together the detections occurred.

So we grouped consecutive detections according to the time separating them.

The result was quite striking:

| Approximate time between detections | Same-detector probability |
|---|---:|
| Under 1 microsecond | 70.20% |
| 1–3 microseconds | 37.79% |
| 3–6 microseconds | 30.43% |
| 6–8 microseconds | 28.32% |
| 8–11 microseconds | 27.52% |
| 11–15 microseconds | 27.01% |
| Longer intervals | Approaches 26.36% |

A microsecond is one millionth of a second. A nanosecond is one billionth of a second.

**What does this mean?**

The tendency for consecutive detections to come from the same detector is particularly strong when the detections happen close together.

As the time between detections increases, this tendency gradually disappears and approaches the shuffled comparison.

This is currently the most interesting observation from our initial work.

### 4. What have I actually learned?

At this early stage, I can say:

1. The photon detection records contain a repeating timing pattern associated with the laser.
2. The order of detector identities is not behaving like our randomly shuffled comparison.
3. The tendency for consecutive detections to come from the same detector is strongest at short time intervals.
4. Knowing the immediately preceding detector gives a small amount of information about the identity of the next detector.

These are observations from the dataset. They are not yet explanations of the physical processes producing them.

### 5. What don't I know yet?

This is just as important as what I have found.

I don't yet know why the detector sequence behaves this way.

Possible explanations include:

- The behaviour of the photon-emitting quantum dots.
- The response and recovery characteristics of the detectors.
- Electronic effects in the measurement equipment.
- The optical arrangement and how photons are distributed between detector channels.
- Interactions between several of these effects.

We need to investigate these possibilities before suggesting anything more unusual.

I also need to remember that the five files are consecutive sections of one measurement, not five separate experiments.

### 6. Why is this relevant to my wider research?

My wider interest is in the relationship between physical measurement and information.

I'm curious about whether the information we obtain from measurements might reveal deeper structures in the physical world.

This first investigation doesn't answer that question. It isn't supposed to.

What it has done is give me a starting point: real measurements, millions of recorded events, identifiable patterns, and some ways of measuring those patterns.

Before trying to understand anything more fundamental, I need to understand the behaviour of the data itself.

That is what this first stage is about.

### 7. Next steps

For now, I don't want to rush into more complicated analysis.

The next sensible questions are:

- Is the short-interval pattern shared by all four detectors, or is it concentrated in particular detectors?
- Could the detector equipment itself explain some or all of the effect?
- Does the laser's 12.5-nanosecond pulse cycle influence the detector sequence?
- Can we reproduce the findings using other sections of the dataset or independent experiments?

These questions will help us understand what we are actually observing before we attempt to interpret it.

---

**Current working conclusion**

The first examination of this photon dataset has revealed measurable patterns in both the timing and ordering of photon detections. In particular, consecutive detections are more likely to come from the same detector when they occur close together in time.

This is an interesting preliminary observation, but its physical cause remains unknown.

For now, the goal is to understand the observation, test alternative explanations and learn what the data can genuinely tell us.