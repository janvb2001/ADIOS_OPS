from simFunctions import *
import random as rnd
import matplotlib.pyplot as plt
import time

def simulate(simInput):
    # drone_n, litter_n, ground_stat_pos, van_positions, x_size, y_size, plot_driveplan, vanMovement, runspeed, v_drone, dt, v_van
    ground_stat_pos = simInput["ground_stat_pos"]
    van_positions = simInput["van_positions"]
    littercoor = simInput["littercoor"]
    lit_avail = simInput["lit_avail"]

    # Setting up the drone data arrays
    # x_coor, y_coor, end time busy, item traveling to
    drones = []
    # drone_data = [[], [], [], []]
    active_drones = []
    for d in range(simInput["drone_n"]):
        drones.append(Drone(ground_stat_pos[0], ground_stat_pos[1], 0, -1))

        # drone_data[0].append(ground_stat_pos[0])
        # drone_data[1].append(ground_stat_pos[1])
        # drone_data[2].append(0)
        # drone_data[3].append(-1)

        active_drones.append(d)

    print(drones)

    # to run GUI event loop, necessary for animation
    plt.ion()

    d_x = []
    d_y = []
    for d in drones:
        d_x.append(d.x)
        d_y.append(d.y)

    # setting up de figure with how each object is displayed
    figure, ax = plt.subplots(figsize=(10, 8))
    litterplot, = plt.plot(littercoor[0], littercoor[1], 'o', color='black', markersize=4)
    groundplot, = plt.plot(ground_stat_pos[0], ground_stat_pos[1], color='g', marker='s', markersize=10)
    droneplot, = plt.plot(d_x, d_y, 'o', color='b', markersize=6)

    if simInput["plot_driveplan"] and simInput["vanMovement"] == 1:
        checkpoint, = plt.plot(van_positions[0], van_positions[1])

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

                # The drone is done with getting to the van
                if d.t_busy <= t and d.state == -1:

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

                # The drone has reached the litter piece
                elif d.t_busy <= t and d.state >= 0:
                    # The litter is picked up so has no coordinate anymore
                    littercoor[0][d.state] = None
                    littercoor[1][d.state] = None

                    # The drone is no longer on its way to litter
                    d.state = -1

                    # Determine the time needed to reach destination and store
                    t_busy, dnext = new_d_t(d.x, d.y, ground_stat_pos[0], ground_stat_pos[1],
                                            simInput["v_drone"])
                    d.t_busy = t + t_busy


                # If the drone is on its way
                elif d.t_busy > t:
                    # Headed to van
                    if litteri == -1:
                        # The drone is on its way to the van
                        nx, ny, t_busy, dis = on_route(d.x, d.y, ground_stat_pos[0],
                                                       ground_stat_pos[1], simInput["v_drone"], simInput["dt"])
                    # Headed to litter
                    elif litteri >= 0:
                        # The drone is on its way to a litter piece
                        nx, ny, t_busy, dis = on_route(d.x, d.y, littercoor[0][litteri],
                                                       littercoor[1][litteri], simInput["v_drone"], simInput["dt"])

                    # Store data
                    totaldronedist += dis
                    d.t_busy = t + t_busy
                    d.x = nx
                    d.y = ny

            if simInput["vanMovement"] == 1:
                ground_stat_pos[0], ground_stat_pos[1], t_busy, dis = on_route(ground_stat_pos[0], ground_stat_pos[1],
                                                                               van_positions[0][cur_goal],
                                                                               van_positions[1][cur_goal], simInput["v_van"], simInput["dt"])
                lit_avail[1] = recalc_lit_dist(littercoor, lit_avail, ground_stat_pos[0], ground_stat_pos[1])

                if ground_stat_pos[0] == van_positions[0][cur_goal] and ground_stat_pos[1] == van_positions[1][
                    cur_goal]:
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

            t += simInput["dt"]

        d_x = []
        d_y = []
        for d in drones:
            d_x.append(d.x)
            d_y.append(d.y)

        plot_update(d_x, d_y, ground_stat_pos[0], ground_stat_pos[1], littercoor[0], littercoor[1],
                    litterplot, groundplot, droneplot, figure)

    results = dict(totalT = t, totald = totaldronedist)
    return results

