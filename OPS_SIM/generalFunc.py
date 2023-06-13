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

def checkLineOnGrid(grid, start, end, res):
    # Return whether line crosses grid barrier
    x1 = start[0]
    x2 = end[0]
    y1 = start[1]
    y2 = end[1]

    if x1 == x2:
        # Vertical line
        None
    elif y1 == y2:
        # Horizontal line
        None
    else:
        # Diagonal line
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

        xs = np.arange(x1, x2, res/10)
        ys = a * xs + b

        rows = ys // res
        cols = xs // res

        rows = rows.astype(int)
        cols = cols.astype(int)

        barCrossed = False
        for i in range(len(rows)):
            if rows[i] >= len(grid):
                rows[i] -= 1
            if cols[i] >= len(grid[rows[i]]):
                cols[i] -= 1

            if grid[rows[i]][cols[i]].color == (0, 0, 0):
                barCrossed = True
                break

        return barCrossed






