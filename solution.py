import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.weights = np.random.rand(c.maxSegments, c.maxSegments+1)
        self.weights = self.weights * 2 - 1
        self.id = id
        self.sensorNames = []
        self.motorNames = []
        
    def Set_ID(self, num):
        self.id = num

    def Evaluate(self, dOG):
        self.Start_Simulation(dOG)
        self.Wait_For_Simulation_To_End()

    def End_Simulations(self):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        time.sleep(1)
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
        row = random.randint(0, len(self.sensorNames)-1)
        col = random.randint(0, len(self.motorNames)-1)

        self.weights[row, col] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        #pyrosim.Send_Cube(name="Box", pos=[3, 3, .5] , size=[1, 1, 1]) 
        #pyrosim.Send_Cube(name="Box", pos=[0, 2.5, .2] , size=[15, 2, .3], mass=100.0) 
        #pyrosim.Send_Cube(name="Box1", pos=[0, 2, .5] , size=[15, 1, 1], mass=10.0)
        #pyrosim.Send_Cube(name="Box2", pos=[0, 3, 1] , size=[15, 1, 1.5], mass=10.0)

        pyrosim.End()
    
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")

        segments = np.random.randint(low=3, high=8)
        #segments = 4
        sensors = np.random.randint(0, 2, size=segments)
        segLengths = np.random.rand(segments)*1.3+.01
        segHeights = np.random.rand(segments)*1.5+.3
        segWidths = np.random.rand(segments)*1.5+.3
        tallest = np.max(segHeights)/2        
        #head counts as zero
        if sensors[0] == 1:
            pyrosim.Send_Cube(name="0", pos=[0, 0, tallest] , size=[segLengths[0], segWidths[0], segHeights[0]], 
                                color='0 0 1.0 1.0', colorName = 'Green')
            self.sensorNames.append(str(0))
        else:
            pyrosim.Send_Cube(name="0", pos=[0, 0, tallest] , size=[segLengths[0], segWidths[0], segHeights[0]], 
                              color='0 0 1.0 1.0', colorName = 'Blue')


        # First segment
        pyrosim.Send_Joint( name = "0_"+str(1) , parent= "0" , child = str(1) , 
                           type = "revolute", position = [segLengths[0]/2, 0, tallest/2],
                            jointAxis="0 1 0")
        
        #position is half of OWN width for cubes
        if sensors[1] == 1:
            self.sensorNames.append(str(1))
            pyrosim.Send_Cube(name=str(1), pos=[segLengths[1]/2, 0, tallest/2] , 
                              size=[segLengths[1], segWidths[1], segHeights[1]], color='0 0 1.0 1.0', 
                              colorName = 'Green')
        else:
            pyrosim.Send_Cube(name=str(1), pos=[segLengths[1]/2, 0, tallest/2] , 
                              size=[segLengths[1], segWidths[1], segHeights[1]], color='0 0 1.0 1.0', 
                              colorName = 'Blue')

        self.motorNames.append(str(0)+"_"+str(1))

        # The rest can be generated in sequence
        # position of joints is FULL width of the previous segment
        for i in range(2, segments):
            boxColor = '0 0 1.0 1.0'
            boxColorName = 'Blue'

            if sensors[i] == 1:
                boxColor = '0 1.0 0 1.0'
                boxColorName = 'Green'
                self.sensorNames.append(str(i))

            pyrosim.Send_Joint( name = str(i-1)+"_"+str(i) , parent= str(i-1) , child = str(i) , 
                                type = "revolute", position = [segLengths[i-1], 0, 0], jointAxis="0 1 0")
            pyrosim.Send_Cube(name=str(i), pos=[segLengths[i]/2, 0, .3] , size=[segLengths[i], segWidths[i], segHeights[i]], 
                              color=boxColor, colorName = boxColorName)
            self.motorNames.append(str(i-1)+"_"+str(i))
                
        

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.id)+".nndf")

        sensorNames = [*set(self.sensorNames)]
        motorNames = [*set(self.motorNames)]

        for i in range(len(sensorNames)):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = sensorNames[i])

        offset = len(sensorNames)
        for j in range(len(motorNames)):
            pyrosim.Send_Motor_Neuron( name = j+offset , jointName = motorNames[j])

        for row in range(len(sensorNames)):
            for column in range(len(motorNames)):
                pyrosim.Send_Synapse( sourceNeuronName = row, targetNeuronName = column+offset, weight = self.weights[row, column])

        pyrosim.End()