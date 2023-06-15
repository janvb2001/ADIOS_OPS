import numpy as np

litterInput = dict(
    amount=10,
    littern=np.array([  500,    500]),
    minvol=np.array([   0,      50]),
    maxvol=np.array([   50,     500]),
    drivingdist=np.array([3.,    3.]),
    seed=3953,
)

droneInput = dict(
    dronetotal=10,                                          # total amount of drones
    amountDrone=np.array([  5,      5]),            # n of drones per type

    vertv=np.array([        3,      3]),            # Max vertical v per type [m/s]
    maxv=np.array([         5,     5]),           # Max horizontal v per type [m/s]
    drivev=np.array([       1,      1]),        # Max drive v per type [m/s]
    drivedistbetlit=np.array([  6,      6]),

    maxvol=np.array([       500,    0]),            # Max volume for litter storage [cm^3]

    batThreshhold=np.array([5000,   5000]),
    battothrusteff=np.array([       0.7,    0.7]),
    powerFlightcom=np.array([       10,    10]),          # Power usage of the drone [W]
    powergrabbing=np.array([        30,    30]),          # Power usage of the drone [W]
    powerDriving=np.array([        30,    30]),
    powerObjDetec=np.array([        20,    20]),          # Power usage of the drone [W]
    maxBat=np.array([       26640,   26640]),         # Battery storage [J]

    litPickT=np.array([     2,     2]),           # How long it takes to pick litter when on top [s]
    litDropT=np.array([     2,     2]),           # How long it takes to drop litter when at gs [s]
    recharget=np.array([    180,    180]),

    b=np.array([            3e-6,   3e-6]),
    d=np.array([            0.1,    0.1]),
    k=np.array([            3e-8,   3e-8]),
    m=np.array([            1.2,    1.2]),
    l=np.array([            0.1,    0.1]),
    max_rpm=np.array([      1500,   1500]),

    S_blade=np.array([      0.01,   0.01]),

    Ixx=np.array([          0.00433,    0.00433]),
    Iyy=np.array([          0.00433,    0.00433]),
    Izz=np.array([          0.008,      0.008]),
)

groundStatInput = dict(
    x=5,
    y=5,
)

areaInput = dict(
    xsize=100,
    ysize=100,
)

simPar = dict(
    runspeed=3,         #runspeed compared to real-time
    maxplotloops=100,       #when runspeed is set up to be faster than possible, it will plot every ... loops
    dt=0.02,                   #time step taken at every loop instance
    plotOperation=True,
    printErrors=False,
)

pathplanningPar = dict(
    gridresolution=1,
    buildingresolution=10,
    animation=False,
    obstacles=[[(10,10),(20,20)],[(40,15),(50,40)],[(50,60),(70,70)],[(20,80),(30,85)],[(5,10),(10,60)], [(90,0),(95,30)], [(17,10),(25,80)],[(60,30),(80,60)]],
    obstacleHeight=8,
    alpha_obst=0.4,
    factor_animation=8,
)
