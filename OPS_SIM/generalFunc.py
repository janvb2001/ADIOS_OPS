from math import sqrt
import numpy as np

def dist2d(x1, x2, y1, y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

def dist3d(x1, x2, y1, y2, z1, z2):
    return sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

def indicesSquareCorners(square, gap, length, width, grid):
    # rowsx = width // gap
    # rowsy = length // gap

    ind = [[-1,-1],[-1,-1]]
    for coor in square:
        y, x = coor
        row = y // gap
        col = x // gap

        if row > ind[0][1] or ind[0][1] == -1:
            ind[0][1] = row
        if row < ind[0][0] or ind[0][0] == -1:
            ind[0][0] = row
        if col > ind[1][1] or ind[1][1] == -1:
            ind[1][1] = col
        if col < ind[1][0] or ind[1][0] == -1:
            ind[1][0] = col

    for i in range(ind[0][0],ind[0][1]):
        for j in range(ind[1][0],ind[1][1]):
            grid[i][j].make_barrier()



