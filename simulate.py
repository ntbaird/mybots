import time
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

totalTime = 1000
backLegSensorValues = np.zeros(totalTime)
frontLegSensorValues = np.zeros(totalTime)

amp = np.pi/2
frq = 20
phaseOffset = np.pi/4.0
targetValues = amp * np.sin(frq * np.linspace(0, 2*np.pi, totalTime) + phaseOffset)

amp2 = np.pi/2
frq2 = 20
phaseOffset2 = 0
targetValues2 = amp2 * np.sin(frq2 * np.linspace(0, 2*np.pi, totalTime) + phaseOffset2)

for i in range(totalTime):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b"Torso_BackLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = targetValues[i],
    maxForce = 100)

    pyrosim.Set_Motor_For_Joint(
    bodyIndex = robotId,
    jointName = b"Torso_FrontLeg",
    controlMode = p.POSITION_CONTROL,
    targetPosition = targetValues2[i],
    maxForce = 100)

    time.sleep(1/60)
    #print(i)

np.save("data\\backLegSensors", backLegSensorValues)
np.save("data\\frontLegSensors", frontLegSensorValues)
np.save("data\\sineWave", targetValues)
np.save("data\\sineWave2", targetValues2)

p.disconnect()
