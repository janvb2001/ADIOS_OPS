import random
import time
import matplotlib.pyplot as plt

from plotting import *


def simulate(drones, litters, grid, groundstat, simPar, pathpp, map_ax, lip0, lip1, drp0, drp1, litterin, dronein, batlifef=1.5, tracking = False, storeData=False):
    maxvreached = 0
    message = [False, False]
    havebreaked = [False, False]
    ts = [0, 0]

    if storeData:
        sdr0 = open("drone_brush0.txt", 'w')
        sdr1 = open("drone_brush1.txt", 'w')
        bdr0 = open("drone_grabber0.txt", 'w')
        bdr1 = open("drone_grabber1.txt", 'w')
        bdr2 = open("drone_grabber2.txt", 'w')
        bdr3 = open("drone_grabber3.txt", 'w')
        sdr0.write("")
        sdr1.write("")
        bdr0.write("")
        bdr1.write("")
        bdr2.write("")
        bdr3.write("")
        sdr0.close()
        sdr1.close()
        bdr0.close()
        bdr1.close()
        bdr2.close()
        bdr3.close()

    t = 0.
    dt = simPar["dt"]
    tstart = time.time()
    run = True
    while run:
        countloops = 0
        while t < simPar["runspeed"] * (time.time() - tstart) and countloops < simPar["maxplotloops"]:
            breaking = False
            dronesdone = 0
            for drtype in range(len(drones)):
                dcount = 0
                dronetypedone = 0
                for d in drones[drtype]:
                    d.updateDrone(dt, t, litters, pathpp["gridresolution"], groundstat, simPar, grid, litterin["drivingdist"][drtype], dronein, dcount, batlifef, tracking)

                    if abs(d.flyingv) > maxvreached:
                        maxvreached = abs(d.flyingv)
                        # print(maxvreached)
                    if d.state == 6:
                        dronesdone += 1
                        dronetypedone += 1
                if dronetypedone == dronein["amountDrone"][drtype] and not havebreaked[drtype]:
                    breaking = True
                    havebreaked[drtype] = True

                    # print("drtype: ", drtype, "dcount: ", dcount, ", t: ", t, ", x: ", d.x, ', y: ', d.y, ", z: ", d.z)
                    dcount += 1
                if storeData:
                    sdr0 = open("drone_brush0.txt", 'a')
                    sdr1 = open("drone_brush1.txt", 'a')
                    bdr0 = open("drone_grabber0.txt", 'a')
                    bdr1 = open("drone_grabber1.txt", 'a')
                    bdr2 = open("drone_grabber2.txt", 'a')
                    bdr3 = open("drone_grabber3.txt", 'a')
                    for litype in range(len(drones)):
                        i = 0
                        for dr in drones[litype]:
                            #           litter type,        drone id,           t,                  x,                              y,                              z,                              phi,                            theta,                              psi,                    state                   battery
                            txtline = str(litype) + ", " + str(i) + ", " + str(t) + ", " + str(float(dr.X[0][0])) + ", " + str(float(dr.X[1][0])) + ", " + str(float(dr.X[2][0])) + ", " + str(float(dr.X[6][0])) + ", " + str(float(dr.X[7][0])) + ", " + str(float(dr.X[8][0])) + ", " + str(dr.state) + ", " + str(dr.batLife * 100/ (dr.batLifeMax / 0.9)) + "\n"

                            if litype == 0 and i == 0:
                                sdr0.write(txtline)
                            elif litype == 0 and i == 1:
                                sdr1.write(txtline)
                            elif litype == 1 and i == 0:
                                bdr0.write(txtline)
                            elif litype == 1 and i == 1:
                                bdr1.write(txtline)
                            elif litype == 1 and i == 2:
                                bdr2.write(txtline)
                            elif litype == 1 and i == 3:
                                bdr3.write(txtline)
                            i += 1
                    sdr0.close()
                    sdr1.close()
                    bdr0.close()
                    bdr1.close()
                    bdr2.close()
                    bdr3.close()

            if dronesdone == sum(dronein["amountDrone"]) or breaking:
                break


            t += dt
            # print(t)
            countloops += 1

        if simPar["plotOperation"]:
            amount = plot(litters, drones, map_ax, lip0, lip1, drp0, drp1)
        else:
            amount = [0, 0]
            for i in range(len(litters)):
                for l in range(len(litters[i])):
                    if not litters[i][l].picked:
                        amount[i] += 1


        for i in range(len(amount)):
            if not message[i] and amount[i] == 0:
                print("Drone type ", i, "is done at ", t, " seconds")
                message[i] = True
                ts[i] = t

        totalLitter = sum(amount)
        print(totalLitter)
        if totalLitter == 0:
            totDoneDrones = 0
            for i in range(len(drones)):
                for d in drones[i]:
                    if d.X[0] == groundstat["x"] and d.X[1] == groundstat["y"] and d.X[2] == 0:
                        totDoneDrones += 1
            if totDoneDrones == sum(dronein["amountDrone"]):
                run = False
                print("all litter is cleaned")

    print("Time to run simulation: ", time.time() - tstart, " seconds")
    print("All litter is cleaned after ", int(t / 60), " minutes and ", round(t - 60*int(t/60)), "seconds, total: ", t, " seconds")
    # print("Max v reached by drones is: ", round(maxvreached, 2), " m/s")

    if simPar["plotOperation"]:
        # Make sure the plot remains on screen when program is finished
        plt.show(block=True)

    return litters, drones, t, ts


