import os
from hillclimber import HILL_CLIMBER

hc = HILL_CLIMBER()
#os.system("python generate.py")
#os.system("python simulate.py")
hc.Evolve()
hc.Show_Best()