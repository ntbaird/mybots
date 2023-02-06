import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.id = id
        
    def Set_ID(self, num):
        self.id = num

    def Evaluate(self, dOG):
        self.Start_Simulation(dOG)
        self.Wait_For_Simulation_To_End()

    def End_Simulations(self):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python simulate.py GUI " + str(self.id))

    def Start_Simulation(self, dOG):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("start /B python simulate.py " + dOG + " " + str(self.id))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("data/fitness"+str(self.id)+".txt"):
            time.sleep(.01)
        f = open("data/fitness"+str(self.id)+".txt", "r")
        self.fitness = float(f.read())
        
        f.close()
        os.remove("data/fitness"+str(self.id)+".txt")

    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons-1)
        col = random.randint(0, c.numMotorNeurons-1)

        self.weights[row, col] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        #pyrosim.Send_Cube(name="Box", pos=[3, 3, .5] , size=[1, 1, 1]) 
        pyrosim.Send_Cube(name="Box", pos=[0, 2.5, .2] , size=[15, 2, .3], mass=100.0) 
        #pyrosim.Send_Cube(name="Box1", pos=[0, 2, .5] , size=[15, 1, 1], mass=10.0)
        #pyrosim.Send_Cube(name="Box2", pos=[0, 3, 1] , size=[15, 1, 1.5], mass=10.0)

        pyrosim.End()
    
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1] , size=[1, 1, 1])

        # First set of legs
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [.25, .5 , .6],
                            jointAxis="1 1 1")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0] , size=[.2, 1, .2])

        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [.25, -.5, .6],
                            jointAxis="1 1 1")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -.5, 0] , size=[.2, 1, .2])

        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-.5, .25 , .6],
                            jointAxis="1 1 1")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-.5, 0, 0] , size=[1, .2, .2])

        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [.5, .25 , .6],
                            jointAxis="1 1 1")
        pyrosim.Send_Cube(name="RightLeg", pos=[.5, 0, 0] , size=[1, .2, .2])

        # Second set of legs
        pyrosim.Send_Joint( name = "Torso_FrontLeg2" , parent= "Torso" , child = "FrontLeg2" , type = "revolute", position = [-.25, .5 , .6],
                            jointAxis="0 0 1")
        pyrosim.Send_Cube(name="FrontLeg2", pos=[0, 0.5, 0] , size=[.2, 1, .2])

        pyrosim.Send_Joint( name = "Torso_BackLeg2" , parent= "Torso" , child = "BackLeg2" , type = "revolute", position = [-.25, -.5, .6],
                            jointAxis="0 0 1")
        pyrosim.Send_Cube(name="BackLeg2", pos=[0, -.5, 0] , size=[.2, 1, .2])

        pyrosim.Send_Joint( name = "Torso_LeftLeg2" , parent= "Torso" , child = "LeftLeg2" , type = "revolute", position = [-.5, -.25 , .6],
                            jointAxis="0 0 1")
        pyrosim.Send_Cube(name="LeftLeg2", pos=[-.5, 0, 0] , size=[1, .2, .2])

        pyrosim.Send_Joint( name = "Torso_RightLeg2" , parent= "Torso" , child = "RightLeg2" , type = "revolute", position = [.5, -.25 , .6],
                            jointAxis="0 0 1")
        pyrosim.Send_Cube(name="RightLeg2", pos=[.5, 0, 0] , size=[1, .2, .2])


        # Next set of leg pieces
        pyrosim.Send_Joint( name = "FrontLeg_FrontFoot" , parent= "FrontLeg" , child = "FrontFoot" , type = "revolute", position = [0, .7, 0],
                           jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontFoot", pos=[0, 0.5, 0] , size=[.1, .6, .1])

        pyrosim.Send_Joint( name = "BackLeg_BackFoot" , parent= "BackLeg" , child = "BackFoot" , type = "revolute", position = [0, -.7, 0],
                            jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackFoot", pos=[0, -.5, 0] , size=[.1, .6, .1])

        pyrosim.Send_Joint( name = "LeftLeg_LeftFoot" , parent= "LeftLeg" , child = "LeftFoot" , type = "revolute", position = [-.7, 0, 0],
                            jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftFoot", pos=[-0.5, 0, 0] , size=[.6, .1, .1])
        
        pyrosim.Send_Joint( name = "RightLeg_RightFoot" , parent= "RightLeg" , child = "RightFoot" , type = "revolute", position = [.7, 0, 0],
                            jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightFoot", pos=[.5, 0, 0] , size=[.6, .1, .1])


        pyrosim.Send_Joint( name = "FrontLeg2_FrontFoot2" , parent= "FrontLeg2" , child = "FrontFoot2" , type = "revolute", position = [0, .7, 0],
                           jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontFoot2", pos=[0, 0.5, 0] , size=[.1, .6, .1])

        pyrosim.Send_Joint( name = "BackLeg2_BackFoot2" , parent= "BackLeg2" , child = "BackFoot2" , type = "revolute", position = [0, -.7, 0],
                            jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackFoot2", pos=[0, -.5, 0] , size=[.1, .6, .1])

        pyrosim.Send_Joint( name = "LeftLeg2_LeftFoot2" , parent= "LeftLeg2" , child = "LeftFoot2" , type = "revolute", position = [-.7, 0, 0],
                            jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftFoot2", pos=[-0.5, 0, 0] , size=[.6, .1, .1])
        
        pyrosim.Send_Joint( name = "RightLeg2_RightFoot2" , parent= "RightLeg2" , child = "RightFoot2" , type = "revolute", position = [.7, 0, 0],
                            jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightFoot2", pos=[.5, 0, 0] , size=[.6, .1, .1])





        #pyrosim.Send_Joint( name = "FrontFoot_FrontTail" , parent= "FrontFoot" , child = "FrontTail" , type = "revolute", position = [0, .5, 0],
         #                  jointAxis="0 0 1")
        #pyrosim.Send_Cube(name="FrontTail", pos=[0, 0.5, 0] , size=[.05, .4, .05])

        #pyrosim.Send_Joint( name = "BackFoot_BackTail" , parent= "BackFoot" , child = "BackTail" , type = "revolute", position = [0, -.5, 0],
         #                  jointAxis="0 0 1")
        #pyrosim.Send_Cube(name="BackTail", pos=[0, -0.5, 0] , size=[.05, .4, .05])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.id)+".nndf")

        sensorNames = ["FrontFoot", "BackFoot", "RightFoot", "LeftFoot"]
        motorNames = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg",
                        "FrontLeg_FrontFoot", "BackLeg_BackFoot", "LeftLeg_LeftFoot", "RightLeg_RightFoot",
                        "Torso_BackLeg2", "Torso_FrontLeg2", "Torso_LeftLeg2", "Torso_RightLeg2",
                        "FrontLeg2_FrontFoot2", "BackLeg2_BackFoot2", "LeftLeg2_LeftFoot2", "RightLeg2_RightFoot2"]

        for i in range(len(sensorNames)):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = sensorNames[i])

        offset = len(sensorNames)
        for j in range(len(motorNames)):
            pyrosim.Send_Motor_Neuron( name = j+offset , jointName = motorNames[j])

        sensorNames2 = ["FrontFoot2", "BackFoot2", "RightFoot2", "LeftFoot2"]
        motorNames2 = ["Torso_BackLeg2", "Torso_FrontLeg2", "Torso_LeftLeg2", "Torso_RightLeg2",
                        "FrontLeg2_FrontFoot2", "BackLeg2_BackFoot2", "LeftLeg2_LeftFoot2", "RightLeg2_RightFoot2"]

        offset += len(motorNames)
        # gotta renumber
        #for i in range(len(sensorNames2)):
         #   pyrosim.Send_Sensor_Neuron(name = i+offset, linkName = sensorNames2[i])

        offset += len(sensorNames2)
        #for j in range(len(motorNames2)):
         #   pyrosim.Send_Motor_Neuron( name = j+offset , jointName = motorNames2[j])
        

        for row in range(c.numSensorNeurons):
            for column in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = row, targetNeuronName = column+4, weight = self.weights[row, column])

        #for row in range(c.numSensorNeurons//2, c.numSensorNeurons):
         #   for column in range(c.numMotorNeurons//2, c.numMotorNeurons):
          #      pyrosim.Send_Synapse( sourceNeuronName = row, targetNeuronName = column+4, weight = self.weights[row, column])


        """
        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = .8 )
        pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = 1.2 )

        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 4 , weight = .2 )
        pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 1.0 )
        """

        pyrosim.End()