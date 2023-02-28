import numpy as np
import matplotlib.pyplot as plt
import constants as c

fitness0 = np.load("FitnessProgression0.npy")
fitness1 = np.load("FitnessProgression1.npy")
fitness3 = np.load("FitnessProgression3.npy")
fitness4 = np.load("FitnessProgression4.npy")
fitness7 = np.load("FitnessProgression7.npy")

plt.plot(fitness0, label='Seed 0')
plt.plot(fitness1, label='Seed 1')
plt.plot(fitness3, label='Seed 3')
plt.plot(fitness4, label='Seed 4')
plt.plot(fitness7, label='Seed 7')
plt.legend()
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.show()