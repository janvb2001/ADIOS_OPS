import numpy as np

litterInput = dict(
    amount=1000,
    littern=np.array([  400,    400,    200]),
    minvol=np.array([   0,      50,     100]),
    maxvol=np.array([   50,     500,    500]),
    seed=3953,
)

droneInput = dict(
    dronetotal=10,                                          # total amount of drones
    amountDrone=np.array([  4,      4,      2]),            # n of drones per type

    vertv=np.array([        3,      3,      3]),            # Max vertical v per type [m/s]
    maxv=np.array([         10,     10,     10]),           # Max horizontal v per type [m/s]
    drivev=np.array([       1,      1,      1]),            # Max drive v per type [m/s]

    maxvol=np.array([       500,    0,      0]),            # Max volume for litter storage [cm^3]

    power=np.array([        450,    450,    450]),          # Power usage of the drone [W]
    maxBat=np.array([       1620,   1620,   1620]),         # Battery storage [kJ]

    litPickT=np.array([     10,     10,     10]),           # How long it takes to pick litter when on top [s]
    litDropT=np.array([     10,     10,     10]),           # How long it takes to drop litter when at gs [s]
)

groundStatInput = dict(
    x=50,
    y=50,
)

areaInput = dict(
    xsize=100,
    ysize=100,
)

simPar = dict(
    runspeed=3,         #runspeed compared to real-time
    maxplotloops=100,       #when runspeed is set up to be faster than possible, it will plot every ... loops
    dt=0.1,                   #time step taken at every loop instance
)
