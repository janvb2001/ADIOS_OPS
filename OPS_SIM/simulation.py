import random
import time
import matplotlib.pyplot as plt

from plotting import *


def simulate(drones, litters, groundstat, simPar, map_ax, lip0, lip1, lip2, drp0, drp1, drp2):
    t = 0
    dt = simPar["dt"]
    tstart = time.time()
    run = True
    while run:
        countloops = 0
        while t < simPar["runspeed"] * (time.time() - tstart) and countloops < simPar["maxplotloops"]:
            # a = random.randint(0,len(litters)-1)
            # b = random.randint(0,len(litters[a])-1)
            # litters[a][b].avail = False

            for drtype in range(len(drones)):
                # dcount = 0
                for d in drones[drtype]:
                    d.updateDrone(dt)
                    # print("drtype: ", drtype, "dcount: ", dcount, ", t: ", t, ", x: ", d.x, ', y: ', d.y, ", z: ", d.z)
                    # dcount += 1


            t += dt
            countloops += 1

        plot(litters, drones, map_ax, lip0, lip1, lip2, drp0, drp1, drp2)
        if time.time() - tstart > 50:
            run = False

    # Make sure the plot remains on screen when program is finished
    plt.show(block=True)
