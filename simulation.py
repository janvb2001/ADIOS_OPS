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
    drone_data = [[], [], [], []]
    active_drones = []
    for d in range(simInput["drone_n"]):
        drone_data[0].append(ground_stat_pos[0])
        drone_data[1].append(ground_stat_pos[1])
        drone_data[2].append(0)
        drone_data[3].append(-1)

        active_drones.append(d)



    # to run GUI event loop, necessary for animation
    plt.ion()

    # setting up de figure with how each object is displayed
    figure, ax = plt.subplots(figsize=(10, 8))
    litterplot, = plt.plot(littercoor[0], littercoor[1], 'o', color='black', markersize=4)
    groundplot, = plt.plot(ground_stat_pos[0], ground_stat_pos[1], color='g', marker='s', markersize=10)
    droneplot, = plt.plot(drone_data[0], drone_data[1], 'o', color='b', markersize=6)

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
            for d in active_drones:
                litteri = drone_data[3][d]

                # The drone is done with getting to the van
                if drone_data[2][d] <= t and drone_data[3][d] == -1:

                    # Selection of next item
                    nextitem, t_busy, lit_avail = van_reached(lit_avail, drone_data, littercoor, d, simInput["v_drone"])
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
                                            simInput["v_drone"])
                    drone_data[2][d] = t + t_busy


                # If the drone is on its way
                elif drone_data[2][d] > t:
                    # Headed to van
                    if litteri == -1:
                        # The drone is on its way to the van
                        nx, ny, t_busy, dis = on_route(drone_data[0][d], drone_data[1][d], ground_stat_pos[0],
                                                       ground_stat_pos[1], simInput["v_drone"], simInput["dt"])
                    # Headed to litter
                    elif litteri >= 0:
                        # The drone is on its way to a litter piece
                        nx, ny, t_busy, dis = on_route(drone_data[0][d], drone_data[1][d], littercoor[0][litteri],
                                                       littercoor[1][litteri], simInput["v_drone"], simInput["dt"])

                    # Store data
                    totaldronedist += dis
                    drone_data[2][d] = t + t_busy
                    drone_data[0][d] = nx
                    drone_data[1][d] = ny

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

        plot_update(drone_data[0], drone_data[1], ground_stat_pos[0], ground_stat_pos[1], littercoor[0], littercoor[1],
                    litterplot, groundplot, droneplot, figure)

    results = dict(totalT = t, totald = totaldronedist)
    return results

