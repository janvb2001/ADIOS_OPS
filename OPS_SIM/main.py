import time
import random

import numpy as np

from inputs import *
from setup import *
from simulation import *



# setup the ararys to keep track of the litters and drones
drones, litters = setupClasses(litterInput, droneInput, groundStatInput, areaInput, simPar)

# setup the 3D plot
map_ax, lip0, lip1, drp0, drp1 = plotSetup(litters, drones, groundStatInput, areaInput)

# simulate
simulate(drones, litters, groundStatInput, simPar, map_ax, lip0, lip1, drp0, drp1)





