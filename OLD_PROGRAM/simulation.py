from simFunctions import *
import random as rnd
import matplotlib.pyplot as plt
import time
from numba import jit

def simulate(simInput):
    # drone_n, litter_n, ground_stat_pos, van_positions, x_size, y_size, plot_driveplan, vanMovement, runspeed, v_drone, dt, v_van
    van_positions = simInput["van_positions"]
    littercoor = simInput["littercoor"]
    lit_avail = simInput["lit_avail"]
    drones = simInput["drones"]
    active_drones = simInput["active_drones"]
    van = simInput["van"]
    ddrones = simInput["ddrones"]

    if simInput["plotProcess"]:

        # to run GUI event loop, necessary for animation
        plt.ion()

        d_x = []
        d_y = []
        for d in drones:
            d_x.append(d.x)
            d_y.append(d.y)
        dd_x = []
        dd_y = []
        for dd in range(len(ddrones)):
            dd_x.append(ddrones[dd].x)
            dd_y.append(ddrones[dd].y)
        # fig, ax = plt.subplots(figsize=(8,6))
        # plt.title("Litter Distribution")
        # ax.plot(littercoor[0], littercoor[1], 'o', color='black', markersize=4)
        # ax.plot(dd_x, dd_y, color='g', marker='s', markersize=10)
        # ax.plot(d_x, d_y, 'o', color='b', markersize=6)
        # ax.plot(van_positions[0], van_positions[1])
        # ax.plot(simInput["van"].x, simInput["van"].y, 'o', color="red", markersize=10)
        # fig.subplots_adjust(right=0.75)
        # ax.legend(["Litter", "Ground drone", "Drone", "Ground Drone Path", "Van Position"], loc="center left", bbox_to_anchor = (0.75, 0.5), bbox_transform = fig.transFigure)
        # plt.show()


        # setting up de figure with how each object is displayed
        figure, ax = plt.subplots(figsize=(10, 8))
        litterplot, = plt.plot(littercoor[0], littercoor[1], 'o', color='black', markersize=4)
        groundplot, = plt.plot(dd_x, dd_y, color='g', marker='s', markersize=10)
        droneplot, = plt.plot(d_x, d_y, 'o', color='b', markersize=6)

        if simInput["plot_driveplan"] and simInput["vanMovement"] >= 1:
            checkpoint, = plt.plot(van_positions[0], van_positions[1])
        if simInput["vanMovement"] >= 1:
            vanplt, = plt.plot(simInput["van"].x, simInput["van"].y, 'o', color = "red", markersize = 10)

    startTime = time.time()

    run = True
    t = 0
    cur_goal = 1
    totaldronedist = 0
    while run:
        while t < simInput["runspeed"] * (time.time() - startTime):
            # loop over every drone
            for ad in active_drones:
                d = drones[ad]
                litteri = d.state

                d.charge -= simInput["dt"]

                # The drone is done with getting to the van
                if d.t_busy <= t and d.state == -1:
                    totaldronedist += dist(d.x, ddrones[d.ddronei].x, d.y, ddrones[d.ddronei].y)
                    #print(dist(d.x, ddrones[d.ddronei].x, d.y, ddrones[d.ddronei].y))
                    if d.wait_t_left <= 0 and d.charge > simInput["charge_start"]:
                        # Selection of next item
                        nextitem, t_busy, lit_avail = van_reached(lit_avail, drones, littercoor, d, simInput["v_drone"])
                        d.state = nextitem

                        # If there is no more litter, remove the drone from active drones
                        if nextitem == -2:
                            dronei = active_drones.index(ad)
                            active_drones.pop(dronei)

                            d.x = None
                            d.y = None
                        else:
                            d.t_busy = t + t_busy
                            d.wait_t_left = d.t_wait_lit
                    elif d.wait_t_left <= 0 and d.charge <= simInput["charge_start"]:
                        d.state = -3
                        t_b, dd = new_d_t(d.x, d.y, van.x, van.y, d.v)
                        d.t_busy = t + t_b
                        ddrones[d.ddronei].v -= ddrones[d.ddronei].maxv / ddrones[d.ddronei].n_drones

                    else:
                        d.wait_t_left -= simInput["dt"]
                        d.x = ddrones[d.ddronei].x
                        d.y = ddrones[d.ddronei].y

                # The drone has reached the litter piece
                elif d.t_busy <= t and d.state >= 0:
                    totaldronedist += dist(d.x, littercoor[0][d.state], d.y, littercoor[1][d.state])
                    #print(dist(d.x, littercoor[0][d.state], d.y, littercoor[1][d.state]))
                    if d.wait_t_left <= 0:
                        # The litter is picked up so has no coordinate anymore
                        littercoor[0][d.state] = None
                        littercoor[1][d.state] = None

                        # The drone is no longer on its way to litter
                        d.state = -1

                        # Determine the time needed to reach destination and store
                        t_busy, dnext = new_d_t(d.x, d.y, ddrones[d.ddronei].x, ddrones[d.ddronei].y,
                                                simInput["v_drone"])
                        d.t_busy = t + t_busy
                        d.wait_t_left = d.t_wait_ground
                    else:
                        d.wait_t_left -= simInput["dt"]
                elif d.t_busy <= t and d.state == -3:
                    totaldronedist += dist(d.x, van.x, d.y, van.y)
                    #print(dist(d.x, van.x, d.y, van.y))
                    if d.charge > d.charge0:
                        d.state = -1
                        t_b, dnext = new_d_t(d.x, d.y, ddrones[d.ddronei].x, ddrones[d.ddronei].y, d.v)
                        ddrones[d.ddronei].v += ddrones[d.ddronei].maxv / ddrones[d.ddronei].n_drones
                        d.t_busy = t + t_b
                    else:
                        d.charge += d.charge0 * simInput["dt"] / d.rechargetime

                # If the drone is on its way
                elif d.t_busy > t:
                    # Headed to van
                    if litteri == -1:
                        # The drone is on its way to the van
                        nx, ny, t_busy, dis = on_route(d.x, d.y, ddrones[d.ddronei].x,
                                                       ddrones[d.ddronei].y, simInput["v_drone"], simInput["dt"])
                    # Headed to litter
                    elif litteri >= 0:
                        # The drone is on its way to a litter piece
                        nx, ny, t_busy, dis = on_route(d.x, d.y, littercoor[0][litteri],
                                                       littercoor[1][litteri], simInput["v_drone"], simInput["dt"])
                    elif litteri == -3:
                        nx, ny, t_busy, dis = on_route(d.x, d.y, van.x, van.y, d.v, simInput['dt'])

                    # Store data
                    totaldronedist += dis
                    d.t_busy = t + t_busy
                    d.x = nx
                    d.y = ny

            if simInput["vanMovement"] >= 1:
                for dd in range(len(ddrones)):
                    if ddrones[dd].v > 0:
                        ddrones[dd].x, ddrones[dd].y, t_busy, dis = on_route(ddrones[dd].x, ddrones[dd].y,
                                                                                       ddrones[dd].waypoints[0][ddrones[dd].cur_goal],
                                                                                       ddrones[dd].waypoints[1][ddrones[dd].cur_goal], ddrones[dd].v, simInput["dt"])
                    lit_avail[1] = recalc_lit_dist(littercoor, lit_avail, ddrones[d.ddronei].x, ddrones[d.ddronei].y)

                    if ddrones[d.ddronei].x == ddrones[dd].waypoints[0][ddrones[dd].cur_goal] and ddrones[d.ddronei].y == ddrones[dd].waypoints[1][ddrones[dd].cur_goal]:
                        if ddrones[dd].cur_goal < len(ddrones[dd].waypoints[0]) - 1:
                            ddrones[dd].cur_goal += 1
                        else:
                            # ddrones[dd].cur_goal = 0
                            None

            # check whether simulation is done
            if len(active_drones) == 0:
                time.sleep(2)
                run = False
                break

            t += simInput["dt"]



        if simInput["plotProcess"]:
            d_x = []
            d_y = []
            for d in drones:
                d_x.append(d.x)
                d_y.append(d.y)
            dd_x = []
            dd_y = []
            for dd in range(len(ddrones)):
                dd_x.append(ddrones[dd].x)
                dd_y.append(ddrones[dd].y)

            plot_update(d_x, d_y, dd_x, dd_y, littercoor[0], littercoor[1],
                        litterplot, groundplot, droneplot, figure)

    results = dict(totalT = t, totald = totaldronedist)
    return results
# test