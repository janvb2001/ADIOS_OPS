
class Drone:
    def __init__(self, x_pos, y_pos, drone_v, t_lit, t_ground, charge0, t_recharge, ddronei):
        self.x = x_pos
        self.y = y_pos
        self.t_busy = 0
        self.state = -1
        self.v = drone_v
        self.t_wait_lit = t_lit
        self.t_wait_ground = t_ground
        self.wait_t_left = 0
        self.charge0 = charge0
        self.charge = charge0
        self.rechargetime = t_recharge
        self.ddronei = ddronei


