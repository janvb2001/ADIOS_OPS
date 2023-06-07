import random
import time
import matplotlib.pyplot as plt

from plotting import *


def simulate(drones, litters, groundstat, simPar, map_ax, lip0, lip1, drp0, drp1):
    t = 0
    dt = simPar["dt"]
    tstart = time.time()
    run = True
    while run:
        countloops = 0
        while t < simPar["runspeed"] * (time.time() - tstart) and countloops < simPar["maxplotloops"]:

            for drtype in range(len(drones)):
                # dcount = 0
                for d in drones[drtype]:
                    d.updateDrone(dt, litters, groundstat)
                    # print("drtype: ", drtype, "dcount: ", dcount, ", t: ", t, ", x: ", d.x, ', y: ', d.y, ", z: ", d.z)
                    # dcount += 1

            t += dt
            countloops += 1

        plot(litters, drones, map_ax, lip0, lip1, drp0, drp1)
        if time.time() - tstart > 600:
            run = False

    # Make sure the plot remains on screen when program is finished
    plt.show(block=True)
