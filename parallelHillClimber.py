from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brains\\brain*.nndf")
        os.system("del fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        self.fitnessProgression = np.zeros((c.numberOfGenerations))
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        
        self.parents[0].Evaluate("GUI")

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)
        print(self.fitnessProgression)

    def Evolve_For_One_Generation(self, gen):
        
        self.Spawn()
        self.Mutate()

        self.Evaluate(self.children)       
        
        #self.Print()
        self.Select(gen)
        self.CleanBrains()

    def Evaluate(self, solutions):
        for key, val in solutions.items():
            val.Start_Simulation("DIRECT")
        for key, val in solutions.items():
            val.Wait_For_Simulation_To_End()

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1  
            #print(self.children[key]) 
                 

    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()

    def Select(self, gen):
        self.saveForPlot(gen)
        for key in self.children:
            if(self.children[key].fitness > self.parents[key].fitness):
                self.parents[key] = self.children[key]

    def Print(self):
        for key in self.parents:
            print("")
            print(self.parents[key].fitness, "vs.", self.children[key].fitness)
            print("")
        best = max(self.parents, key = lambda x: self.parents[x].fitness)
        print("Best was:", self.parents[best].fitness)

    def Show_Best(self):
        best = max(self.parents, key = lambda x: self.parents[x].fitness)
        self.parents[best].End_Simulations()
        np.save("FitnessProgression.npy", np.array(self.fitnessProgression))

    def saveForPlot(self, gen):
        best = max(self.parents, key = lambda x: self.parents[x].fitness)
        self.fitnessProgression[gen] = self.parents[best].fitness

    def cleanBrains(self):
        best = max(self.parents, key = lambda x: self.parents[x].fitness)
        keepBrain = self.parents[best].id
        for item in os.listdir(os.getcwd()+"\\brains"):
            if(item != "brain"+str(keepBrain)+".nndf"):
                os.system("del "+item)
        pass
        