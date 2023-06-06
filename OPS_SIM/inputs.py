import numpy as np

litterInput = dict(
    amount=1000,
    littern=np.array([  500,    500]),
    minvol=np.array([   0,      50]),
    maxvol=np.array([   50,     500]),
    seed=3953,
)

droneInput = dict(
    dronetotal=10,                                          # total amount of drones
    amountDrone=np.array([  1,      0,      0]),            # n of drones per type

    vertv=np.array([        3,      3,      3]),            # Max vertical v per type [m/s]
    maxv=np.array([         10,     10,     10]),           # Max horizontal v per type [m/s]
    drivev=np.array([       1,      1,      1]),            # Max drive v per type [m/s]

    maxvol=np.array([       500,    0,      0]),            # Max volume for litter storage [cm^3]

    power=np.array([        450,    450,    450]),          # Power usage of the drone [W]
    maxBat=np.array([       1620,   1620,   1620]),         # Battery storage [kJ]

    litPickT=np.array([     10,     10,     10]),           # How long it takes to pick litter when on top [s]
    litDropT=np.array([     10,     10,     10]),           # How long it takes to drop litter when at gs [s]

    b=np.array([            3e-6,   3e-6,   3e-6]),
    d=np.array([            0.1,    0.1,    0.1]),
    k=np.array([            3e-8,   3e-8,   3e-8]),
    m=np.array([            1.2,    1.2,    1.2]),
    Ixx=np.array([          0.00433,    0.00433,    0.00433]),
    Iyy=np.array([          0.00433,    0.00433,    0.00433]),
    Izz=np.array([          0.008,      0.008,      0.008]),
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
    runspeed=1,         #runspeed compared to real-time
    maxplotloops=100,       #when runspeed is set up to be faster than possible, it will plot every ... loops
    dt=0.001,                   #time step taken at every loop instance
)
