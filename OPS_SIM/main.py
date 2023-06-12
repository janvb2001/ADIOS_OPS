import time
import random

import numpy as np

from inputs import *
from setup import *
from simulation import *



# setup the ararys to keep track of the litters and drones
drones, litters, grid = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar, pathplanningPar)

# setup the 3D plot
if simPar["plotOperation"]:
    map_ax, lip0, lip1, drp0, drp1 = plotSetup(litters, drones, groundStatInput, areaInput, pathplanningPar)
else:
    map_ax = lip0 = lip1 = drp0 = drp1 = None

# simulate
simulate(drones, litters, groundStatInput, simPar, pathplanningPar, map_ax, lip0, lip1, drp0, drp1)





