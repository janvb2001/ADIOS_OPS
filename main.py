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
van = Van(int(simInput["x_size"]/2), int(simInput["y_size"]/2))
simInput["van"] = van

#setup the driving drones
ddrones = []
if simInput["vanMovement"] == 0:
    par = [simInput["x_size"]/2, simInput["y_size"]/2]
elif simInput["vanMovement"] == 1:
    par = [simInput["x_size"] / 10, simInput["y_size"] / 10]
elif simInput["vanMovement"] == 2:
    par = [0,0]
elif simInput["vanMovement"] == 3:
    par = [simInput["x_size"] / 10, simInput["y_size"] / 20]
simInput, ddrone = ddronePosData(simInput, par)
ddrones.append(ddrone)

simInput["ddrones"] = ddrones

#Determine where the litter is located
simInput = litterDist(simInput)

#Setup the drones
drones = []
active_drones = []
for dd in range(len(ddrones)):
    for d in range(simInput["drone_n"]):
        # x_pos, y_pos, t_busy, drone_v, t_lit, t_ground, charge0, t_recharge
        drones.append(Drone(ddrones[dd].x, ddrones[dd].y, simInput["v_drone"], simInput["t_lit"], simInput["t_ground"], simInput["charge0"], simInput["t_recharge"], dd))

        active_drones.append(dd * simInput["drone_n"] + d)
simInput["drones"] = drones
simInput["active_drones"] = active_drones


#Run the simulation
simResults = simulate(simInput)

print("Total drone distance is: " + str(simResults["totald"]) + " m")
print("End time is: " + str(simResults["totalT"]) + " s")


