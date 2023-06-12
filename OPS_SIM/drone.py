import numpy as np
# import OPS_Simulation.control_and_stability.LQR_controller
import OPS_Simulation.control_and_stability.quadcopter_full_state_space as ss
import OPS_Simulation.control_and_stability.LQR_controller as LQR_controller
import scipy.io as io

from math import pi
from generalFunc import *
from minimum_snap_path_planner import *

class drone:
    def __init__(self, x, y, z, typeD, verv, mv, drv, maxvol, btte, pfc, pob, pgr, pdr, bat, litpickt, litdropt, recharget, b, d, k, m, S_blade, Ixx, Iyy, Izz, g, dt):
        self.X = np.array([[float(x)], [float(y)], [float(z)], [0], [0], [0], [0], [0], [0], [0], [0], [0]])
        self.typeD = typeD
        self.vertvmax = float(verv)
        self.volume = 0.
        self.vmax = float(mv)
        self.drivevmax = float(drv)
        self.maxvol = float(maxvol)
        self.battothrusteff = float(btte)

        self.Pwait = 0
        self.powerflightcom = float(pfc)
        self.powerobdetec = float(pob)
        self.powergrabber = float(pgr)
        self.powerdriving = float(pdr)
        self.batLifeMax = float(bat)
        self.batLife = float(bat)

        self.litpickt = float(litpickt)
        self.litdropt = float(litdropt)
        self.recharget = float(recharget)
        self.state = 0              # 0 = ready for new litter, 1 = on route, 2 = driving, 3 = picking litter, 4 = dropping litter, 5 = charging, 6 = done and waiting at gs
        self.waypoints = [[[float(x),float(y),float(z),0]]]
        # self.waypoints = [[0, 0, 20, 0], [0, 50, 10, 0], [100, 50, 10, 0], [60, 60, 8, 0], [80, 80, 3, 0],
        #                   [100, 100, 0, 0]]
        # self.waypoints = [[0, 0, 20, 0], [100, 100, 0, 0]]

        self.goal = np.array([0.,100.,0., 0])          # x, y, z, litteri
        self.waittogo = 0.

        self.b = b
        self.d = d
        self.k = k
        self.m = m
        self.S_blade = S_blade
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz

        self.A = ss.get_A(g)
        self.B = ss.get_B(self.m, self.Ixx, self.Iyy, self.Izz)
        self.C = ss.get_C()
        self.D = ss.get_D()
        self.desiredX = np.array([[0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.]])
        self.lqr_controller = LQR_controller.LQR_controller()
        self.U = [0.,0.,0.,0.]

        self.K = np.matrix(io.loadmat("OPS_Simulation/control_and_stability/Matlab/own_uav/K.mat")['K'].reshape(4, 12))
        self.E = np.linalg.inv((np.identity(12) - self.A * dt + self.B * dt * self.K))

        self.curdes = 0
        self.curway = 0
        self.litteri = []
        self.r_array = []

        self.tb = 0
        self.flyingindex = 0
        self.flyingto = 0           # 0 = litter, 1 = groundstation
        self.f = 0

        self.w_array = np.matrix([[1], [2], [3], [4]])

    def moveToWaypoint(self, curd, dmax, curdes, curw):
        # Function checks whether waypoint is reached. If not reached, the next position is the distance away that the
        # drone can travel. Otherwise it calls this function again to check how much further after the waypoint can be
        # moved. If the final waypoint is reached. The function returns -1

        dis = dist2d(self.X[0], self.goal[0], self.X[1], self.goal[1])
        if dis > (dmax - curd):
            self.X[0] += (dmax-curd) / dis * (self.goal[0] - self.X[0])
            self.X[1] += (dmax-curd) / dis * (self.goal[1] - self.X[1])
            return curw
        # elif dis < (dmax - curd) and (len(self.waypoints[curdes])-curw) > 1:
        #     curd += dis
        #     self.X[0] = self.waypoints[curdes][curw][0]
        #     self.X[1] = self.waypoints[curdes][curw][1]
        #     newWaypoint = self.moveToWaypoint(curd, dmax, curdes, curw+1)
        #     return newWaypoint
        else:
            self.X[0] = self.goal[0]
            self.X[1] = self.goal[1]
            return -1

    def calcNextPos(self, desx, desy, desz, dt):
        self.desiredX[0] = float(desx)
        self.desiredX[1] = float(desy)
        self.desiredX[2] = float(desz)

        self.w_array = self.lqr_controller.get_motor_rotation_speeds(self.X, self.desiredX, 9.80665, self, self.K)

        self.U = ss.get_U_plus_config(self.w_array, 9.80665, self)
        X_dot = np.dot(self.A, self.X) + np.dot(self.B, self.U)
        self.Y = np.dot(self.C, self.X) + np.dot(self.D, self.U)
        # self.X += X_dot * dt
        self.X = self.E * (self.X + self.B*self.K*dt*self.desiredX)

    def delaying(self, dt):
        # Function is called when waiting time >0. This function reduces the time left to wait and when it is
        # below 0, it sets it to 0 which lets the program continue

        if self.Pwait == 0:
            print("No power is used during waiting")
        self.batLife -= self.Pwait * dt

        if self.waittogo - dt > 0:
            self.waittogo -= dt
        else:
            self.waittogo = 0
            self.Pwait = 0
    def driveToLitter(self, dt):
        # Function is called each timestep to move the drone to the litter by driving. When goal is reached, state is
        # changed to 3 to pickup litter
        maxd = self.drivevmax * dt

        P = self.powerobdetec + self.powerflightcom + self.powerdriving
        self.batLife -= P * dt

        way = self.moveToWaypoint(0, maxd, self.curdes, self.curway)
        if way == -1:
            #Litter is reached
            self.state = 3

    def pickLitter(self, litters, gs):
        # Litter is picked up (time delay on the drone). The picked litter variable is changed to picked and the volume
        # of the litter is added to payload volume in the drone. Then the state is changed according to the planning.
        # When more litter is closeby, the drone drives there (2), otherwise the drone flies there (1). When cargo is
        # full, the drone flies back to ground station (1)
        litters[self.typeD][self.goal[3]].picked = True
        self.volume += litters[self.typeD][self.goal[3]].vol

        P = self.powerobdetec + self.powerflightcom + self.powergrabber
        self.Pwait = P

        self.waittogo = self.litpickt
        if len(self.waypoints) - 1 > self.curdes:
            #Drone moves to next litterpiece
            self.goal = [litters[self.typeD][self.litteri[self.curdes+1]].x, litters[self.typeD][self.litteri[self.curdes+1]].y, litters[self.typeD][self.litteri[self.curdes+1]].z, self.litteri[self.curdes+1]]
            self.curdes += 1
            self.curway = 0
            d = dist2d(self.X[0], self.goal[0], self.X[1], self.goal[1])
            if d > 10:
                self.state = 1
            else:
                self.state = 2

        else:
            #Drone flies back to van for dropoff
            self.waypoints = [[[gs["x"], gs["y"], 0 , -1]]]
            self.goal = self.waypoints[0][0]
            self.flyingto = 1
            self.state = 1
            self.curdes = 0
            self.curway = 0
    def dropLitter(self):
        # When the drone has reached the ground station for dropoff. A time delay is posed on the drone and the litter
        # volume set to 0. If the drone can continue, new litter is chosen (0). Otherwise the drone will recharge (5)

        P = self.powerflightcom + self.powergrabber + self.powerobdetec
        self.Pwait = P

        self.waittogo = self.litdropt
        self.volume = 0
        if self.batLife > 5000:
            self.state = 0
        else:
            # Battery must be replaced
            self.waittogo = self.recharget
            self.state = 5
    def recharged(self):
        # The drone has reached the ground station and is recharging. A time delay is posed and the battery capacity is
        # restored to max. Afterwards, new litter is chosen (0)
        self.batLife = self.batLifeMax
        self.state = 0
    def chooseLitter(self, litters, gap, dt, t):
        # The path planning function is called with the relevant drone information to decide which litter will be
        # picked by the drone. When this is successfull, drone will start flying (1). When no litter is available, state
        # is set to 6 to wait for more litter to be discovered.
        if self.typeD == 0:
            n = 1
        else:
            n = 1
        way = []
        liti = []
        i = 0
        while len(way) < n:
            if litters[self.typeD][i].avail:
                litters[self.typeD][i].avail = False

                coorend = [litters[self.typeD][i].x - 3, litters[self.typeD][i].y, litters[self.typeD][i].z, i]
                coormiddle = [(coorend[0]+self.X[0][0])/2, (coorend[1]+self.X[1][0])/2, 10, i]
                way.append([coorend])
                liti.append(i)
                if len(way) == 1:
                    self.goal = [litters[self.typeD][i].x, litters[self.typeD][i].y, litters[self.typeD][i].z, i]
                i += 1
            elif i+1 < len(litters[self.typeD]):
                i += 1
            else:
                if len(way) == 0:
                    self.state = 6
                break
        if self.state != 6:
            self.state = 1
            self.tb = t
            self.flyingindex=0

            # Make function for pathplanning
            self.r_array = np.array(create_trajectory(litters[self.typeD][liti[0]].path, 5, dt, gap))


        self.flyingto = 0
        self.waypoints = way
        self.litteri = liti


    def waiting(self):
        # It is checked whether more litter has become available, state will be set to 0. Otherwise it will continue
        # waiting
        None

    def flying(self, dt, t):

        # print("X: ", self.X, ", waypoints: ", self.waypoints)
        d = dist3d(self.X[0], self.waypoints[self.curdes][self.curway][0],self.X[1], self.waypoints[self.curdes][self.curway][1],self.X[2], self.waypoints[self.curdes][self.curway][2])
        # print("distance: ", d, " x: ", self.X[0], " y: ", self.X[1], " z: ", self.X[2], "desx: ", self.waypoints[self.current][0], " desy: ", self.waypoints[self.current][1], " desz: ", self.waypoints[self.current][2])
        # print(d)
        # if self.curway + 1 < len(self.waypoints[self.curdes]) and d < 1.1:
        #     # Waypoint reached
        #     self.curway += 1
        #     self.calcNextPos(self.waypoints[self.curdes][self.curway][0], self.waypoints[self.curdes][self.curway][1], self.waypoints[self.curdes][self.curway][2], dt)
        # elif d < 0.2:
        #     #Not yet able to get closer than 0.8
        #     #Destination reached
        #
        #     if self.flyingto == 0:
        #         # Drone has landed and now drives to litter
        #         self.X[2] = 0.
        #         self.state = 2
        #         # self.waypoints = [[self.goal]]
        #     elif self.flyingto == 1:
        #         # Drone has reached the groundstation
        #         self.state = 4
        # else:
        #     # Drone is on route
        #     if self.curway + 1 < len(self.waypoints):
        #         dx = self.waypoints[self.curdes][self.curway][0] - self.waypoints[self.curdes][self.curway - 1][0]
        #         dy = self.waypoints[self.curdes][self.curway][1] - self.waypoints[self.curdes][self.curway - 1][1]
        #         dz = self.waypoints[self.curdes][self.curway][2] - self.waypoints[self.curdes][self.curway - 1][2]
        #     else:
        #         dx = 0
        #         dy = 0
        #         dz = 0
        if d < 0.2:
            if self.flyingto == 0:
            # Drone has landed and now drives to litter
                self.X[2] = 0.
                self.state = 2
                # self.waypoints = [[self.goal]]
            elif self.flyingto == 1:
                # Drone has reached the groundstation
                self.state = 4
        else:

            self.calcNextPos(self.r_array[self.flyingindex][0], self.r_array[self.flyingindex][1], self.r_array[self.flyingindex][2], dt)
            if self.flyingindex + 1 < len(self.r_array):
                self.flyingindex += 1













        # Calculating the drone power and updating battery
        # https://www.tytorobotics.com/blogs/articles/how-to-increase-drone-flight-time-and-lift-capacity - propeller efficiency

        P = 0

        for w in self.w_array[:,0]:
            T_prop = self.b * w**2
            P_prop = T_prop * np.sqrt(T_prop) / np.sqrt(2 * 1.225 * self.S_blade) / self.battothrusteff
            P += P_prop

        P += self.powerflightcom + self.powerobdetec
        delta_E = max(-P*dt, -50)
        self.batLife += delta_E
        # print(self.batLife)

    def updateDrone(self, dt, t, litters, gap, gs, simPar):
        # Function: calculate next position and change drone position
        # Input: variables to describe where the drone is, where it is going and which time step is taken
        # output: new position of drone, new state of drone when goal is reached
        if self.batLife < 0 and simPar["printErrors"]:
            print("ERROR: Battery is gone while operating, drone:", self.typeD)

        if self.waittogo > 0:
            self.delaying(dt)
        else:
            # hord_to_way = dist2d(self.X[0], self.waypoints[0][0], self.X[1], self.waypoints[0][1])
            # hord_to_goal = dist2d(self.X[0], self.goal[0], self.X[1], self.goal[1])
            # self.waypoints[0][3] = hord_to_way
            # self.goal[3] = hord_to_goal

            # if self.state == 0:         # When drone is ready for new litter, choose which litter to pick and initiate flying
            #     self.chooseLitter(litters)
            # elif self.state == 1:       # When the drone is on its way, move to the checkpoints and land near the litter
            #     self.flying(dt)
            # elif self.state == 2:       # When the drone has landed, it drives to the litter
            #     self.driveToLitter(dt)
            # elif self.state == 3:       # The drone picks the litter when it is positioned on top of it. Then chooses to continue driving or start flying
            #     self.pickLitter(litters, gs)
            # elif self.state == 4:       # When the drone has reached the ground station, it drops the litter and checks battery life
            #     self.dropLitter()
            # elif self.state == 5:       # When the drone is at the ground station and needs to charge. After, litter is chosen
            #     self.recharged()
            # elif self.state == 6:       # Drone is waiting at gs until more litter becomes available by reconnaisance
            #     self.waiting()

            match self.state:
                case 0:  # When drone is ready for new litter, choose which litter to pick and initiate flying
                    self.chooseLitter(litters, gap, dt, t)
                case 1:  # When the drone is on its way, move to the checkpoints and land near the litter
                    self.flying(dt, t)
                case 2:  # When the drone has landed, it drives to the litter
                    self.driveToLitter(dt)
                case 3:  # The drone picks the litter when it is positioned on top of it. Then chooses to continue driving or start flying
                    self.pickLitter(litters, gs)
                case 4:  # When the drone has reached the ground station, it drops the litter and checks battery life
                    self.dropLitter()
                case 5:  # When the drone is at the ground station and needs to charge. After, litter is chosen
                    self.recharged()
                case 6:  # Drone is waiting at gs until more litter becomes available by reconnaisance
                    self.waiting()
