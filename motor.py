import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.values = np.zeros(c.loops)

        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        self.amp = c.frontAmp
        self.frq = c.frontFrq
        self.pO = c.frontPO
        
        if(self.jointName == b'Torso_BackLeg'):
            self.frq /= 2

        self.values = self.amp * np.sin(self.frq * np.linspace(0, 2*np.pi, c.loops) + self.pO)

    def Set_Value(self, desiredAngle, robotId):
         pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = 100)

    def Save_Values(self):
        np.save("data\\"+self.jointName, self.values)