import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import time
from math import sqrt
import time

# Things to include:
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
# - 3D
# - Drone accellerations

# Done:
# - Drones should have a delay at the ground station and each litter piece (Which can be deduced from req.)
# - Include the possibility for the van to drive

from generalFunc import *
from simParameters import *

# starting position of ground station
from driving_droneSetup import *
from vanSetup import *
from litterSetup import *
from dronesSetup import *
from simulation import *

# setup van
if simInput["vanMovement"] >= 1:
    van = Van(int(simInput["x_size"]/2), int(simInput["y_size"]/2))
    simInput["van"] = van

#setup the driving drones
ddrones = []
simInput, ddrone = ddronePosData(simInput)
ddrones.append(ddrone)

#Determine where the litter is located
simInput = litterDist(simInput)



#Setup the drones
drones = []
active_drones = []
for d in range(simInput["drone_n"]):
    # x_pos, y_pos, t_busy, drone_v, t_lit, t_ground, charge0, t_recharge
    drones.append(Drone(simInput["ground_stat_pos"][0], simInput["ground_stat_pos"][1], simInput["v_drone"], simInput["t_lit"], simInput["t_ground"], simInput["charge0"], simInput["t_recharge"]))

    active_drones.append(d)
simInput["drones"] = drones
simInput["active_drones"] = active_drones


#Run the simulation
simResults = simulate(simInput)


