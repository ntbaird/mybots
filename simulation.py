import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from world import WORLD
from robot import ROBOT
import constants as c
import time
import numpy as np

class SIMULATION:
    def __init__(self, directOrGUI):
        if(directOrGUI == "DIRECT"):
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-13.8)

        self.world = WORLD()
        self.robot = ROBOT()
    
    def Run(self, direct):
        backLegSensorValues = np.zeros(c.loops)
        frontLegSensorValues = np.zeros(c.loops)
        d = False
        if(direct == "DIRECT"):
            d = True

        targetValues = c.frontAmp * np.sin(c.frontFrq * np.linspace(0, 2*np.pi, c.loops) + c.frontPO)
        targetValues2 = c.backAmp * np.sin(c.backFrq * np.linspace(0, 2*np.pi, c.loops) + c.backPO)

        for i in range(c.loops):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

            if not d:
                time.sleep(1/80)
            #print(i)
        self.robot.Save_Values()

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()