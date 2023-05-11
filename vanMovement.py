
def vanPosData(simInput):
    vanMoveChoice = simInput["vanMovement"]
    x_s = simInput["x_size"]
    y_s = simInput["y_size"]


    # Van starting position
    if vanMoveChoice == 0:
        #Starts in middle
        g_s = [int(x_s/2), int(y_s/2)]
        van_positions = g_s
    elif vanMoveChoice == 1:
        x_clearance = 1/10 * x_s
        y_clearance = 1/10 * y_s

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
    simInput["ground_stat_pos"] = g_s
    simInput["van_positions"] = van_positions

    return simInput