import random
import time
import matplotlib.pyplot as plt

from plotting import *


def simulate(drones, litters, groundstat, simPar, pathpp, map_ax, lip0, lip1, drp0, drp1):
    t = 0.
    dt = simPar["dt"]
    tstart = time.time()
    run = True
    while run:
        countloops = 0
        while t < simPar["runspeed"] * (time.time() - tstart) and countloops < simPar["maxplotloops"]:

            for drtype in range(len(drones)):
                # dcount = 0
                for d in drones[drtype]:
                    d.updateDrone(dt, t, litters, pathpp["gridresolution"], groundstat, simPar)
                    # print("drtype: ", drtype, "dcount: ", dcount, ", t: ", t, ", x: ", d.x, ', y: ', d.y, ", z: ", d.z)
                    # dcount += 1

            t += dt
            # print(t)
            countloops += 1

        if simPar["plotOperation"]:
            amount = plot(litters, drones, map_ax, lip0, lip1, drp0, drp1)
        else:
            amount = [0, 0]
            for i in range(len(litters)):
                for l in range(len(litters[i])):
                    if not litters[i][l].picked:
                        amount[i] += 1

        totalLitter = sum(amount)
        if totalLitter == 0:
            run = False
            print("all litter is cleaned")

    # Make sure the plot remains on screen when program is finished
    plt.show(block=True)

    print("Time to run simulation: ", time.time()-tstart)
    print("All litter is cleaned after: ", int(t/60), " minutes")
