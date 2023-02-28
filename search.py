import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

for i in range(0, 8):
    if i == 2 or i == 5 or i == 6:
        pass
    else:
        phc = PARALLEL_HILL_CLIMBER(i)
        #os.system("python generate.py")
        #os.system("python simulate.py")
        phc.Evolve()
        #phc.Show_Best()
        #os.system("python analyze.py")