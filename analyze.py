import numpy as np
import matplotlib.pyplot as plt
import constants as c

fitness0 = np.load("FitnessProgression0.npy")
fitness1 = np.load("FitnessProgression1.npy")
fitness2 = np.load("FitnessProgression2.npy")
fitness3 = np.load("FitnessProgression3.npy")
fitness4 = np.load("FitnessProgression4.npy")
fitness5 = np.load("FitnessProgression5.npy")
fitness6 = np.load("FitnessProgression6.npy")
fitness7 = np.load("FitnessProgression7.npy")
fitness8 = np.load("FitnessProgression8.npy")
fitness9 = np.load("FitnessProgression9.npy")

plt.plot(fitness0, label='Seed 0')
plt.plot(fitness1, label='Seed 1')
plt.plot(fitness2, label='Seed 2')
plt.plot(fitness3, label='Seed 3')
plt.plot(fitness4, label='Seed 4')
plt.plot(fitness5, label='Seed 5')
plt.plot(fitness6, label='Seed 6')
plt.plot(fitness7, label='Seed 7')
plt.plot(fitness8, label='Seed 8')
plt.plot(fitness9, label='Seed 9')
plt.legend()
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.show()