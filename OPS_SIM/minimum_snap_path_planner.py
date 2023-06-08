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

    t_array = lambda t: np.array([float(t)**7, float(t)**6, float(t)**5, float(t)**4, float(t)**3, float(t)**2, float(t), 1])
    x_t = lambda t: np.dot(t_array(t), p_array)
    return x_t

# Takes the desired states at certain locations as input, gives a trajectory as a polynomial function of time as output
def create_path():


    # x(t) = p7 * t^7 + p6 * t^6 + p5 * t^5 + p4 t^4 + p3 * t^3 + p2 * t^2 + p1 * t + p0

    b = np.transpose(np.matrix([0, 0, 0, 0, 1, 0, 0, 0]))

    A = get_A(0, 1)
    p_array = np.linalg.inv(A) * b

    print(p_array)

    # x_t = lambda t: p_array[0] * t**7 + p_array[1] * t**6 + p_array[2] * t**5 + p_array[3] * t**4 + \
    #                p_array[4] * t**3 + p_array[5] * t**2 + p_array[6] * t + p_array[7]

    x_t = get_polynomial_from_coeffs(p_array)

    t_array = np.arange(0, 1, 0.1)
    x_array = x_t(t_array)

    print(t_array)
    print(x_array)

    plt.plot(t_array, x_array)
    plt.show()

create_path()



