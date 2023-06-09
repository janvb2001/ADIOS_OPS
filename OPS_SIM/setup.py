import numpy as np
import random as rnd

from drone import *
from litter import *
from generalFunc import *
import AstarMultiplepoints
import time

def setupClasses(litterIn, droneIn, gsIn, areaIn, simpar, pathplanningPar):
    #drones = np.zeros(droneIn["dronetotal"])
    drones = []
    for i in range(len(droneIn["amountDrone"])):
        drones.append([])
        for j in range(droneIn["amountDrone"][i]):
            d = drone(gsIn["x"], gsIn["y"], 0, i, droneIn["vertv"][i], droneIn["maxv"][i], droneIn["drivev"][i],
                      droneIn["maxvol"][i], droneIn["battothrusteff"][i], droneIn["powerFlightcom"][i], droneIn["powergrabbing"][i], droneIn["powerDriving"][i], droneIn["powerObjDetec"][i], droneIn["maxBat"][i], droneIn["litPickT"][i],
                      droneIn["litDropT"][i], droneIn["recharget"][i], droneIn["b"][i], droneIn["d"][i], droneIn["k"][i], droneIn["m"][i], droneIn["S_blade"][i],
                      droneIn["Ixx"][i], droneIn["Iyy"][i], droneIn["Izz"][i], 9.80665, simpar["dt"])

            drones[i].append(d)

    # Obstructions:
    # [[(),(),(),()],[(),(),(),()],[(),(),(),()]]

    animation = pathplanningPar["animation"]
    WIDTH = areaIn["xsize"]
    LENGTH = areaIn["ysize"]
    gap = pathplanningPar["gridresolution"]
    gs = dict(x=gsIn["x"], y=gsIn["y"])


    grid, rowsx, rowsy = AstarMultiplepoints.make_grid(LENGTH, WIDTH, gap)

    pos = (gs["x"], gs["y"])
    row, col = AstarMultiplepoints.get_clicked_pos(pos, gap)
    spot = grid[row][col]
    start = spot
    start.make_start()

    for obstacle in pathplanningPar["obstacles"]:
        indicesSquareCorners(obstacle, gap, LENGTH, WIDTH, grid)


    # Litters
    litters = []
    ends = []
    rnd.seed(litterIn["seed"])
    for i in range(len(litterIn["littern"])):
        litters.append([])
        for j in range(litterIn["littern"][i]):
            searching = True
            while searching:
                lx = rnd.random() * areaIn["xsize"]
                ly = rnd.random() * areaIn["ysize"]
                lvol = rnd.random() * (litterIn["maxvol"][i] - litterIn["minvol"][i]) + litterIn["minvol"][i]

                pos = (lx, ly)
                row, col = AstarMultiplepoints.get_clicked_pos(pos, gap)
                if row < len(grid) and col < len(grid[row]):
                    spot = grid[row][col]
                elif row >= len(grid):
                    spot = grid[row - 1][col]
                elif col >= len(grid[row]):
                    spot = grid[row][col - 1]

                end = spot
                if end.color == (255, 255, 255) or end.color == (64, 224, 208):
                    end.litteri.append([i, j])

                    ends.append(end)
                    end.make_end()
                    searching = False

            l = litter(lx, ly, 0, i, lvol)
            litters[i].append(l)



    t = time.time()
    f=pathplanningPar["factor_animation"]
    AstarMultiplepoints.main(grid, start, ends, gap, LENGTH, WIDTH, rowsx, rowsy, litters, animation, f)
    print(time.time() - t)


    return drones, litters, grid
