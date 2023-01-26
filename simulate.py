from simulation import SIMULATION
import sys


directOrGUI = sys.argv[1]
simulation = SIMULATION(directOrGUI)

simulation.Run(directOrGUI)
simulation.Get_Fitness()