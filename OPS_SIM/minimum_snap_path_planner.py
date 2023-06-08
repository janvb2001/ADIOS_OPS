import numpy as np
import matplotlib.pyplot as plt

def get_A(t0, t1):
    return np.array([[t0**7, t0**6, t0**5, t0**4, t0**3, t0**2, t0, 1], # x at t1
                     [7*t0**6, 6*t0**5, 5*t0**4, 4*t0**3, 3*t0**2, 2*t0, 1, 0], # v at t1
                     [42*t0**5, 30*t0**4, 20*t0**3, 12*t0**2, 6*t0, 2, 0, 0], # a at t1
                     [210*t0**4, 120*t0**3, 60*t0**2, 24*t0, 6, 0, 0, 0], # jerk at t1
                     [t1**7, t1**6, t1**5, t1**4, t1**3, t1**2, t1, 1], # x at t1
                     [7*t1**6, 6*t1**5, 5*t1**4, 4*t1**3, 3*t1**2, 2*t1, 1, 0], # v at t1
                     [42*t1**5, 30*t1**4, 20*t1**3, 12*t1**2, 6*t1, 2, 0, 0], # a at t1
                     [210*t1**4, 120*t1**3, 60*t1**2, 24*t1, 6, 0, 0, 0]]) # jerk at t1

def get_polynomial_from_coeffs(p_array):

    t_array = lambda t: np.array([t**7, t**6, t**5, t**4, t**3, t**2, t, np.ones(len(t))])
    x_t = lambda t: np.dot(np.transpose(t_array(t)), p_array)

    return x_t

# Creates a path through a number of waypoints, where position, velocity, acceleration and jerk can be chosen
def create_trajectory(b_array, t_array):
    for i in range(len(b_array) - 1):
        print(b_array[i])
        b = np.concatenate((b_array[i], b_array[i+1]))
        b = np.matrix(b)

        print(b)
        create_spline(b, t_array[i], t_array[i+1])


# Takes the desired states at 2 end point as input, gives a trajectory as a polynomial function of time as output
def create_spline(b, t0, t1):

    # x(t) = p7 * t^7 + p6 * t^6 + p5 * t^5 + p4 t^4 + p3 * t^3 + p2 * t^2 + p1 * t + p0

    A = get_A(t0, t1)
    p_array = np.linalg.inv(A) * b

    r_t = get_polynomial_from_coeffs(p_array)

    t_array = np.arange(t0, t1, 0.01)
    r_array = r_t(t_array)

    x = r_array[:,0]
    y = r_array[:,1]
    z = r_array[:,2]
    yaw = r_array[:,3]

    plt.plot(x, y)


# b = np.transpose(np.matrix([1, -1, 0, 0, 3, -1, 0, 0]))
# create_spline(b, 3, 4)

# b_array = np.array([[1, 1, 0, 0],
#                     [2, 0, 0, 0],
#                     [1, -1, 0, 0],
#                     [3, 4, 0, 0]])
# t_array = np.array([1, 2, 3, 4])

b_array = np.array([[[1, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                    [[2, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                    [[1, 2, 2, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                    [[3, 0, 0, 0], [4, 2, 3, 0], [0, 0, 0, 0], [0, 0 ,0, 0]]])

t_array = np.array([1, 2, 3, 4])

create_trajectory(b_array, t_array)

plt.show()


