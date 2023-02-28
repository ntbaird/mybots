import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:
    def __init__(self, id, seed):
        self.id = id
        self.robotId = p.loadURDF("bodies\\"+str(seed)+"seedbody"+str(self.id)+".urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK("brains/"+str(seed)+"seedbrain"+str(self.id)+".nndf")
        

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for s in self.sensors.values():
            s.Get_Value(t)

    # Can be deleted?
    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            #print(jointName)
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)*c.motorJointRange
                if(jointName in self.motors):
                    self.motors[jointName].Set_Value(desiredAngle, self.robotId)
                

    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    # Can be deleted?
    def Save_Values(self):
        for s in self.sensors.values():
            s.Save_Values()
        for m in self.sensors.values():
            m.Save_Values()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordOfLinkZero = positionOfLinkZero[0]
        yCoordOfLinkZero = positionOfLinkZero[1]
        zCoordOfLinkZero = positionOfLinkZero[2]

        sumCoords = xCoordOfLinkZero+yCoordOfLinkZero

        f = open("tmp"+str(self.id)+".txt", "w")
        f.write(str(sumCoords))
        f.close()
        os.rename("tmp"+str(self.id)+".txt" , "fitness"+str(self.id)+".txt")

    
