import numpy as np
import matplotlib.pyplot as plt
from directions import Directions

### Use the function create_trajectory(a_star_position_arrray, nominal_speed, dt) ###

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


def create_setpoints_from_Astar(a_star_position_array, nominal_speed, block_size):

    b_list = []
    t_list = []

    x_array = a_star_position_array[:, 0]
    y_array = a_star_position_array[:, 1]

    current_direction = get_wind_direction(x_array[0], x_array[1], y_array[0], y_array[1])

    t = 0

    time_increment = 0.5 / nominal_speed # Was empirically found to work nicely

    for i in range(len(a_star_position_array)):

        x = x_array[i]
        y = y_array[i]

        if i == 0:  # Initial point: path must start with 0 initial velocity, acceleration and jerk
            b_list.append([[x, y, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
            t_list.append(t)
            t += time_increment

            x_next = x_array[i + 1]
            y_next = y_array[i + 1]

            continue

        elif i == len(a_star_position_array) - 1:  # Final point: path must end with 0 final velocity, acceleration and jerk
            b_list.append([[x, y, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
            t_list.append(t)
            t += time_increment

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

        if direction_change == 0:  # Not changing direction: Speed is increased to straight_speed
            t += time_increment

        elif next_direction % 2 == 0:  # Means shifting to travelling along +/- 90 degrees direction
            if abs(direction_change) == 1 or abs(direction_change) == 7: # Making a 45 degree turn
                x_setpoint_1 = (x_prev + x) / 2
                y_setpoint_1 = (y_prev + y) / 2

                x_speed_1, y_speed_1, x_accel_1, y_accel_1 = get_velocity_and_accel_from_dir(previous_direction, direction_change, nominal_speed, block_size)
                yaw_angle_1 = get_yaw_angle_from_velocity(x_speed_1, y_speed_1)

                b_list.append([[x_setpoint_1, y_setpoint_1, 0, yaw_angle_1], [x_speed_1, y_speed_1, 0, 0], [x_accel_1, y_accel_1, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += time_increment

                x_speed_2, y_speed_2, x_accel_2, y_accel_2 = get_velocity_and_accel_from_dir(next_direction, 0, nominal_speed, block_size)
                yaw_angle_2 = get_yaw_angle_from_velocity(x_speed_2, y_speed_2)

                b_list.append([[x_next, y_next, 0, yaw_angle_2], [x_speed_2, y_speed_2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += time_increment

            elif abs(direction_change) == 2 or abs(direction_change) == 6: # Making a 90 degree turn

                x_speed_1, y_speed_1, x_accel_1, y_accel_1 = get_velocity_and_accel_from_dir(previous_direction, direction_change, nominal_speed, block_size)
                x_speed_2, y_speed_2, x_accel_2, y_accel_2 = get_velocity_and_accel_from_dir(next_direction, direction_change, nominal_speed, block_size)

                yaw_angle_1 = get_yaw_angle_from_velocity(x_speed_1, y_speed_1)
                yaw_angle_2 = get_yaw_angle_from_velocity(x_speed_2, y_speed_2)

                b_list.append([[x_prev, y_prev, 0, yaw_angle_1], [x_speed_1, y_speed_1, 0, 0], [x_accel_1, y_accel_1, 0, 0], [0, 0, 0, 0]])
                b_list.append([[x_next, y_next, 0, yaw_angle_2], [x_speed_2, y_speed_2, 0, 0], [x_accel_2, y_accel_2, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += time_increment
                t_list.append(t)
                t += time_increment

        elif next_direction % 2 == 1:  # Means shifting to travelling along +/- 45 degrees direction
            if abs(direction_change) == 1 or abs(direction_change) == 7:   # Making a 45 degree turn
                x_setpoint_1 = (x + x_next) / 2
                y_setpoint_1 = (y + y_next) / 2

                x_speed_1, y_speed_1, x_accel_1, y_accel_1 = get_velocity_and_accel_from_dir(next_direction, direction_change, nominal_speed, block_size)
                yaw_angle_1 = get_yaw_angle_from_velocity(x_speed_1, y_speed_1)

                b_list.append([[x_setpoint_1, y_setpoint_1, 0, yaw_angle_1], [x_speed_1, y_speed_1, 0, 0], [x_accel_1, x_accel_1, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += time_increment

            elif abs(direction_change) == 2 or abs(direction_change) == 6: # Making a 90 degree turn

                x_setpoint_1 = (x_prev + x) / 2
                y_setpoint_1 = (y_prev + y) / 2

                x_setpoint_2 = (x + x_next) / 2
                y_setpoint_2 = (y + y_next) / 2

                x_speed_1, y_speed_1, x_accel_1, y_accel_1 = get_velocity_and_accel_from_dir(previous_direction, direction_change, nominal_speed, block_size)
                x_speed_2, y_speed_2, x_accel_2, y_accel_2 = get_velocity_and_accel_from_dir(next_direction, direction_change, nominal_speed, block_size)

                yaw_angle_1 = get_yaw_angle_from_velocity(x_speed_1, y_speed_1)
                yaw_angle_2 = get_yaw_angle_from_velocity(x_speed_2, y_speed_2)

                b_list.append([[x_setpoint_1, y_setpoint_1, 0, yaw_angle_1], [x_speed_1, y_speed_1, 0, 0], [x_accel_1, x_accel_1, 0, 0], [0, 0, 0, 0]])
                b_list.append([[x_setpoint_2, y_setpoint_2, 0, yaw_angle_2], [x_speed_2, y_speed_2, 0, 0], [x_accel_2, x_accel_2, 0, 0], [0, 0, 0, 0]])

                t_list.append(t)
                t += time_increment
                t_list.append(t)
                t += time_increment

    return np.array(b_list), np.array(t_list)


def get_wind_direction(x_1, x_2, y_1, y_2):

    # Default
    direction = Directions.NORTH

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


def get_velocity_and_accel_from_dir(direction, direction_change, speed, block_size):

    accel_magnitude_90_deg_turn = speed**2 / block_size
    accel_magnitude_45_deg_turn = speed**2 / (2 * block_size)

    x_speed = 0
    y_speed = 0

    x_accel = 0
    y_accel = 0

    # Velocity assignment block
    match direction:
        case 0:
            y_speed = + speed
        case 1:
            x_speed = + 0.5 * np.sqrt(2) * speed
            y_speed = + 0.5 * np.sqrt(2) * speed
        case 2:
            x_speed = + speed
        case 3:
            x_speed = + 0.5 * np.sqrt(2) * speed
            y_speed = - 0.5 * np.sqrt(2) * speed
        case 4:
            y_speed = - speed
        case 5:
            x_speed = - 0.5 * np.sqrt(2) * speed
            y_speed = - 0.5 * np.sqrt(2) * speed
        case 6:
            x_speed = - speed
        case 7:
            x_speed = - 0.5 * np.sqrt(2) * speed
            y_speed = + 0.5 * np.sqrt(2) * speed

    next_direction = direction + direction_change


    # Acceleration assignment block

    # For 90 degree turns
    if abs(direction_change) == 2 or abs(direction_change) == 6:
        match next_direction: # Normal acceleration at the start of a 90 degree turn is always pointed in the same direction as the end of the 90 degree turn
            case 0:
                x_accel = 0
                y_accel = accel_magnitude_90_deg_turn
            case 1:
                pass
            case 2:
                x_accel = accel_magnitude_90_deg_turn
                y_accel = 0
            case 3:
                pass
            case 4:
                x_accel = 0
                y_accel = - accel_magnitude_90_deg_turn
            case 5:
                pass
            case 6:
                x_accel = - accel_magnitude_90_deg_turn
                y_accel = 0
            case 7:
                pass


    return x_speed, y_speed, x_accel, y_accel


def get_yaw_angle_from_velocity(x_speed, y_speed):

    arg = 0
    if not x_speed == 0:
        arg = np.arctan(y_speed / x_speed)

    if y_speed < 0:
        arg += np.deg2rad(180)

    return arg


# Takes the desired states at 2 end point as input, gives a trajectory as a polynomial function of time as output
def create_spline(b, t0, t1, dt):
    # x(t) = p7 * t^7 + p6 * t^6 + p5 * t^5 + p4 t^4 + p3 * t^3 + p2 * t^2 + p1 * t + p0

    A = get_A(t0, t1)
    p_array = np.linalg.inv(A) * b

    r_t = get_polynomial_from_coeffs(p_array)

    t_array = np.arange(t0, t1, dt)
    r_array = r_t(t_array)

    return r_array


# Creates a path through a number of waypoints, where position, velocity, acceleration and jerk can be chosen
def create_trajectory(a_star_position_array, nominal_speed, dt, block_size):
    b_array, t_array = create_setpoints_from_Astar(a_star_position_array, nominal_speed, block_size)

    r_array = np.empty((0, 4))
    for i in range(len(b_array) - 1):
        b = np.concatenate((b_array[i], b_array[i + 1]))
        b = np.matrix(b)

        local_r_array = create_spline(b, t_array[i], t_array[i + 1], dt)

        r_array = np.concatenate((r_array, local_r_array))
    return r_array


if __name__=="__main__":

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

    b_array, t_array = create_setpoints_from_Astar(a_star_position_array, 10, 1)

    x_points = b_array[:,0,0]
    y_points = b_array[:,0,1]


    vx = b_array[:,1,0]
    vy = b_array[:,1,1]

    ax = b_array[:,2,0]
    ay = b_array[:,2,1]

    for i in range(len(t_array)):
        print('x:', x_points[i], 'vx:', vx[i], 'vy:', vy[i], 'ax:', ax[i], 'ay:', ay[i], 't:', t_array[i])

    ### PLOT GRIDLINES ###

    for i in range(7):
        plt.plot([0, 5], [i, i], color='black')

    for i in range(6):
        plt.plot([i, i], [0, 6], color='black')

    for i in range(90):
        plt.plot([i / 100 + 4.05, i / 100 + 4.05], [1 + 0.1, 2 - 0.1], color='red')
        plt.plot([i / 100 + 3.05, i / 100 + 3.05], [1 + 0.1, 2 - 0.1], color='red')
        plt.plot([i / 100 + 2.05, i / 100 + 2.05], [1 + 0.1, 2 - 0.1], color='red')
        plt.plot([i / 100 + 1.05, i / 100 + 1.05], [1 + 0.1, 2 - 0.1], color='red')
        plt.plot([i / 100 + 1.05, i / 100 + 1.05], [2 + 0.1, 3 - 0.1], color='red')

        plt.plot([3.5, 4.5], [0.5, 5.5], 'o', markersize='20', color='black')
    ######################

    #plt.plot(a_star_position_array[:, 0], a_star_position_array[:, 1], 'x', color='b', markersize='10')
    plt.plot(x_points, y_points, 'o', color='red')

    r_array = create_trajectory(a_star_position_array, 1, 0.01, 1)

    plt.plot(r_array[:,0], r_array[:,1], color='green', markersize='5')
    plt.show()