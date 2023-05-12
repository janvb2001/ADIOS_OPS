from math import sqrt

simInput = dict(
    litter_n = 1000,
    drone_n = 10,
    v_drone = 10,    # m/s
    v_ddrone = 0.5,       # m/s
    vanMovement = 3,         # 0: Stationary van, 1: van squares around, 2: square, 3: up and down


    charge0 = 20 * 60,
    t_recharge = 3 * 60,
    charge_start = 3 * 60,      # s         When the drone needs to start to go to the van for charging

    runspeed = 1000,          # Factor wrt real-time

    t_lit = 10,
    t_ground = 10,

    dt = 1,  # s

    # sizes of area in m
    totalArea = 10000,       # m^2
    plotProcess = False,
    plot_driveplan = True
)
simInput["x_size"] = sqrt(simInput["totalArea"])
simInput["y_size"] = sqrt(simInput["totalArea"])

#test

