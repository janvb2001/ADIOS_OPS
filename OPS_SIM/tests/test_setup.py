import setup as setup
import generalFunc

import pytest
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import numpy as np
import random

initial_state = random.getstate()

litterInput = dict(
    amount=40,
    littern=np.array([3, 2]),
    minvol=np.array([0, 20]),
    maxvol=np.array([90, 700]),
    drivingdist=np.array([1,    1]),
    seed=3955,
)

droneInput = dict(
    dronetotal=5,  # total amount of drones
    amountDrone=np.array([2, 2, 1]),  # n of drones per type

    vertv=np.array([1, 3, 6]),  # Max vertical v per type [m/s]
    maxv=np.array([5, 6, 7]),  # Max horizontal v per type [m/s]
    drivev=np.array([0.5, 0.6, 0.7]),  # Max drive v per type [m/s]

    maxvol=np.array([450, 0, 0]),  # Max volume for litter storage [cm^3]

    battothrusteff=np.array([0.5, 0.3, 0.4]),
    powerFlightcom=np.array([8, 9, 10]),  # Power usage of the drone [W]
    powergrabbing=np.array([23, 25, 31]),  # Power usage of the drone [W]
    powerDriving=np.array([24, 26, 19]),
    powerObjDetec=np.array([18, 19, 21]),

    maxBat=np.array([1600, 1610, 1605]),  # Battery storage [kJ]

    litPickT=np.array([9, 8, 7]),  # How long it takes to pick litter when on top [s]
    litDropT=np.array([4, 5, 6]),  # How long it takes to drop litter when at gs [s]
    recharget=np.array([160, 170, 150]),

    b=np.array([2e-6, 3e-6, 4e-6]),
    d=np.array([0.05, 0.08, 0.09]),
    k=np.array([4e-8, 3e-8, 2e-8]),
    m=np.array([1.1, 1.3, 1.5]),

    S_blade=np.array([0.03, 0.02, 0.04]),

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

simPar = dict(
    runspeed=0.7,         #runspeed compared to real-time
    maxplotloops=80,       #when runspeed is set up to be faster than possible, it will plot every ... loops
    dt=0.01,                   #time step taken at every loop instance
    plotOperation=True,
    printErrors=False,
)

pathplanningPar = dict(
    gridresolution=2,
    buildingresolution=5,
    animation=False,
    obstacles=[[(15,10),(20,20)],[(30,15),(50,43)],[(50,60),(70,70)],[(21,96),(30,85)],[(5,10),(10,60)], [(90,0),(95,30)], [(17,10),(25,80)],[(60,30),(80,60)]],
    obstacleHeight=7,
    alpha_obst=0.5,
    factor_animation=7,
)
# noinspection PyStatementEffect
class test_setup(unittest.TestCase):

    with patch("generalFunc.indicesSquareCorners", side_effect=print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")):
        actual_drones, actual_litters = setup.setupClasses(litterInput,
                                                           droneInput,
                                                           groundStatInput,
                                                           areaInput,
                                                           simPar,
                                                           pathplanningPar)

    def test_drone_setup(self):

        with self.subTest():
            drone = self.actual_drones[0][0]
            actual_drone_properties = [drone.litdropt, drone.d, drone.Ixx]
            expected_drone_properties = [4, 0.05, 0.00430]

            np.testing.assert_array_equal(expected_drone_properties, actual_drone_properties)

        with self.subTest():
            drone = self.actual_drones[0][1]
            actual_drone_properties = [drone.vertvmax, drone.maxvol, drone.k]
            expected_drone_properties = [1, 450, 4e-8]

            np.testing.assert_array_equal(expected_drone_properties, actual_drone_properties)

        with self.subTest():
            drone = self.actual_drones[1][0]
            actual_drone_properties = [drone.waypoints[0][0][1], drone.power, drone.batLifeMax]
            expected_drone_properties = [40, 450, 1610]

            np.testing.assert_array_equal(expected_drone_properties, actual_drone_properties)

        with self.subTest():
            drone = self.actual_drones[1][1]
            actual_drone_properties = [drone.drivevmax, drone.litdropt, drone.Izz]
            expected_drone_properties = [0.6, 5, 0.007]

            np.testing.assert_array_equal(expected_drone_properties, actual_drone_properties)

        with self.subTest():
            drone = self.actual_drones[2][0]
            actual_drone_properties = [drone.vmax, drone.d, drone.Iyy]
            expected_drone_properties = [7, 0.09, 0.00436]

            np.testing.assert_array_equal(expected_drone_properties, actual_drone_properties)

    def test_litter_setup(self):
        random.setstate(initial_state)
        random.seed(3955)

        for i in range(3):
            with self.subTest():
                litter = self.actual_litters[0][i]
                actual_litter_properties = [litter.x, litter.y, litter.vol]
                expected_litter_properties = [random.random() * 80, random.random() * 90, random.random() * 90]

                np.testing.assert_array_equal(expected_litter_properties, actual_litter_properties)

        for i in range(2):
            with self.subTest():
                litter = self.actual_litters[1][i]
                actual_litter_properties = [litter.x, litter.y, litter.vol]
                expected_litter_properties = [random.random() * 80, random.random() * 90, random.random() * 680 + 20]

                np.testing.assert_array_equal(expected_litter_properties, actual_litter_properties)