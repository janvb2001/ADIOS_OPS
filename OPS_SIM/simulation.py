import random
import time
import matplotlib.pyplot as plt

from plotting import *


def simulate(drones, litters, grid, groundstat, simPar, pathpp, map_ax, lip0, lip1, drp0, drp1, litterin, dronein):
    maxvreached = 0

    t = 0.
    dt = simPar["dt"]
    tstart = time.time()
    run = True
    while run:
        countloops = 0
        while t < simPar["runspeed"] * (time.time() - tstart) and countloops < simPar["maxplotloops"]:

            for drtype in range(len(drones)):
                dcount = 0
                for d in drones[drtype]:
                    d.updateDrone(dt, t, litters, pathpp["gridresolution"], groundstat, simPar, grid, litterin["drivingdist"][drtype], dronein, dcount)

                    if abs(d.flyingv) > maxvreached:
                        maxvreached = abs(d.flyingv)
                        # print(maxvreached)

                    # print("drtype: ", drtype, "dcount: ", dcount, ", t: ", t, ", x: ", d.x, ', y: ', d.y, ", z: ", d.z)
                    dcount += 1

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
        # print(totalLitter)
        if totalLitter == 0:
            totDoneDrones = 0
            for i in range(len(drones)):
                for d in drones[i]:
                    if d.X[0] == groundstat["x"] and d.X[1] == groundstat["y"] and d.X[2] == 0:
                        totDoneDrones += 1
            if totDoneDrones == sum(dronein["amountDrone"]):
                run = False
                print("all litter is cleaned")

    print("Time to run simulation: ", time.time() - tstart, " seconds")
    print("All litter is cleaned after: ", int(t / 60), " minutes")
    print("Max v reached by drones is: ", round(maxvreached, 2), " m/s")

    if simPar["plotOperation"]:
        # Make sure the plot remains on screen when program is finished
        plt.show(block=True)

    return litters, t


