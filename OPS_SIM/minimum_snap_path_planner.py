import numpy as np
import matplotlib.pyplot as plt
from directions import Directions


def get_A(t0, t1):
    return np.array([[t0 ** 7, t0 ** 6, t0 ** 5, t0 ** 4, t0 ** 3, t0 ** 2, t0, 1],  # x at t1
                     [7 * t0 ** 6, 6 * t0 ** 5, 5 * t0 ** 4, 4 * t0 ** 3, 3 * t0 ** 2, 2 * t0, 1, 0],  # v at t1
                     [42 * t0 ** 5, 30 * t0 ** 4, 20 * t0 ** 3, 12 * t0 ** 2, 6 * t0, 2, 0, 0],  # a at t1
                     [210 * t0 ** 4, 120 * t0 ** 3, 60 * t0 ** 2, 24 * t0, 6, 0, 0, 0],  # jerk at t1
                     [t1 ** 7, t1 ** 6, t1 ** 5, t1 ** 4, t1 ** 3, t1 ** 2, t1, 1],  # x at t1
                     [7 * t1 ** 6, 6 * t1 ** 5, 5 * t1 ** 4, 4 * t1 ** 3, 3 * t1 ** 2, 2 * t1, 1, 0],  # v at t1
                     [42 * t1 ** 5, 30 * t1 ** 4, 20 * t1 ** 3, 12 * t1 ** 2, 6 * t1, 2, 0, 0],  # a at t1
                     [210 * t1 ** 4, 120 * t1 ** 3, 60 * t1 ** 2, 24 * t1, 6, 0, 0, 0]])  # jerk at t1


def get_polynomial_from_coeffs(p_array):
    t_array = lambda t: np.array([t ** 7, t ** 6, t ** 5, t ** 4, t ** 3, t ** 2, t, np.ones(len(t))])
    x_t = lambda t: np.dot(np.transpose(t_array(t)), p_array)

    return x_t


