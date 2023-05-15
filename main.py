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
import numpy as np
from tempfile import TemporaryFile

# starting position of ground station
from driving_droneSetup import *
from vanSetup import *
from litterSetup import *
from dronesSetup import *
from simulation import *

def runsim(simInput, x_space):

    ddrones = []
    if simInput["vanMovement"] == 0:
        par = [simInput["x_size"] / 2, simInput["y_size"] / 2]
    elif simInput["vanMovement"] == 1:
        par = [x_space, x_space]
    elif simInput["vanMovement"] == 2:
        par = [0, 0]
    elif simInput["vanMovement"] == 3:
        par = [x_space, simInput["y_size"] / 20]

    simInput, ddrone = ddronePosData(simInput, par)
    ddrones.append(ddrone)
    simInput["ddrones"] = ddrones

    # Determine where the litter is located
    simInput = litterDist(simInput)

    # Setup the drones
    drones = []
    active_drones = []
    for dd in range(len(ddrones)):
        for d in range(simInput["drone_n"]):
            # x_pos, y_pos, t_busy, drone_v, t_lit, t_ground, charge0, t_recharge
            drones.append(
                Drone(ddrones[dd].x, ddrones[dd].y, simInput["v_drone"], simInput["t_lit"], simInput["t_ground"],
                      simInput["charge0"], simInput["t_recharge"], dd))

            active_drones.append(dd * simInput["drone_n"] + d)
    simInput["drones"] = drones
    simInput["active_drones"] = active_drones

    # Run the simulation
    simResults = simulate(simInput)

    return simResults



# setup van
van = Van(int(simInput["x_size"] / 2), int(simInput["y_size"] / 2))
simInput["van"] = van

results = np.array([])

# n_dr = 7
minTime = 5000
dx_space = (1/5 * simInput["x_size"] - 1/15 * simInput["x_size"]) / 5
# while minTime > 3600:
for n_dr in range(7,9,1):
    mini = 5000
    simInput["drone_n"] = n_dr
    for v_gdr in range(2,30,2):
        v_gdr = v_gdr / 10
        simInput["v_ddrone"] = v_gdr
        # simInput["v_ddrone"] = 0.37
        for x_space in range(4,10,1):
            # x_space = x_space * dx_space
            # x_space = x_space * dx_space
            # x_space = 10.666666666666666
            x_space = simInput["x_size"] / x_space

            # simInput["vanMovement"] = 2
            # simResults = runsim(simInput, x_space)
            #
            # if simResults["totalT"] < mini:
            #     mini = simResults["totalT"]
            # print(str(n_dr) + " drones, " + str(v_gdr) + " m/s, " + str(x_space) + " spacing, " + str(2) + " pattern, " + str(simResults["totalT"]) + " s")
            # np.append(results, np.array([n_dr, v_gdr, x_space, 2, simResults["totalT"]]))

            for moveType in range(1, 4, 2):
                if moveType != 2:
                    simInput["vanMovement"] = moveType

                    simResults = runsim(simInput, x_space)

                    if simResults["totalT"] < mini:
                       mini = simResults["totalT"]
                    printRes = "\n" + str(n_dr) + " drones, " + str(v_gdr) + " m/s, " + str(x_space) + " spacing, " + str(moveType) + " pattern, " + str(simResults["totalT"]) + " s"
                    print(printRes)

                    f = open("testdata.txt", "a")
                    f.write(printRes)
                    f.close()

                    #np.append(results, np.array([n_dr, v_gdr, x_space, moveType, simResults["totalT"]]))


    if mini < minTime:
        minTime = mini
    # n_dr += 1

#print(results)

# f = open("testdata.txt", "a")
# f.write("Now the file has more content!")
# f.close()


