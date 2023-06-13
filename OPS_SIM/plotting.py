import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def plotSetup(li, dr, gr, area, pp):
    # https://www.galaxysofts.com/new/python-creating-a-real-time-3d-plot/

    litCoor = np.array([np.zeros((len(li[0]),3)),np.zeros((len(li[1]),3))], dtype=object)
    for i in range(len(li)):
        for l in range(len(li[i])):
            if not li[i][l].picked:
                litCoor[i][l][0] = li[i][l].x
                litCoor[i][l][1] = li[i][l].y
                litCoor[i][l][2] = li[i][l].z

    droCoor = np.array([np.zeros((len(dr[0]),3)),np.zeros((len(dr[1]),3))], dtype=object)
    for i in range(len(dr)):
        for j in range(len(dr[i])):
            droCoor[i][j][0] = dr[i][j].X[0]
            droCoor[i][j][1] = dr[i][j].X[1]
            droCoor[i][j][2] = dr[i][j].X[2]

    obst = pp["obstacles"]
    h = pp["obstacleHeight"]
    alphab = pp["alpha_obst"]

    # map = plt.figure()
    # map_ax = Axes3D(map)

    map = plt.figure()
    map_ax = plt.axes(projection='3d')

    map_ax.set_xlabel("x")
    map_ax.set_ylabel("y")
    map_ax.set_zlabel("z")
    map_ax.set_aspect("equal")

    # # # Setting the axes properties
    map_ax.set_xlim3d([0.0, area["xsize"]])
    map_ax.set_ylim3d([0.0, area["ysize"]])
    map_ax.set_zlim3d([0.0, 20.0])

    cubes = []
    # voxelarray =
    # data = np.full((area["xsize"], area["ysize"], 20), False)

    buildres = pp["buildingresolution"]
    z = np.full((buildres, buildres), h)
    z[:1] = 0
    z[-1:] = 0
    z[:,:1] = 0
    z[:, -1:] = 0

    for i in range(len(obst)):
        coor = [[-1, -1], [-1, -1], [0,h]]
        coors = [[],[],[]]
        for j in range(len(obst[i])):
            # x, y, z = np.indices((area["xsize"], area["ysize"], 20))
            if obst[i][j][0] < coor[0][0] or coor[0][0] == -1:
                coor[0][0] = obst[i][j][0]
            if obst[i][j][0] > coor[0][1] or coor[0][1] == -1:
                coor[0][1] = obst[i][j][0]
            if obst[i][j][1] < coor[1][0] or coor[1][0] == -1:
                coor[1][0] = obst[i][j][1]
            if obst[i][j][1] > coor[1][1] or coor[1][1] == -1:
                coor[1][1] = obst[i][j][1]

            x = np.outer(np.linspace(coor[0][0], coor[0][1], buildres), np.ones(buildres))
            y = np.outer(np.ones(buildres), np.linspace(coor[1][0], coor[1][1], buildres))
            map_ax.plot_surface(x, y, z, color=(0,0,0), alpha=alphab, edgecolor=None)

    # for i in range(len(li)):
    #     for l in range(len(li[i])):
    #         x = li[i][l].path[:,0]
    #         y = li[i][l].path[:, 1]
    #         z = np.zeros(len(x))
    #         map_ax.plot3D(x,y,z, color="r", marker="s", markersize="1")

    lismall, = map_ax.plot3D(litCoor[0][:, 0], litCoor[0][:, 1], litCoor[0][:, 2], color='lightskyblue', marker="o", markersize=2,linestyle="None")
    limed, = map_ax.plot3D(litCoor[1][:, 0], litCoor[1][:, 1], litCoor[1][:, 2], color='lightcoral', marker="o",markersize=2, linestyle="None")
    # lilar, = map_ax.plot3D(litCoor[2][:, 0], litCoor[2][:, 1], litCoor[2][:, 2], color='r', marker="o", markersize=2, linestyle="None")

    drsmall, = map_ax.plot3D(droCoor[0][:, 0], droCoor[0][:, 1], droCoor[0][:, 2], color='deepskyblue', marker="v", markersize=6, linestyle="None")
    drmed, = map_ax.plot3D(droCoor[1][:, 0], droCoor[1][:, 1], droCoor[1][:, 2], color='indianred', marker="v", markersize=6, linestyle="None")
    # drlar, = map_ax.plot3D(droCoor[2][:, 0], droCoor[2][:, 1], droCoor[2][:, 2], color='r', marker="v", markersize=6, linestyle="None")

    grstat, = map_ax.plot3D(gr["x"], gr["y"], 0, color='purple', marker="D", markersize=7, linestyle="None")

    # plt.show(block=True)

    return map_ax, lismall, limed, drsmall, drmed


def updateplot(plot, coordinates, id, amount=-1):
    if amount == -1:
        amount = len(coordinates[id])
    x = coordinates[id][:amount, 0]
    y = coordinates[id][:amount, 1]
    z = coordinates[id][:amount, 2]

    plot.set_xdata(x)
    plot.set_ydata(y)
    plot.set_3d_properties(z)

    return plot


def plot(li, dr, map_ax, lismall, limed, drsmall, drmed):
    # https://www.galaxysofts.com/new/python-creating-a-real-time-3d-plot/

    litCoor = np.array([np.zeros((len(li[0]), 3)), np.zeros((len(li[1]), 3))], dtype=object)
    amAvail = [0,0]
    for i in range(len(li)):
        for l in range(len(li[i])):
            if not li[i][l].picked:
                litCoor[i][amAvail[i]][0] = li[i][l].x
                litCoor[i][amAvail[i]][1] = li[i][l].y
                litCoor[i][amAvail[i]][2] = li[i][l].z
                amAvail[i] += 1
    # print("small litter: ", amAvail[0], " large litter: ", amAvail[1])

    droCoor = np.array([np.zeros((len(dr[0]), 3)), np.zeros((len(dr[1]), 3))], dtype=object)
    for i in range(len(dr)):
        for j in range(len(dr[i])):
            droCoor[i][j][0] = dr[i][j].X[0]
            droCoor[i][j][1] = dr[i][j].X[1]
            droCoor[i][j][2] = dr[i][j].X[2]

    # for i in range(len(dr)):
    #     for j in range(len(dr[i])):
    #         if len(dr[i][j].r_array) > 0:
    #             x = dr[i][j].r_array[:,0]
    #             y = dr[i][j].r_array[:, 1]
    #             z = np.zeros(len(x))
    #             map_ax.plot3D(x,y,z, color="g", marker=".")
    #             print("test")

    updateplot(lismall, litCoor, 0, amAvail[0])
    updateplot(limed, litCoor, 1, amAvail[1])

    updateplot(drsmall, droCoor, 0)
    updateplot(drmed, droCoor, 1)

    plt.draw()
    plt.show(block=False)
    plt.pause(0.001)

    return amAvail