def create_setpoints_from_Astar(a_star_position_array, speed):

    b_list = []
    t_list = []

    x_array = a_star_position_array[:, 0]
    y_array = a_star_position_array[:, 1]

    current_direction = get_wind_direction(x_array[0], x_array[1], y_array[0], y_array[1])

    t = 0

    for i in range(len(a_star_position_array)):

        x = x_array[i]
        y = y_array[i]

        if i == 0:  # Initial point: path must start with 0 initial velocity, acceleration and jerk
            b_list.append([[x, y, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
            t_list.append(t)
            t += 1

            x_next = x_array[i + 1]
            y_next = y_array[i + 1]

            continue

        elif i == len(a_star_position_array) - 1:  # Final point: path must end with 0 final velocity, acceleration and jerk
            b_list.append([[x, y, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
            t_list.append(t)
            t += 1

            x_prev = x_array[i - 1]
            y_prev = y_array[i - 1]

            continue

        x_prev = x_array[i - 1]
        y_prev = y_array[i - 1]

        x_next = x_array[i + 1]
        y_next = y_array[i + 1]

        next_direction = get_wind_direction(x, x_next, y, y_next)

        direction_change = next_direction - current_direction

        previous_direction = current_direction
        current_direction = next_direction

        if next_direction % 2 == 0:  # Means shifting to travelling along +/- 90 degrees direction

            if direction_change == 0:  # Not changing direction: no new setpoint needed
                pass

            elif abs(direction_change) == 1 or abs(direction_change) == 7: # Making a 45 degree turn
                x_setpoint = (x_prev + x) / 2
                y_setpoint = (y_prev + y) / 2

                x_speed, y_speed = get_velocity_and_accel_from_direction(previous_direction, speed)

                b_list.append([[x_setpoint, y_setpoint, 0, 0], [x_speed, y_speed, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += 1

            elif abs(direction_change) == 2 or abs(direction_change) == 6: # Making a 90 degree turn

                x_speed_1, y_speed_1 = get_velocity_and_accel_from_direction(previous_direction, speed)
                x_speed_2, y_speed_2 = get_velocity_and_accel_from_direction(next_direction, speed)

                b_list.append([[x_prev, y_prev, 0, 0], [x_speed_1, y_speed_1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
                b_list.append([[x_next, y_next, 0, 0], [x_speed_2, y_speed_2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += 1
                t_list.append(t)
                t += 1

        elif next_direction % 2 == 1:  # Means shifting to travelling along +/- 45 degrees direction

            if direction_change == 0:  # Not changing direction: no new setpoint needed
                pass

            elif abs(direction_change) == 1 or abs(direction_change) == 7:   # Making a 45 degree turn
                x_setpoint = (x + x_next) / 2
                y_setpoint = (y + y_next) / 2

                x_speed, y_speed = get_velocity_and_accel_from_direction(next_direction, speed)

                b_list.append([[x_setpoint, y_setpoint, 0, 0], [x_speed, y_speed, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += 1

            elif abs(direction_change) == 2 or abs(direction_change) == 6: # Making a 90 degree turn

                x_setpoint_1 = (x_prev + x) / 2
                y_setpoint_1 = (y_prev + y) / 2

                x_speed, y_speed = get_velocity_and_accel_from_direction(next_direction, speed)

                b_list.append([[x_setpoint_1, y_setpoint_1, 0, 0], [x_speed, y_speed, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

                x_setpoint_2 = (x + x_next) / 2
                y_setpoint_2 = (y + y_next) / 2

                b_list.append([[x_setpoint_2, y_setpoint_2, 0, 0], [x_speed, y_speed, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += 1
                t_list.append(t)
                t += 1

    print('---------------------')
    return np.array(b_list), np.array(t_list)


def get_wind_direction(x_1, x_2, y_1, y_2):
    if y_1 < y_2:
        if x_1 == x_2:
            direction = Directions.NORTH
        elif x_1 > x_2:
            direction = Directions.NORTH_WEST
        elif x_1 < x_2:
            direction = Directions.NORTH_EAST

    elif y_1 > y_2:
        if x_1 == x_2:
            direction = Directions.SOUTH
        elif x_1 > x_2:
            direction = Directions.SOUTH_WEST
        elif x_1 < x_2:
            direction = Directions.SOUTH_EAST

    else:
        if x_1 > x_2:
            direction = Directions.WEST
        elif x_1 < x_2:
            direction = Directions.EAST

    return direction.value


def get_velocity_and_accel_from_direction(direction, speed):
    x_speed = 0
    y_speed = 0

    x_accel = 0
    y_accel = 0

    if direction == 0:
        y_speed = + speed

    elif direction == 1:
        x_speed = + 0.5 * np.sqrt(2) * speed
        y_speed = + 0.5 * np.sqrt(2) * speed

    elif direction == 2:
        x_speed = + speed

    elif direction == 3:
        x_speed = + 0.5 * np.sqrt(2) * speed
        y_speed = - 0.5 * np.sqrt(2) * speed

    elif direction == 4:
        y_speed = - speed

    elif direction == 5:
        x_speed = - 0.5 * np.sqrt(2) * speed
        y_speed = - 0.5 * np.sqrt(2) * speed

    elif direction == 6:
        x_speed = - speed

    elif direction == 7:
        x_speed = - 0.5 * np.sqrt(2) * speed
        y_speed = + 0.5 * np.sqrt(2) * speed

    return x_speed, y_speed


# Creates a path through a number of waypoints, where position, velocity, acceleration and jerk can be chosen
def create_trajectory(b_array, t_array):
    r_array = np.empty((0, 4))
    for i in range(len(b_array) - 1):
        b = np.concatenate((b_array[i], b_array[i + 1]))
        b = np.matrix(b)

        local_r_array = create_spline(b, t_array[i], t_array[i + 1])

        r_array = np.concatenate((r_array, local_r_array))
    return r_array


# Takes the desired states at 2 end point as input, gives a trajectory as a polynomial function of time as output
def create_spline(b, t0, t1):
    # x(t) = p7 * t^7 + p6 * t^6 + p5 * t^5 + p4 t^4 + p3 * t^3 + p2 * t^2 + p1 * t + p0

    A = get_A(t0, t1)
    p_array = np.linalg.inv(A) * b

    r_t = get_polynomial_from_coeffs(p_array)

    t_array = np.arange(t0, t1, 0.01)
    r_array = r_t(t_array)

    x = r_array[:, 0]
    y = r_array[:, 1]
    z = r_array[:, 2]
    yaw = r_array[:, 3]

    return r_array


# b_array = np.array([[[1, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], # [point, r/v/a/jerk, x/y/z/yaw]
#                     [[2, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#                     [[1, 2, 2, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#                     [[3, 0, 0, 0], [4, 2, 3, 0], [0, 0, 0, 0], [0, 0 ,0, 0]]])

a_star_position_array = np.array([[3.5, 0.5],
                                      [2.5, 0.5],
                                      [1.5, 0.5],
                                      [0.5, 0.5],
                                      [0.5, 1.5],
                                      [0.5, 2.5],
                                      [1.5, 3.5],
                                      [2.5, 4.5],
                                      [3.5, 5.5],
                                      [4.5, 5.5]])

b_array, t_array = create_setpoints_from_Astar(a_star_position_array, 5)

x_points = b_array[:,0,0]
y_points = b_array[:,0,1]


vx = b_array[:,1,0]
vy = b_array[:,1,1]

for i in range(len(t_array)):
    print('x:', x_points[i], 'vx:', vx[i], 'vy:', vy[i], 't:', t_array[i])

plt.plot(a_star_position_array[:,0], a_star_position_array[:,1], 'x', color='b', markersize='10')
plt.plot(x_points, y_points, 'ro', color='red')

r_array = create_trajectory(b_array, t_array)

plt.plot(r_array[:,0], r_array[:,1])
plt.show()