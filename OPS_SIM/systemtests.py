
import time
import random

import numpy as np

from inputs import *
from setup import *
from simulation import *

import matplotlib.pyplot as plt

def dtVar(dts):
    times = []

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    for i in range(len(dts)):
        print("dt: ", dts[i])
        simPar["dt"] = dts[i]
        # setup the ararys to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, tdone = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1,
                                  drp0, drp1,
                                  litterInput, droneInput)
        times.append(tdone)

    plt.plot(dts, times)
    plt.xscale('log')

    plt.show()





# Tests differing the dt in the program
# dts = [0.0005, 0.001, 0.002, 0.003, 0.004,
# dts = [0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
dts = [0.1, 0.5, 1.]

dtVar(dts)



# # simulate
# litters1, tdone = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1, drp0, drp1, litterInput, droneInput)
#
# simPar["dt"] = 0.01
# # setup the ararys to keep track of the litters and drones
# drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar, pathplanningPar)
#
# litters2, tdone = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1, drp0, drp1, litterInput, droneInput)
#
# xs = []
# ys = []
#
# for i in range(len(litters1[1])):
#     xs.append(3 * i + 0.5)
#     xs.append(3 * i + 1)
#     xs.append(3 * i + 1.5)
#
#     ys.append(litters1[1][i].timedist["litterChoose"])
#     ys.append(litters1[1][i].timedist["landed"])
#     ys.append(litters1[1][i].timedist["litterReached"])
#
#
#
# xs1 = []
# ys1 = []
#
# for i in range(len(litters2[1])):
#     xs1.append(3 * i + 0.5)
#     xs1.append(3 * i + 1)
#     xs1.append(3 * i + 1.5)
#
#     ys1.append(litters2[1][i].timedist["litterChoose"])
#     ys1.append(litters2[1][i].timedist["landed"])
#     ys1.append(litters2[1][i].timedist["litterReached"])
#
# plt.plot(xs, ys, color="r", marker=".", markersize = 3)
# plt.plot(xs1, ys1, color="orange",marker=".", markersize=3)
#
# plt.legend(["dt=0.1", "dt=1"])
#
# plt.show()
#
# print("stop")

