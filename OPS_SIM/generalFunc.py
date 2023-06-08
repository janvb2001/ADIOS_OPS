from math import sqrt
import numpy as np

def dist2d(x1, x2, y1, y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

def dist3d(x1, x2, y1, y2, z1, z2):
    return sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

def dronePower():
    # Total power = induced power (Pi) + profile power (Pp) + parasite power (Ppar)
    # https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7991310&tag=1

    # k1 =
    None

def lineCrossCells(obst,begin,end):
    # obst =    [[]
    #            []
    #            []
    #            []]
    # begin:    [0,0]
    # end:      [10,10]

    xs = np.arange(0,len(obst[0]), 0.1)
    crossed = np.zeros((len(obst),len(obst[0])))

    a = (end[1]-begin[1])/(end[0]-begin[0])
    b = begin[1]-a*begin[0]

    ys = a * xs + b

    for i in range(len(ys)):
        ix = int(np.floor(xs[i]))
        iy = int(np.floor(ys[i]))
        if ix < len(crossed[0]) and iy < len(crossed):
            crossed[iy][ix] = True
    obsAndCrossed = obst&crossed
    print(obsAndCrossed)




#lineCrossCells(np.array([[False,False,True,True],[False,True,True,True],[False,True,False,True]]), [0,0],[4,3])
