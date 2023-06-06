import numpy as np
# import OPS_Simulation.control_and_stability.LQR_controller
import State_space.control_and_stability.quadcopter_full_state_space as ss
import State_space.control_and_stability.LQR_controller as LQR_controller

from math import pi
from generalFunc import *

class drone:
    def __init__(self, x, y, z, typeD, verv, mv, drv, maxvol, p, bat, litpickt, litdropt, b, d, k, m, Ixx, Iyy, Izz, g):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.vx = float(0)
        self.vy = float(0)
        self.vz = float(0)
        self.typeD = typeD
        self.vertvmax = verv
        self.vmax = mv
        self.drivevmax = drv
        self.maxvol = maxvol
        self.power = p
        self.batLifeMax = bat
        self.batLife = bat
        self.litpickt = litpickt
        self.litdropt = litdropt
        self.state = 1              # 0 = ready for new litter, 1 = on route, 2 = driving, 3 = picking litter, 4 = dropping litter, 5 = charging, 6 = done and waiting at gs
        self.waypoints = np.array([[0.,typeD*40,0.,0.],[typeD*40,0.,20.,sqrt((typeD*40)**2+20**2)],[100.,100.,20.,100.],[0.,100.,0.,sqrt(100**2+20**2)]])    #x, y, z, horizontal distance to previous
        self.goal = np.array([0.,100.,0., 0.])
        self.waittogo = 0.

        self.b = b
        self.d = d
        self.k = k
        self.m = m
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz
        self.phi = 0
        self.theta = 0
        self.psi = 0
        self.phi_dot = 0
        self.theta_dot = 0
        self.psi_dot = 0

        self.A = ss.get_A(g)
        self.B = ss.get_B(self.m, self.Ixx, self.Iyy, self.Izz)
        self.C = ss.get_C()
        self.D = ss.get_D()
        self.Xmat = np.array([[self.x], [self.y], [self.z], [self.vx], [self.vy], [self.vz], [self.phi], [self.theta], [self.psi], [self.phi_dot], [self.theta_dot], [self.psi_dot]])
        self.desiredXmat = np.array([[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]])
        self.lqr_controller = LQR_controller.LQR_controller()
        self.U = [0,0,0,0]



    def moveToWaypoint(self, curd, dmax, curw):
        # Function checks whether waypoint is reached. If not reached, the next position is the distance away that the
        # drone can travel. Otherwise it calls this function again to check how much further after the waypoint can be
        # moved. If the final waypoint is reached. The function returns -1

        dis = self.waypoints[curw][3]
        if dis > (dmax - curd):
            self.x += (dmax-curd) / dis * (self.waypoints[curw][0] - self.x)
            self.y += (dmax-curd) / dis * (self.waypoints[curw][1] - self.y)
            return curw
        elif dis < (dmax - curd) and (len(self.waypoints)-curw) > 1:
            curd += dis
            self.x = self.waypoints[curw][0]
            self.y = self.waypoints[curw][1]
            newWaypoint = self.moveToWaypoint(curd, dmax, curw+1)
            return newWaypoint
        else:
            self.x = self.waypoints[curw][0]
            self.y = self.waypoints[curw][1]
            return -1
    def delaying(self, dt):
        # Function is called when waiting time >0. This function reduces the time left to wait and when it is
        # below 0, it sets it to 0 which lets the program continue
        if self.waittogo - dt > 0:
            self.waittogo -= dt
        else:
            self.waittogo = 0
    def driveToLitter(self):
        # Function is called each timestep to move the drone to the litter by driving. When goal is reached, state is
        # changed to 3 to pickup litter
        None
    def pickLitter(self):
        # Litter is picked up (time delay on the drone). The picked litter variable is changed to picked and the volume
        # of the litter is added to payload volume in the drone. Then the state is changed according to the planning.
        # When more litter is closeby, the drone drives there (2), otherwise the drone flies there (1). When cargo is
        # full, the drone flies back to ground station (1)
        None
    def dropLitter(self):
        # When the drone has reached the ground station for dropoff. A time delay is posed on the drone and the litter
        # volume set to 0. If the drone can continue, new litter is chosen (0). Otherwise the drone will recharge (5)
        None
    def charging(self):
        # The drone has reached the ground station and is recharging. A time delay is posed and the battery capacity is
        # restored to max. Afterwards, new litter is chosen (0)
        None
    def chooseLitter(self):
        # The path planning function is called with the relevant drone information to decide which litter will be
        # picked by the drone. When this is successfull, drone will start flying (1). When no litter is available, state
        # is set to 6 to wait for more litter to be discovered.
        None
    def waiting(self):
        # It is checked whether more litter has become available, state will be set to 0. Otherwise it will continue
        # waiting
        None

    def flying(self, dt):
        hordmax = self.vmax * dt

        # vdis = self.vertvmax * dt
        # if self.z + vdis < 20 and self.goal[3] > 30:
        #     self.z += vdis
        # elif self.goal[3] < 30 and self.z - vdis > 1:
        #     self.z -= vdis
        # elif self.goal[3] < 10 and self.z - vdis < 1:
        #     self.z = 1
        # elif self.goal[3] > 30:
        #     self.z = 20


        # newWaypoint = self.moveToWaypoint(0, hordmax, 0)
        # if newWaypoint > 0:
        #     self.waypoints = self.waypoints[newWaypoint:]
        # elif newWaypoint == -1 and self.z <= 1:
        #     self.waittogo = 10
        #     self.waypoints = np.array([[50,50,0,0]])
        #     self.goal = np.array([50,50,0,0])
        #     self.state = 1

        self.desiredXmat[0] = 50
        self.desiredXmat[1] = 50
        self.desiredXmat[2] = 20
        self.desiredXmat[7] = 15/180*pi

        w_array = self.lqr_controller.get_motor_rotation_speeds(self.Xmat, self.desiredXmat, 9.80665, self, dt)

        self.U = ss.get_U_plus_config(w_array, 9.80665, self)
        X_dot = np.dot(self.A, self.Xmat) + np.dot(self.B, self.U)
        self.Y = np.dot(self.C, self.Xmat) + np.dot(self.D, self.U)
        self.Xmat += X_dot * dt

        # print(self.Xmat)

        self.x = self.Xmat[0]
        self.y = self.Xmat[1]
        self.z = self.Xmat[2]
        self.vx = self.Xmat[3]
        self.vy = self.Xmat[4]
        self.vz = self.Xmat[5]
        print("x: ", self.x, ", y: ", self.y, ", z: ", self.z, ", vx: ", self.vx, ", theta: ", self.Xmat[7])





    def updateDrone(self, dt):
        # Function: calculate next position and change drone position
        # Input: variables to describe where the drone is, where it is going and which time step is taken
        # output: new position of drone, new state of drone when goal is reached
        if self.waittogo > 0:
            self.delaying(dt)
        else:
            hord_to_way = dist2d(self.x, self.waypoints[0][0], self.y, self.waypoints[0][1])
            hord_to_goal = dist2d(self.x, self.goal[0], self.y, self.goal[1])
            self.waypoints[0][3] = hord_to_way
            self.goal[3] = hord_to_goal

            if self.state == 0:         # When drone is ready for new litter, choose which litter to pick and initiate flying
                self.chooseLitter()
            elif self.state == 1:       # When the drone is on its way, move to the checkpoints and land near the litter
                self.flying(dt)
            elif self.state == 2:       # When the drone has landed, it drives to the litter
                self.driveToLitter()
            elif self.state == 3:       # The drone picks the litter when it is positioned on top of it. Then chooses to continue driving or start flying
                self.pickLitter()
            elif self.state == 4:       # When the drone has reached the ground station, it drops the litter and checks battery life
                self.dropLitter()
            elif self.state == 5:       # When the drone is at the ground station and needs to charge. After, litter is chosen
                self.charging()
            elif self.state == 6:       # Drone is waiting at gs until more litter becomes available by reconnaisance
                self.waiting()










