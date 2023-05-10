import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import time
from math import sqrt
import time

# Things to include:
# - Drones should have a delay at the ground station and each litter piece (Which can be deduced from req.)
# - Drones should not get too close to each other
# - Simulate the reasonable worst-case scenario
#     - van position is not ideal
#     - Garbage position is not ideal
# - Include different litter types in the program
# - Include different drone types in the program
# - Include obstacles
# - Include reconnaisance drone
# - Wind

# Done:
# - Include the possibility for the van to drive

# inputs
litter_n = 1000
drone_n = 10
v_drone = 8    # m/s
v_van = 2       # m/s
vanMovement = 1         # 0: Stationary van, 1: van squares around
plot_driveplan = True

runspeed = 10          # Factor wrt real-time

dt = 0.1  # s

# sizes of area in m
totalArea = 10000       # m^2
x_size = sqrt(totalArea)
y_size = sqrt(totalArea)

# starting position of ground station

# Van starting position
if vanMovement == 0:
    #Starts in middle
    ground_stat_pos = [int(x_size/2), int(y_size/2)]
elif vanMovement == 1:
    x_clearance = 1/10 * x_size
    y_clearance = 1/10 * y_size

    ly = y_size - y_clearance
    lx = x_size - x_clearance

    ground_stat_pos = [int(x_clearance), int(y_clearance)]
    van_positions = [[ground_stat_pos[0], ground_stat_pos[0]],
                     [ground_stat_pos[1], ground_stat_pos[1] + ly - y_clearance]]

    dir = 2             # 1: up, 2: right, 3: down, 4: left
    cont = True
    while cont:
        if dir == 1:
            ly = ly - y_clearance
            van_positions[0].append(van_positions[0][-1])
            van_positions[1].append(van_positions[1][-1] + ly)
        elif dir == 2:
            lx = lx - x_clearance
            van_positions[0].append(van_positions[0][-1] + lx)
            van_positions[1].append(van_positions[1][-1])
        elif dir == 3:
            ly = ly - y_clearance
            van_positions[0].append(van_positions[0][-1])
            van_positions[1].append(van_positions[1][-1] - ly)
        elif dir == 4:
            lx = lx - x_clearance
            van_positions[0].append(van_positions[0][-1] - lx)
            van_positions[1].append(van_positions[1][-1])
            dir = 0

        if lx < 0 or ly < 0:
            cont = False
        dir += 1

