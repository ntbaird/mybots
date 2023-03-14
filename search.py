import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

for i in range(10):
    
    phc = PARALLEL_HILL_CLIMBER(i)
        #os.system("python generate.py")
        #os.system("python simulate.py")
    phc.Evolve()
    phc.Show_Best()
        #os.system("python analyze.py")