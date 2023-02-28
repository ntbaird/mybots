from simulation import SIMULATION
import sys


directOrGUI = sys.argv[1]
id = sys.argv[2]
seed = sys.argv[3]
simulation = SIMULATION(directOrGUI, id, seed)

simulation.Run(directOrGUI)
simulation.Get_Fitness()