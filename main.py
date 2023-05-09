import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import time
from math import sqrt


#inputs
litter_n = 100
drone_n = 10
v_drone = 20 # m/s

dt = 1

# coordinates in m
x_size = 1000
y_size = 1000

#starting position of ground station
ground_stat_pos = [int(x_size/2), int(y_size/2)]


#function to determine distance between 2 points
def dist(x1, x2, y1, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

#Determine the new coordinate from current coordinate, target and speed
def newcoor(finx, finy, curx, cury, v, dt):
    dcur = dist(curx, finx, cury, finy)

    d_traveled = v * dt

    if d_traveled > dcur:
        return finx, finy
    else:
        fracd = d_traveled / dcur
        newx = curx + (finx - curx)*fracd
        newy = cury + (finy - cury)*fracd

        return newx, newy

#Setting up the drone data arrays
# x_coor, y_coor, end time busy, item traveling to
drone_data = [[], [], [], []]
for d in range(drone_n):
    drone_data[0].append(ground_stat_pos[0])
    drone_data[1].append(ground_stat_pos[1])
    drone_data[2].append(0)
    drone_data[3].append(0)

# Setting up the litter data arrays
lit_avail = []
litterdata = []
littercoor = [[],[]]
for i in range(litter_n):
    lit_avail.append(i)
    litterdata.append([])
    littercoor[0].append(rnd.randint(0,x_size))
    littercoor[1].append(rnd.randint(0, y_size))

#to run GUI event loop, necessary for animation
plt.ion()

#setting up de figure with how each object is displayed
figure, ax = plt.subplots(figsize=(10, 8))
litterplot, = plt.plot(littercoor[0], littercoor[1], 'o', color='black', markersize = 4)
groundplot, = plt.plot(ground_stat_pos[0], ground_stat_pos[1], color='g', marker='s', markersize=10)
droneplot, = plt.plot(drone_data[0], drone_data[1], 'o', color='b', markersize = 6)

#variable to keep track of how many drones are done
dronesDone = 0

run = True
t = 0
while run:

    #loop over every drone
    for d in range(drone_n):
        #check whether the drone is not done
        if drone_data[3][d] != -2:
            #check whether a drone has reached its destination
            if drone_data[2][d] <= t:
                #Check whether a drone needs a new litter target or needs to return to ground station
                if drone_data[3][d] == -1 or t==0:
                    #Check whether there is still litter left to be taken
                    if len(lit_avail)>0:
                        #Choose a litter item
                        nextitemi = rnd.randint(0,len(lit_avail)-1)
                        nextitem = lit_avail[nextitemi]

                        #Remove the chosen litter item from the available list
                        liti = lit_avail.index(nextitem)
                        lit_avail.pop(liti)
                        drone_data[3][d] = nextitem

                        #Calculate the time needed to get to the destination and store
                        dnext = dist(drone_data[0][d], littercoor[0][nextitem], drone_data[1][d], littercoor[1][nextitem])
                        t_busy = dnext/v_drone
                        drone_data[2][d] = t + t_busy
                    else:
                        #if there is no litter left, the drone is done
                        drone_data[3][d] = -2
                        dronesDone += 1

                else:
                    #The litter is picked up so has no coordinate anymore
                    littercoor[0][drone_data[3][d]] = None
                    littercoor[1][drone_data[3][d]] = None

                    #The drone is no longer on its way to litter
                    drone_data[3][d] = -1

                    #Calculate and store the distance and time needed to get to the ground station
                    dnext = dist(drone_data[0][d], ground_stat_pos[0], drone_data[1][d], ground_stat_pos[1])
                    t_busy = dnext / v_drone
                    drone_data[2][d] = t + t_busy
            else:
                # The drone continues further in the direction of its destination.
                litteri = drone_data[3][d]
                #Continue in the direction of the van
                if litteri == -1:
                    nx, ny = newcoor(ground_stat_pos[0], ground_stat_pos[1], drone_data[0][d], drone_data[1][d],
                                     v_drone, dt)

                    dnext = dist(drone_data[0][d], ground_stat_pos[0], drone_data[1][d], ground_stat_pos[1])
                    t_busy = dnext / v_drone
                    drone_data[2][d] = t + t_busy
                #Continue in the direction of the litter
                else:
                    nx, ny = newcoor(littercoor[0][litteri], littercoor[1][litteri], drone_data[0][d], drone_data[1][d], v_drone, dt)

                    dnext = dist(drone_data[0][d], littercoor[0][drone_data[3][d]], drone_data[1][d], littercoor[1][drone_data[3][d]])
                    t_busy = dnext / v_drone
                    drone_data[2][d] = t + t_busy

                #The new coordinates of the drone is the calculated coordinates
                drone_data[0][d] = nx
                drone_data[1][d] = ny


    # updating the plot
    litterplot.set_xdata(littercoor[0])
    litterplot.set_ydata(littercoor[1])

    droneplot.set_xdata(drone_data[0])
    droneplot.set_ydata(drone_data[1])

    figure.canvas.draw()
    figure.canvas.flush_events()

    if dronesDone == drone_n:
        time.sleep(3)
        run = False
    #time.sleep(0.05)
    t += dt
