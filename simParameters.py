from math import sqrt

simInput = dict(
    litter_n = 1000,
    drone_n = 10,
    v_drone = 8,    # m/s
    v_van = 2,       # m/s
    vanMovement = 0,         # 0: Stationary van, 1: van squares around
    plot_driveplan = True,

    runspeed = 100,          # Factor wrt real-time

    dt = 0.1,  # s

    # sizes of area in m
    totalArea = 10000,       # m^2
)
simInput["x_size"] = sqrt(simInput["totalArea"])
simInput["y_size"] = sqrt(simInput["totalArea"])

