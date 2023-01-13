import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensors.npy")
frontLegSensorValues = np.load("data/frontLegSensors.npy")

#print(backLegSensorValues)

plt.plot(backLegSensorValues, linewidth=2)
plt.plot(frontLegSensorValues)
plt.legend(["Back Leg", "Front Leg"])
plt.show()