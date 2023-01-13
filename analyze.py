import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensors.npy")
frontLegSensorValues = np.load("data/frontLegSensors.npy")
targets = np.load("data/sineWave.npy")
targets2 = np.load("data/sineWave2.npy")

#print(backLegSensorValues)

#plt.plot(backLegSensorValues, linewidth=2)
#plt.plot(frontLegSensorValues)
plt.plot(targets)
plt.plot(targets2)
#plt.legend(["Back Leg", "Front Leg", "Sine Wave"])
plt.show()