from simulation import SIMULATION
import sys


directOrGUI = sys.argv[1]
id = sys.argv[2]
simulation = SIMULATION(directOrGUI, id)

simulation.Run(directOrGUI)
simulation.Get_Fitness()