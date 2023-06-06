import numpy as np
import random as rnd

from drone import *
from litter import *

def setupClasses(litterIn, droneIn, gsIn, areaIn):
    #drones = np.zeros(droneIn["dronetotal"])
    drones = []
    for i in range(len(droneIn["amountDrone"])):
        drones.append([])
        for j in range(droneIn["amountDrone"][i]):
            d = drone(gsIn["x"], gsIn["y"], 0, i, droneIn["vertv"][i], droneIn["maxv"][i], droneIn["drivev"][i],
                      droneIn["maxvol"][i], droneIn["power"][i], droneIn["maxBat"][i], droneIn["litPickT"][i],
                      droneIn["litDropT"][i], droneIn["b"][i], droneIn["d"][i], droneIn["k"][i], droneIn["m"][i],
                      droneIn["Ixx"][i], droneIn["Iyy"][i], droneIn["Izz"][i], 9.80665)

            drones[i].append(d)

    litters = []
    rnd.seed(litterIn["seed"])
    for i in range(len(litterIn["littern"])):
        litters.append([])
        for j in range(litterIn["littern"][i]):
            lx = rnd.random() * areaIn["xsize"]
            ly = rnd.random() * areaIn["ysize"]
            lvol = rnd.random() * (litterIn["maxvol"][i] - litterIn["minvol"]) + litterIn["minvol"]

            l = litter(lx, ly, 0, i, lvol)
            litters[i].append(l)

    return drones, litters
