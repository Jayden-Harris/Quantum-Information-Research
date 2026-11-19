import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("g2_detector_4_5.txt", usecols=(0, 2))

time_ns = data[:, 0]
counts = data[:, 1]

plt.figure(figsize=(12, 5))
plt.plot(time_ns, counts, marker=".", linewidth=1)

plt.xlabel("Time difference (ns)")
plt.ylabel("Coincidence counts")
plt.title("Detector 4–5 photon coincidence histogram")
plt.grid(True)

plt.tight_layout()
plt.savefig("g2_detector_4_5.png", dpi=200)
plt.show()