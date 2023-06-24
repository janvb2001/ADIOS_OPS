
import time
import random

import numpy as np

from inputs import *
from setup import *
from simulation import *

from matplotlib import pyplot as plt, patches
from matplotlib.ticker import MaxNLocator

def dtVar(dts):
    times = []

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    for i in range(len(dts)):
        print("dt: ", dts[i])
        simPar["dt"] = dts[i]
        # setup the ararys to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1,
                                  drp0, drp1,
                                  litterInput, droneInput)
        times.append(tdone/60)

    plt.plot(dts, times)
    plt.xlabel("dt")
    plt.ylabel("Operation time [min]")
    plt.title("Simulation result dependency on dt")
    plt.xscale('log')

    plt.show()

def drVar(drn):
    times = []
    iss = []

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    for i in range(drn[0], drn[1]):
        print("drn: ", i)
        droneInput["amountDrone"] = np.array([i, i])
        # setup the ararys to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1,
                                  drp0, drp1,
                                  litterInput, droneInput)
        iss.append(i)
        times.append(ts)

    # times = np.array(times)
    # times = times / 60
    # mintimes = [min(times[:,0]), min(times[:,1])]
    # maxtimes = [max(times[:,0]), max(times[:,1])]
    # margin = [0.1 * (maxtimes[0] - mintimes[0]), 0.1 * (maxtimes[1] - mintimes[1])]
    # mintimes[0] = mintimes[0] - margin[0]
    # maxtimes[0] = maxtimes[0] + margin[0]
    # mintimes[1] = mintimes[1] - margin[1]
    # maxtimes[1] = maxtimes[1] + margin[1]
    #
    # fig, axs = plt.subplots(1, 2)
    # fig.suptitle('Relation Number of Drones and Operation Time')
    # rectangler = patches.Rectangle((0, 0), 20, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    # rectangleg = patches.Rectangle((0, 60), 20, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    # axs[0].add_patch(rectangler)
    # axs[0].add_patch(rectangleg)
    # axs[0].set_title("Small Litter Drone")
    # axs[0].set(xlabel='Number of Drones', ylabel='Operation time [min]')
    # axs[0].set_xlim(0,drn[1])
    # axs[0].set_ylim(mintimes[0], maxtimes[0])
    # axs[0].plot(iss, times[:, 0], marker=".")
    #
    # rectangler = patches.Rectangle((0, 0), 20, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    # rectangleg = patches.Rectangle((0, 60), 20, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    # axs[1].add_patch(rectangler)
    # axs[1].add_patch(rectangleg)
    # axs[1].set_title("Big Litter Drone")
    # axs[1].set(xlabel='Number of Drones', ylabel='Operation time [min]')
    # axs[1].set_xlim(0, drn[1])
    # axs[1].set_ylim(mintimes[1], maxtimes[1])
    # axs[1].plot(iss, times[:, 1], marker=".")
    #
    # plt.show()

    times = np.array(times)
    times = times / 60
    mintimes = np.min(times)
    maxtimes = np.max(times)
    margin = 0.1 * (maxtimes - mintimes)
    mintimes -= margin
    maxtimes += margin

    if mintimes < 0:
        mintimes = 0

    fig, axs = plt.subplots()
    # fig.suptitle('Relation Litter Ratio and Operation Time')
    rectangler = patches.Rectangle((0, 0), 150, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    rectangleg = patches.Rectangle((0, 60), 150, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    axs.add_patch(rectangler)
    axs.add_patch(rectangleg)
    axs.set_title("Relation Number of Drones and Operation Time")
    axs.set(xlabel='Number of Drones', ylabel='Operation time [min]')
    axs.set_xlim(0, drn[1])
    axs.set_ylim(mintimes, maxtimes)
    axs.plot(iss, times[:, 0], label="Small", marker=".")
    axs.plot(iss, times[:, 1], label="Large", marker=".")
    axs.legend(title="Drone type:")

    plt.show()


def litterVar(step):
    times = []
    iss = []
    iss2 = []

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    for i in range(step,100,step):
        print("small litter percentage: ", i)
        litterInput["littern"] = np.array([i * 10, 1000 - i * 10])
        # setup the arrays to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1,
                                  drp0, drp1,
                                  litterInput, droneInput)
        iss.append(i)
        iss2.append(100-i)
        times.append(ts)

    times = np.array(times)
    times = times / 60
    mintimes = np.min(times)
    maxtimes = np.max(times)
    margin = 0.1 * (maxtimes - mintimes)
    mintimes -= margin
    maxtimes += margin

    if mintimes < 0:
        mintimes = 0

    fig, axs = plt.subplots()
    # fig.suptitle('Relation Litter Ratio and Operation Time')
    rectangler = patches.Rectangle((0, 0), 150, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    rectangleg = patches.Rectangle((0, 60), 150, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    axs.add_patch(rectangler)
    axs.add_patch(rectangleg)
    axs.set_title("Relation Litter Ratio and Operation Time")
    axs.set(xlabel='Percentage of Small litter', ylabel='Operation time [min]')
    axs.set_xlim(0, 100)
    axs.set_ylim(mintimes, maxtimes)
    axs.plot(iss, times[:, 0], label="Small")
    axs.plot(iss, times[:, 1], label="Large")
    axs.legend(title="Drone type:")

    plt.show()

    # rectangler = patches.Rectangle((0, 0), 150, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    # rectangleg = patches.Rectangle((0, 60), 150, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    # axs[1].add_patch(rectangler)
    # axs[1].add_patch(rectangleg)
    # axs[1].set_title("Big Litter Drone")
    # axs[1].set(xlabel='Percentage of Small litter', ylabel='Operation time [min]')
    # axs[1].set_xlim(0, 100)
    # axs[1].set_ylim(mintimes[1], maxtimes[1])
    #
    # axs[1].invert_xaxis()



def seedVar(n):
    times = []
    iss = []

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    for i in range(n):
        print("n: ", i)
        litterInput["seed"] = i
        # setup the arrays to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1,
                                  drp0, drp1,
                                  litterInput, droneInput)
        iss.append(i+1)
        times.append(ts)

    times = np.array(times)
    times = times / 60
    mintimes = [min(times[:,0]), min(times[:,1])]
    maxtimes = [max(times[:,0]), max(times[:,1])]
    margin = [0.1 * (maxtimes[0] - mintimes[0]), 0.1 * (maxtimes[1] - mintimes[1])]
    mintimes[0] = mintimes[0] - margin[0]
    maxtimes[0] = maxtimes[0] + margin[0]
    mintimes[1] = mintimes[1] - margin[1]
    maxtimes[1] = maxtimes[1] + margin[1]

    fig, axs = plt.subplots()
    # # fig.suptitle('Relation Litter Ratio and Operation Time')
    # rectangler = patches.Rectangle((0, 0), 150, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    # rectangleg = patches.Rectangle((0, 60), 150, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    # axs.add_patch(rectangler)
    # axs.add_patch(rectangleg)
    axs.set_title("Dependence of Operating Time to Litter Distribution")
    axs.set_xlabel('Simulation run')
    axs.set_ylabel('Operation time [min]')
    axs.set_xlim(0, n+1)
    axs.set_ylim(mintimes[0], maxtimes[0])
    axs.tick_params(axis="y", labelcolor="b")
    line1 = axs.plot(iss, times[:, 0], label="Small", marker=".")

    axs.xaxis.set_major_locator(MaxNLocator(integer=True))
    axs2 = axs.twinx()

    line2 = axs2.plot(iss, times[:, 1], label="Large", color="orange", marker=".")
    axs2.set_ylim(mintimes[1], maxtimes[1])
    axs2.tick_params(axis="y", labelcolor="orange")
    axs2.set_xlabel('Simulation run')
    axs2.set_ylabel('Operation time [min]')

    lns = line1 + line2
    labs = [l.get_label() for l in lns]

    plt.legend(lns, labs, title="Drone type: ")

    plt.show()

def gsVar(gspos):
    times = []
    iss = []

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    for i in range(len(gspos)):
        print("gs: ", gspos[i])
        groundStatInput["x"] = gspos[i][0]
        groundStatInput["y"] = gspos[i][1]
        # setup the ararys to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1,
                                  drp0, drp1,
                                  litterInput, droneInput)
        iss.append(i + 1)
        times.append(ts)

    times = np.array(times)
    times = times / 60
    mintimes = np.min(times)
    maxtimes = np.max(times)
    margin = 0.1 * (maxtimes - mintimes)
    mintimes -= margin
    maxtimes += margin

    if mintimes < 0:
        mintimes = 0

    fig, axs = plt.subplots()
    # fig.suptitle('Relation Litter Ratio and Operation Time')
    rectangler = patches.Rectangle((0, 0), 150, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    rectangleg = patches.Rectangle((0, 60), 150, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    axs.add_patch(rectangler)
    axs.add_patch(rectangleg)
    axs.set_title("Dependence of operation time on ground station location")
    axs.set(xlabel='Ground station location', ylabel='Operation time [min]')
    axs.set_xlim(0, len(gspos) + 1)
    axs.set_ylim(mintimes, maxtimes)
    axs.xaxis.set_major_locator(MaxNLocator(integer=True))

    for i in range(len(iss)):
        if times[i][1] > times[i][0]:
            large, = axs.bar(iss[i], times[i][1], width=0.5, color="tab:orange")
            small, = axs.bar(iss[i], times[i][0], width=0.5, color="tab:blue")
        else:
            small, = axs.bar(iss[i], times[i][0], width=0.5, color="tab:blue")
            large, = axs.bar(iss[i], times[i][1], width=0.5, color="tab:orange")

    axs.plot(iss, times[:, 0], label="Small", linewidth=0)
    axs.plot(iss, times[:, 1], label="Large", linewidth=0)

    axs.legend([small, large], ["Small","Large"], title="Drone type:")

    plt.show()

def batLife(factors):
    dronesdata = []
    iss = []
    maxtime = 0

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    for i in range(len(factors)):
        print("factor: ", factors[i])

        # setup the ararys to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax,
                                              lip0, lip1,
                                              drp0, drp1,
                                              litterInput, droneInput, batlifef=factors[i], tracking=True)
        iss.append(i + 1)
        dronesdata.append(drones)

        if tdone > maxtime:
            maxtime = tdone

    line0 = None
    line1 = None
    line2 = None
    line3 = None

    fig, axs = plt.subplots()
    axs.set_title("Battery life development during operation")
    axs.set(xlabel='time [min]', ylabel='Battery level [%]')
    axs.set_xlim(0, (1.1 * maxtime)/60)
    axs.set_ylim(0, 100)

    rectangler = patches.Rectangle((0, 0), 60, 150, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    rectangleg = patches.Rectangle((60, 0), 150, 150, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    axs.add_patch(rectangler)
    axs.add_patch(rectangleg)

    for i in range(len(dronesdata)):
        for drType in range(len(dronesdata[i])):
            for d in dronesdata[i][drType]:
                if i == 0 and drType == 0:
                    line0, = axs.plot(d.tHistory, d.batHistory, color="red")
                elif i == 0 and drType == 1:
                    line1, = axs.plot(d.tHistory, d.batHistory, color="darkred")
                elif i == 1 and drType == 0:
                    line2, = axs.plot(d.tHistory, d.batHistory, color="deepskyblue")
                elif i == 1 and drType == 1:
                    line3, = axs.plot(d.tHistory, d.batHistory, color="royalblue")

    axs.legend([line0, line1, line2, line3], ["Small and f=1.5", "Large and f=1.5", "Small and f=2.0", "Large and f=2.0"], title="Drone type and power factor:")

    plt.show()

def batSens(startBat, stepDown, massLoss):

    # dronesdata = []
    # nRecharged = [[],[]]
    # iss = [[],[]]
    # times = [[],[]]
    # map_ax = lip0 = lip1 = drp0 = drp1 = 0
    #
    # for i in range(2):
    #     amountsRecharged = 0
    #     maxbatlife = startBat
    #     batThresh = startBat / 10 * (1 + 150000 / 127872)
    #     step = stepDown / 100 * startBat
    #     if i == 0:
    #         f = 1.5
    #     else:
    #         f = 2.0
    #
    #     while amountsRecharged < 3:
    #         print("start percentage compared to begin: ", 100 * maxbatlife / startBat)
    #
    #         droneInput["maxBat"] = np.array([0.9 * maxbatlife, 0.9 * maxbatlife])
    #         droneInput["batThreshhold"] = np.array([batThresh, batThresh])
    #         if massLoss:
    #             droneInput["m"] = np.array([4. - (startBat - maxbatlife) * 1.905 / startBat, 4. - (startBat - maxbatlife) * 1.905 / startBat])
    #
    #         # setup the ararys to keep track of the litters and drones
    #         drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
    #                                              pathplanningPar)
    #
    #         print(f)
    #         litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar,
    #                                               map_ax,
    #                                               lip0, lip1,
    #                                               drp0, drp1,
    #                                               litterInput, droneInput, batlifef=f)
    #         iss[i].append(100 * maxbatlife / startBat)
    #         dronesdata.append(drones)
    #         times[i].append(tdone)
    #
    #         maxRec = 0
    #         for dType in range(len(drones)):
    #             for d in drones[dType]:
    #                 if d.rechargeAmount > maxRec:
    #                     maxRec = d.rechargeAmount
    #                     if d.rechargeAmount > amountsRecharged:
    #                         amountsRecharged = d.rechargeAmount
    #         nRecharged[i].append(maxRec)
    #         if amountsRecharged < 3:
    #             maxbatlife -= step
    #             batThresh = maxbatlife / 10 * (1 + 150000/127872)
    #
    #         print("Amount times batteries needed to be replaced: ", amountsRecharged)
    #         print(iss)
    #         print(nRecharged)
    #         print(times)

    iss = [[100.0, 95.0, 90.0, 85.0, 80.0, 75.0, 70.0, 65.0, 60.0, 55.0, 50.0, 45.0, 40.0, 35.0, 30.0, 25.0, 20.0],
           [100.0, 95.0, 90.0, 85.0, 80.0, 75.0, 70.0, 65.0, 60.0, 55.0, 50.0, 45.0, 40.0, 35.0, 30.0]]
    nRecharged = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3], [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3]]
    times = [[2993.050000018911, 2997.050000018998, 3002.000000019106, 3007.9200000192354, 3014.860000019387,
              3021.690000019536,
              3029.6900000197106, 3039.1100000199162, 3048.3700000201184, 3058.6500000203428, 3069.340000020576,
              3080.7700000208256, 3150.61000002235, 3164.390000022651, 3174.3500000228682, 3187.310000023151,
              3257.4100000246813],
             [2993.8600000189285, 2997.050000018998, 3002.000000019106, 3008.3900000192457, 3014.370000019376,
              3021.690000019536, 3029.6900000197106, 3096.730000021174, 3106.390000021385, 3116.670000021609,
              3127.3600000218426, 3138.790000022092, 3150.61000002235, 3162.240000022604, 3232.3700000241347]]

    times[0] = np.array(times[0])
    times[1] = np.array(times[1])
    times = np.array(times, dtype=object)

    nRecharged = np.array(nRecharged, dtype=object)
    iss = np.array(iss, dtype=object)
    times = times / 60
    # mintimes = np.min(times)
    # maxtimes = np.max(times)
    # margin = 0.1 * (maxtimes - mintimes)
    # mintimes = mintimes - margin
    # maxtimes = maxtimes + margin

    print(iss)
    print(nRecharged)
    print(times)

    fig, axs = plt.subplots()
    # # fig.suptitle('Relation Litter Ratio and Operation Time')
    rectangleg = patches.Rectangle((0, 0), 150, 1.5, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    rectangleo = patches.Rectangle((0,1.5), 150, 1, edgecolor='orange', facecolor="orange", linewidth=0, alpha=0.3)
    rectangler = patches.Rectangle((0, 2.5), 150, 5, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    axs.add_patch(rectangler)
    axs.add_patch(rectangleg)
    axs.add_patch(rectangleo)
    axs.set_title("Dependence of Recharge Amount on Battery Size")
    axs.set_xlabel('Battery size compared to start [%]')
    axs.set_ylabel('Amount of Recharges [-]')
    axs.set_xlim(0, 100)
    axs.set_ylim(0, 4)
    axs.tick_params(axis="y", labelcolor="b")
    axs.invert_xaxis()
    line1 = axs.plot(iss[0], nRecharged[0], label="n battery replaced f=1.5", color="deepskyblue")
    line3 = axs.plot(iss[1], nRecharged[1], label="n battery replaced f=2.0", color="royalblue")

    axs.yaxis.set_major_locator(MaxNLocator(integer=True))
    axs2 = axs.twinx()

    line2 = axs2.plot(iss[0], times[0], label="Operating time f=1.5", color="red", marker=".")
    line4 = axs2.plot(iss[1], times[1], label="Operating time f=2.0", color="darkred", marker=".")
    axs2.set_ylim(45, 56)
    axs2.set_ylim(45, 56)
    axs2.tick_params(axis="y", labelcolor="red")
    axs2.set_xlabel('Simulation run')
    axs2.set_ylabel('Operation time [min]')

    lns = line1 + line3 + line2 + line4
    labs = [l.get_label() for l in lns]

    plt.legend(lns, labs, title="Parameter and wind factor: ", loc="upper left")

    plt.show()

def howmuchlitterfromcenter(step):
    times = []
    iss = []

    map_ax = lip0 = lip1 = drp0 = drp1 = 0

    stopamount = 20000
    litteramount = 1000
    endset = False
    while litteramount < stopamount:
        print("Litter amount: ", litteramount)
        litterInput["littern"] = np.array([int(0.64 * litteramount), int(0.36 * litteramount)])

        # setup the arrays to keep track of the litters and drones
        drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar,
                                             pathplanningPar)

        litters, drones, tdone, ts = simulate(drones, litters, grid, groundStatInput, simPar, pathplanningPar, map_ax,
                                              lip0, lip1,
                                              drp0, drp1,
                                              litterInput, droneInput)
        iss.append(litteramount)
        times.append(ts)

        if tdone > 3600 and not endset:
            stopamount = (litteramount - 1000) * 1.1
        litteramount += step



    times = np.array(times)
    times = times / 60
    mintimes = np.min(times)
    maxtimes = np.max(times)
    margin = 0.1 * (maxtimes - mintimes)
    mintimes -= margin
    maxtimes += margin

    if mintimes < 0:
        mintimes = 0

    fig, axs = plt.subplots()
    # fig.suptitle('Relation Litter Ratio and Operation Time')
    rectangler = patches.Rectangle((0, 0), 10000, 60, edgecolor='orange', facecolor="green", linewidth=0, alpha=0.3)
    rectangleg = patches.Rectangle((0, 60), 10000, 5000, edgecolor='orange', facecolor="Red", linewidth=0, alpha=0.3)
    axs.add_patch(rectangler)
    axs.add_patch(rectangleg)
    axs.set_title("Operation time from middle in relation to litter amount")
    axs.set(xlabel='Amount of Litter', ylabel='Operation time [min]')
    axs.set_xlim(900, litteramount)
    axs.set_ylim(mintimes, maxtimes)
    axs.plot(iss, times[:, 0], label="Small")
    axs.plot(iss, times[:, 1], label="Large")
    axs.legend(title="Drone type:")

    plt.show()


# ------------------------------------------------------------------------

# Tests
# dts = [0.01, 0.012, 0.014, 0.016, 0.018, 0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07]
# dts = [0.1, 0.5, 1.]

# Test to test which dt should be taken
# dts = [0.005, 0.006, 0.007, 0.009, 0.01, 0.013, 0.017, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# dtVar(dts)

# Test to test how many drones should be taken
# dronens = [1, 7]
# drVar(dronens)

# Test by varrying litter percentages
# litterVar(5)

# Test the seed
# seedVar(25)

# Test the ground station positions
# positions = [(5,5), (50,50)]
# positions = [(50, 50), (5,5), (5, 95), (95, 95), (98, 5), (13, 25), (70, 10), (90, 50)]
# gsVar(positions)

# Battery life vs. operation time
# factors = [1.5, 2.]
# batLife(factors)

# Reducing amount of battery until needs to be recharged triple
batSens(1278720, 5, True)

# Increasing the amount of litter from center
# howmuchlitterfromcenter(100)