# function to determine distance between 2 points
def dist(x1, x2, y1, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

# Determine the new coordinate from current coordinate, target and speed
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

def new_d_t(curx, cury, finx, finy, v):
    dn = dist(curx, finx, cury, finy)
    t_b = dn / v
    return t_b, dn

def on_route(curx, cury, goalx, goaly, v, dt):
    newx, newy = newcoor(goalx, goaly, curx, cury, v, dt)

    # recalculate the time needed to reach destination and store
    t_b, dn = new_d_t(curx, cury, goalx, goaly, v)

    dd = dist(curx, newx, cury, newy)

    return newx, newy, t_b, dd
def van_reached(lit_a):

    # Check whether there is still litter left to be taken
    if len(lit_a[0]) > 0:
        # Choose a litter item
            # Randomly
        # nextitemi = rnd.randint(0, len(lit_a[0]) - 1)
        # nextitem = lit_a[0][nextitemi]

            # Closest to van
        mindis = min(lit_a[1])
        nexti = lit_a[1].index(mindis)
        nextitem = lit_a[0][nexti]

        # Remove the chosen litter item from the available list
        liti = lit_a[0].index(nextitem)
        lit_a[0].pop(liti)
        lit_a[1].pop(liti)

        # Calculate the time needed to get to the destination and store
        t_busy, dnext = new_d_t(drone_data[0][d], drone_data[1][d], littercoor[0][nextitem],
                                littercoor[1][nextitem], v_drone)

    else:
        # if there is no litter left, the drone is done
        nextitem = -2
        t_busy = None

    return nextitem, t_busy, lit_a

def recalc_lit_dist(lit_coor, lit_a, gs_x, gs_y):
    distances = []

    for li in range(len(lit_a[0])):
        di = dist(gs_x, lit_coor[0][lit_a[0][li]], gs_y, lit_coor[1][lit_a[0][li]])
        distances.append(di)

    return distances

def plot_update(newxdrone, newydrone, newxvan, newyvan, newxlit, newylit):
    # updating the plot
    litterplot.set_xdata(newxlit)
    litterplot.set_ydata(newylit)

    groundplot.set_xdata(newxvan)
    groundplot.set_ydata(newyvan)

    droneplot.set_xdata(newxdrone)
    droneplot.set_ydata(newydrone)

    figure.canvas.draw()
    figure.canvas.flush_events()



# Setting up the drone data arrays
# x_coor, y_coor, end time busy, item traveling to
drone_data = [[], [], [], []]
active_drones = []
for d in range(drone_n):
    drone_data[0].append(ground_stat_pos[0])
    drone_data[1].append(ground_stat_pos[1])
    drone_data[2].append(0)
    drone_data[3].append(-1)

    active_drones.append(d)

# Setting up the litter data arrays
lit_avail = [[],[]]
littercoor = [[],[]]
for i in range(litter_n):
    lit_avail[0].append(i)

    xlit = rnd.randint(0, x_size)
    ylit = rnd.randint(0, y_size)
    littercoor[0].append(xlit)
    littercoor[1].append(ylit)

    d_van = dist(xlit, ground_stat_pos[0], ylit, ground_stat_pos[1])
    lit_avail[1].append(d_van)

# to run GUI event loop, necessary for animation
plt.ion()

# setting up de figure with how each object is displayed
figure, ax = plt.subplots(figsize=(10, 8))
litterplot, = plt.plot(littercoor[0], littercoor[1], 'o', color='black', markersize = 4)
groundplot, = plt.plot(ground_stat_pos[0], ground_stat_pos[1], color='g', marker='s', markersize=10)
droneplot, = plt.plot(drone_data[0], drone_data[1], 'o', color='b', markersize = 6)

if plot_driveplan and vanMovement == 1:
    checkpoint, = plt.plot(van_positions[0], van_positions[1])

startTime = time.time()

run = True
t = 0
cur_goal = 1
totaldronedist = 0
while run:
    while t < runspeed * (time.time()-startTime):
        # loop over every drone
        for d in active_drones:
            litteri = drone_data[3][d]

            # The drone is done with getting to the van
            if drone_data[2][d] <= t and drone_data[3][d] == -1:

                #Selection of next item
                nextitem, t_busy, lit_avail = van_reached(lit_avail)
                drone_data[3][d] = nextitem

                # If there is no more litter, remove the drone from active drones
                if nextitem == -2:
                    dronei = active_drones.index(d)
                    active_drones.pop(dronei)

                    drone_data[0][d] = None
                    drone_data[1][d] = None
                else:
                    drone_data[2][d] = t + t_busy

            # The drone has reached the litter piece
            elif drone_data[2][d] <= t and drone_data[3][d] >= 0:
                # The litter is picked up so has no coordinate anymore
                littercoor[0][drone_data[3][d]] = None
                littercoor[1][drone_data[3][d]] = None

                # The drone is no longer on its way to litter
                drone_data[3][d] = -1

                # Determine the time needed to reach destination and store
                t_busy, dnext = new_d_t(drone_data[0][d], drone_data[1][d], ground_stat_pos[0], ground_stat_pos[1],
                                        v_drone)
                drone_data[2][d] = t + t_busy


            # If the drone is on its way
            elif drone_data[2][d] > t:
                # Headed to van
                if litteri == -1:
                    # The drone is on its way to the van
                    nx, ny, t_busy, dis = on_route(drone_data[0][d], drone_data[1][d], ground_stat_pos[0],
                                              ground_stat_pos[1], v_drone, dt)
                # Headed to litter
                elif litteri >= 0:
                    # The drone is on its way to a litter piece
                    nx, ny, t_busy, dis = on_route(drone_data[0][d], drone_data[1][d], littercoor[0][litteri],
                                              littercoor[1][litteri], v_drone, dt)

                # Store data
                totaldronedist += dis
                drone_data[2][d] = t + t_busy
                drone_data[0][d] = nx
                drone_data[1][d] = ny

        if vanMovement == 1:
            ground_stat_pos[0], ground_stat_pos[1], t_busy, dis = on_route(ground_stat_pos[0], ground_stat_pos[1], van_positions[0][cur_goal], van_positions[1][cur_goal], v_van, dt)
            lit_avail[1] = recalc_lit_dist(littercoor, lit_avail, ground_stat_pos[0], ground_stat_pos[1])


            if ground_stat_pos[0] == van_positions[0][cur_goal] and ground_stat_pos[1] == van_positions[1][cur_goal]:
                if cur_goal < len(van_positions[0]) - 1:
                    cur_goal += 1
                else:
                    cur_goal = 0

        # check whether simulation is done
        if len(active_drones) == 0:
            time.sleep(2)
            run = False
            print("Total drone distance is: " + str(totaldronedist) + " m")
            print("End time is: " + str(t) + " s")
            break

        t += dt

    plot_update(drone_data[0], drone_data[1], ground_stat_pos[0], ground_stat_pos[1], littercoor[0], littercoor[1])


