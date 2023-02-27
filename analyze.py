import numpy as np
import matplotlib.pyplot as plt

fitnesses = np.load("FitnessProgression.npy")

plt.plot(fitnesses)
plt.show()