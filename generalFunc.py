from math import sqrt
from numba import jit
# function to determine distance between 2 points
@jit
def dist(x1, x2, y1, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

# Determine the new coordinate from current coordinate, target and speed
@jit
def newcoor(finx, finy, curx, cury, v, dt):
    # distance to destination
    dcur = dist(curx, finx, cury, finy)

    # distance traveled in this timestep
    d_traveled = v * dt

    # Destination is reached
    if d_traveled > dcur:
        return finx, finy
    # destination is not reached
    else:
        # fraction of total distance that is traveled in this timestep
        fracd = d_traveled / dcur
        # multiply this fraction with total distance to travel and find new coordinates of the drone
        newx = curx + (finx - curx)*fracd
        newy = cury + (finy - cury)*fracd

        return newx, newy

@jit
def new_d_t(curx, cury, finx, finy, v):
    dn = dist(curx, finx, cury, finy)
    t_b = dn / v
    return t_b, dn

@jit
def on_route(curx, cury, goalx, goaly, v, dt):
    newx, newy = newcoor(goalx, goaly, curx, cury, v, dt)

    # recalculate the time needed to reach destination and store
    t_b, dn = new_d_t(curx, cury, goalx, goaly, v)

    dd = dist(curx, newx, cury, newy)

    return newx, newy, t_b, dd