import setup as setup

import pytest
import unittest
from unittest.mock import MagicMock
import numpy as np

litterInput = dict(
    amount=40,
    littern=np.array([300, 200]),
    minvol=np.array([0, 20]),
    maxvol=np.array([90, 700]),
    seed=3955,
)

droneInput = dict(
    dronetotal=5,  # total amount of drones
    amountDrone=np.array([2, 2, 1]),  # n of drones per type

    vertv=np.array([4, 4, 4]),  # Max vertical v per type [m/s]
    maxv=np.array([7, 7, 7]),  # Max horizontal v per type [m/s]
    drivev=np.array([0.5, 0.5, 0.5]),  # Max drive v per type [m/s]

    maxvol=np.array([450, 0, 0]),  # Max volume for litter storage [cm^3]

    power=np.array([500, 450, 400]),  # Power usage of the drone [W]
    maxBat=np.array([1600, 1610, 1605]),  # Battery storage [kJ]

    litPickT=np.array([9, 8, 7]),  # How long it takes to pick litter when on top [s]
    litDropT=np.array([4, 5, 6]),  # How long it takes to drop litter when at gs [s]

    b=np.array([2e-6, 3e-6, 4e-6]),
    d=np.array([0.05, 0.08, 0.09]),
    k=np.array([4e-8, 3e-8, 2e-8]),
    m=np.array([1.1, 1.3, 1.5]),
    Ixx=np.array([0.00430, 0.00431, 0.00432]),
    Iyy=np.array([0.00434, 0.00435, 0.00436]),
    Izz=np.array([0.006, 0.007, 0.009]),
)

groundStatInput = dict(
    x=30,
    y=40,
)

areaInput = dict(
    xsize=80,
    ysize=90,
)

class test_setup(unittest.TestCase):

    def test_setupClasses(self):

        actual_drones, actual_litters = setup.setupClasses(litterInput, droneInput, groundStatInput, areaInput)

        print(actual_drones)