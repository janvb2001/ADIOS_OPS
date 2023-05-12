from math import sqrt

class DrivingDrone:
    def __init__(self, x_pos, y_pos, ddrone_v, waypoints, n_drones, maxv):
        self.x = x_pos
        self.y = y_pos
        self.v = ddrone_v
        self.maxv = maxv
        self.waypoints = waypoints
        self.n_drones = n_drones
        self.cur_goal = 1


def ddronePosData(simInput, par = []):
    # output: array [[xs], [ys]]. when first checkpoint is reached, the van will move to the next
    vanMoveChoice = simInput["vanMovement"]
    x_s = simInput["x_size"]
    y_s = simInput["y_size"]


    # Van starting position
    if vanMoveChoice == 0:
        # par = [x, y]
        if len(par) > 0:
            g_s = [int(par[0]), int(par[1])]
        else:
            # starts in middle
            g_s = [int(x_s / 2), int(y_s / 2)]
        van_positions = g_s
    elif vanMoveChoice == 1:
        # par = [x_clearance, y_clearance]

        x_clearance = par[0]
        y_clearance = par[1]

        ly = y_s - y_clearance
        lx = x_s - x_clearance

        g_s = [int(x_clearance), int(y_clearance)]
        van_positions = [[g_s[0], g_s[0]],
                         [g_s[1], g_s[1] + ly - y_clearance]]

        dir = 2             # 1: up, 2: right, 3: down, 4: left
        cont = True
        while cont:
            if dir == 1:
                ly = ly - y_clearance
                van_positions[0].append(van_positions[0][-1])
                van_positions[1].append(van_positions[1][-1] + ly)
            elif dir == 2:
                lx = lx - x_clearance
                van_positions[0].append(van_positions[0][-1] + lx)
                van_positions[1].append(van_positions[1][-1])
            elif dir == 3:
                ly = ly - y_clearance
                van_positions[0].append(van_positions[0][-1])
                van_positions[1].append(van_positions[1][-1] - ly)
            elif dir == 4:
                lx = lx - x_clearance
                van_positions[0].append(van_positions[0][-1] - lx)
                van_positions[1].append(van_positions[1][-1])
                dir = 0

            if lx < 0 or ly < 0:
                cont = False
            dir += 1
    elif vanMoveChoice == 2:
        l_side = sqrt(x_s * y_s / 2)

        g_s = [int(x_s/2 - 0.5 * l_side), int(y_s/2 - 0.5 * l_side)]
        van_positions = [[x_s/2 - 0.5 * l_side, x_s/2 - 0.5 * l_side, x_s/2 + 0.5 * l_side, x_s/2 + 0.5 * l_side],
                         [y_s/2 - 0.5 * l_side, y_s/2 + 0.5 * l_side, y_s/2 + 0.5 * l_side, y_s/2 - 0.5 * l_side]]


    elif vanMoveChoice == 3:
        # par = [n_x, y_c]

        # n_x = 1/10 * x_s
        # y_c = 1/20 * y_s
        n_x = par[0]
        y_c = par[1]

        x = 0
        y = y_c

        g_s = [0, y_c]
        van_positions = [[0],
                         [y_c]]
        drawing = True
        up = True
        while drawing:
            if x <= x_s and up:
                y += y_s - 2 * y_c
                up = False
            elif x <= x_s and not up:
                y -= y_s - 2 * y_c
                up = True
            elif x > x_s:
                drawing = False

            if drawing:
                van_positions[0].append(x)
                van_positions[1].append(y)

                x += n_x
                if x <= x_s:

                    van_positions[0].append(x)
                    van_positions[1].append(y)


    ddrone = DrivingDrone(g_s[0], g_s[1], simInput["v_ddrone"], van_positions, simInput["drone_n"], simInput["v_ddrone"])

    simInput["ground_stat_pos"] = g_s
    simInput["van_positions"] = van_positions

    return simInput, ddrone