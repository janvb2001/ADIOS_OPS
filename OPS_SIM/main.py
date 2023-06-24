
import time
import random

import numpy as np

from inputs import *
from setup import *
from simulation import *

import matplotlib.pyplot as plt

storeData = True

# setup the ararys to keep track of the litters and drones
drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar, pathplanningPar)

sli = open("small_litter.txt", 'a')

bli = open("big_litter.txt", 'a')

# setup the 3D plot
if simPar["plotOperation"]:
    map_ax, lip0, lip1, drp0, drp1 = plotSetup(litters, drones, groundStatInput, areaInput, pathplanningPar, initPlot=True)
else:
    map_ax = lip0 = lip1 = drp0 = drp1 = None



# simulate

litters1, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1, drp0, drp1, litterInput, droneInput, storeData)
# print(np.average(drones[0][0].flyingPHistory))
# print(np.average(drones[1][0].flyingPHistory))

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

