from math import sqrt

def dist2d(x1, x2, y1, y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

def dist3d(x1, x2, y1, y2, z1, z2):
    return sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)