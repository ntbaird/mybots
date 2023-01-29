from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del data\\fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        
        #self.parent.Evaluate("GUI")

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        
        self.Spawn()
        self.Mutate()

        self.Evaluate(self.children)       
        
        #self.Print()
        self.Select()

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

    def Select(self):
        for key in self.children:
            if(self.children[key].fitness < self.parents[key].fitness):
                self.parents[key] = self.children[key]

    def Print(self):
        for key in self.parents:
            print("")
            print(self.parents[key].fitness, "vs.", self.children[key].fitness)
            print("")

    def Show_Best(self):
        best = min(self.parents, key = lambda x: self.parents[x].fitness)
        self.parents[best].End_Simulations()