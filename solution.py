import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os

class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1

    def Evaluate(self, dOG):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python simulate.py " + dOG)

        f = open("data/fitness.txt", "r")
        self.fitness = float(f.read())
        f.close()

    def Mutate(self):
        row = random.randint(0, 2)
        col = random.randint(0, 1)

        self.weights[row, col] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(name="Box", pos=[1, 1, .5] , size=[1, 1, 1]) 

        pyrosim.End()
    
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5] , size=[1, 1, 1])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [.5,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5] , size=[1, 1, 1])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-.5,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5] , size=[1, 1, 1])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        sensorNeurons = [0, 1, 2]
        motorNeurons = [0, 1]

        for row in sensorNeurons:
            for column in motorNeurons:
                pyrosim.Send_Synapse( sourceNeuronName = row, targetNeuronName = column+3, weight = self.weights[row, column])

        """
        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = .8 )
        pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = 1.2 )

        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = .2 )
        pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 1.0 )
        """

        pyrosim.End()