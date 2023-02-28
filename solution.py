import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, id, seed):
        self.weights = np.random.rand(c.maxSegments*3, c.maxSegments*3)
        self.weights = self.weights * 2 - 1
        self.id = id
        self.sensorNames = []
        self.motorNames = []
        self.existing = 0
        self.seed = seed
        
    def Set_ID(self, num):
        self.id = num

    def Evaluate(self, dOG):
        self.Start_Simulation(dOG)
        self.Wait_For_Simulation_To_End()

    def End_Simulations(self):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python simulate.py GUI " + str(self.id) + " " + str(self.seed))

    def Start_Simulation(self, dOG):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("start /B python simulate.py " + dOG + " " + str(self.id)+ " " + str(self.seed))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness"+str(self.id)+".txt"):
            time.sleep(.01)
        while True:
            try:
                f = open("fitness"+str(self.id)+".txt", "r")
                break
            except:
                pass
        self.fitness = float(f.read())
        
        f.close()
        os.remove("fitness"+str(self.id)+".txt")

    def Mutate(self):
        row = random.randint(0, min(len(self.sensorNames)-1, c.maxSegments*3-1))
        col = random.randint(0, min(len(self.motorNames)-1, c.maxSegments*3-1))

        self.weights[row, col] = random.random() * 2 - 1

        segChoice = random.randint(2, self.segments-1)
        dimensionChoice = random.randint(0, 3)
        self.modifyBody(segChoice, dimensionChoice)

    def modifyBody(self, seg, dimC):
        if(dimC == 0):
            self.segLengths[seg] += random.random()-.5
        elif(dimC == 1):
            self.segWidths[seg] += random.random()-.5
        else:
            self.segHeights[seg] += random.random()-.5

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        #pyrosim.Send_Cube(name="Box", pos=[3, 3, .5] , size=[1, 1, 1]) 
        #pyrosim.Send_Cube(name="Box", pos=[0, 2.5, .2] , size=[15, 2, .3], mass=100.0) 
        #pyrosim.Send_Cube(name="Box1", pos=[0, 2, .5] , size=[15, 1, 1], mass=10.0)
        #pyrosim.Send_Cube(name="Box2", pos=[0, 3, 1] , size=[15, 1, 1.5], mass=10.0)

        pyrosim.End()
    
    def Generate_Body(self):
        pyrosim.Start_URDF("bodies\\"+str(self.seed)+"seedbody"+str(self.id)+".urdf")

        if(not self.existing):
            np.random.seed(self.seed)
            self.segments = np.random.randint(low=5, high=c.maxSegments)        
            self.segLengths = np.random.rand(self.segments)+.01
            self.segHeights = np.random.rand(self.segments)+.3
            self.segWidths = np.random.rand(self.segments)+.3
            self.sensors = np.random.randint(0, 2, size=self.segments)
        cStyle = np.random.randint(0, 3, size=self.segments)
        tallest = 3      
        #head counts as zero
        if self.sensors[0] == 1:
            pyrosim.Send_Cube(name="0", pos=[0, 0, tallest] , size=[.5, .5, .5], 
                                color='0 0 1.0 1.0', colorName = 'Green')
            self.sensorNames.append(str(0))
        else:
            pyrosim.Send_Cube(name="0", pos=[0, 0, tallest] , size=[.5, .5, .5], 
                              color='0 0 1.0 1.0', colorName = 'Blue')


        # First segment
        pyrosim.Send_Joint( name = "0_"+str(1) , parent= "0" , child = str(1) , 
                           type = "revolute", position = [.25, 0, tallest],
                            jointAxis="1 1 1")
        
        #position is half of OWN width for cubes
        if self.sensors[1] == 1:
            self.sensorNames.append(str(1))
            pyrosim.Send_Cube(name=str(1), pos=[self.segLengths[1]/2, 0, 0] , 
                              size=[self.segLengths[1], self.segWidths[1], self.segHeights[1]], color='0 0 1.0 1.0', 
                              colorName = 'Green')
        else:
            pyrosim.Send_Cube(name=str(1), pos=[self.segLengths[1]/2, 0, 0] , 
                              size=[self.segLengths[1], self.segWidths[1], self.segHeights[1]], color='0 0 1.0 1.0', 
                              colorName = 'Blue')

        self.motorNames.append(str(0)+"_"+str(1))

        # The rest can be generated in sequence
        # position of joints is FULL width of the previous segment
        curSeg = 2

        # One side
        lastMove = 1
        for i in range(2, self.segments):
            boxColor = '0 0 1.0 1.0'
            boxColorName = 'Blue'

            jMove, cMove = self.Get_Move(lastMove, cStyle[i], self.segWidths, -self.segLengths, self.segHeights, i)
            lastMove = cStyle[i]

            if self.sensors[i] == 1:
                boxColor = '0 1.0 0 1.0'
                boxColorName = 'Green'
                self.sensorNames.append(str(i))

            if(i == 2):
                pyrosim.Send_Joint(name = str(1)+"_"+str(curSeg) , parent= str(1) , child = str(curSeg) , 
                                type = "revolute", position = [self.segLengths[i-1]/2, -self.segWidths[i-1]/2, 0], 
                                jointAxis="1 1 1")
                pyrosim.Send_Cube(name=str(curSeg), pos=[0, -self.segLengths[i]/2, 0] , 
                                  size=[self.segWidths[i], self.segLengths[i], self.segHeights[i]], 
                              color=boxColor, colorName = boxColorName)
            else:
                pyrosim.Send_Joint( name = str(curSeg-1)+"_"+str(curSeg) , parent= str(curSeg-1) , child = str(curSeg) , 
                                type = "revolute", position = jMove, jointAxis="1 1 1")
                pyrosim.Send_Cube(name=str(curSeg), pos= cMove , size=[self.segWidths[i], self.segLengths[i], self.segHeights[i]], 
                                color=boxColor, colorName = boxColorName)
            
            self.motorNames.append(str(i-1)+"_"+str(i))
            curSeg += 1

        # Opposing side
        lastMove = 1
        for j in range(2, self.segments):
            boxColor = '0 0 1.0 1.0'
            boxColorName = 'Blue'

            jMove, cMove = self.Get_Move(lastMove, cStyle[j], self.segWidths, self.segLengths, self.segHeights, j)
            lastMove = cStyle[j]

            if self.sensors[j] == 1:
                boxColor = '0 1.0 0 1.0'
                boxColorName = 'Green'
                self.sensorNames.append(str(j))
            
            if(j == 2):
                pyrosim.Send_Joint(name = str(1)+"_"+str(curSeg) , parent= str(1) , child = str(curSeg) , 
                                type = "revolute", position = [self.segLengths[j-1]/2, self.segWidths[j-1]/2, 0], 
                                jointAxis="1 1 1")
                self.motorNames.append(str(1)+"_"+str(curSeg))
                pyrosim.Send_Cube(name=str(curSeg), pos=[0, self.segLengths[j]/2, 0] , 
                                  size=[self.segWidths[j], self.segLengths[j], self.segHeights[j]], 
                              color=boxColor, colorName = boxColorName)
            else:
                pyrosim.Send_Joint( name = str(curSeg-1)+"_"+str(curSeg) , parent= str(curSeg-1) , child = str(curSeg) , 
                                type = "revolute", position = jMove, jointAxis="1 1 1")
                self.motorNames.append(str(curSeg-1)+"_"+str(curSeg))
                pyrosim.Send_Cube(name=str(curSeg), pos= cMove , size=[self.segWidths[j], self.segLengths[j], self.segHeights[j]], 
                              color=boxColor, colorName = boxColorName)
            curSeg += 1
        self.existing = 1

        pyrosim.End()

    def Get_Move(self, lastMove, curMove, segWidths, segLengths, segHeights, segNum):
        jointOperation = []
        cubeOperation = [[-segWidths[segNum]/2, 0, 0], [0, segLengths[segNum]/2, 0], [0, 0, -segHeights[segNum]/2]]
        if(lastMove == 0):
            xMoves = [[-segWidths[segNum-1], 0, 0], 
                      [-segWidths[segNum-1]/2, segLengths[segNum-1]/2, 0], 
                      [-segWidths[segNum-1]/2, 0, -segHeights[segNum-1]/2]]
            jointOperation = xMoves[curMove]
            cubeOperation = cubeOperation[curMove]
        elif(lastMove == 1):
            yMoves = [[-segWidths[segNum-1]/2, segLengths[segNum-1]/2, 0], 
                      [0, segLengths[segNum-1], 0], 
                      [0, segLengths[segNum-1]/2, -segHeights[segNum-1]/2]]
            jointOperation = yMoves[curMove]
            cubeOperation = cubeOperation[curMove]
        else:
            zMoves = [[-segWidths[segNum-1]/2, 0, -segHeights[segNum-1]/2], 
                      [0, segLengths[segNum-1]/2, -segHeights[segNum-1]/2], 
                      [0, 0, -segHeights[segNum-1]]]
            jointOperation = zMoves[curMove]
            cubeOperation = cubeOperation[curMove]
        return jointOperation, cubeOperation



    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brains\\"+str(self.seed)+"seedbrain"+str(self.id)+".nndf")

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