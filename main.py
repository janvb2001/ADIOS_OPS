import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import time
from math import sqrt
import time

# Things to include:
# - Drones should have a delay at the ground station and each litter piece (Which can be deduced from req.)
# - Drones should not get too close to each other
# - Simulate the reasonable worst-case scenario
#     - van position is not ideal
#     - Garbage position is not ideal
# - Include different litter types in the program
# - Include different drone types in the program
# - Include obstacles
# - Include reconnaisance drone
# - Wind
# - keep track of litter volume in driving drone
# - keep track of when drone must be recharged

# Done:
# - Include the possibility for the van to drive
from generalFunc import *
from simParameters import *

# starting position of ground station
from vanMovement import *
from litterDistribution import *
from simulation import *

#Determine the checkpoints of the van
simInput = vanPosData(simInput)

#Determine where the litter is located
simInput = litterDist(simInput)

#Run the simulation
simResults = simulate(simInput)


