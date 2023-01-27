import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
#os.system("python generate.py")
#os.system("python simulate.py")
phc.Evolve()
phc.Show_Best()