from kinematics.config import robix
from kinematics.forward import forward_kinematics, convert_robix_to_degrees, convert_degrees_to_robix
from scipy.optimize import minimize
from scipy.spatial.distance import euclidean
import numpy as np
import math
import sys

def arctan(x):
    y = np.arctan(x + 0j)
    return np.real(y)

def arcsin(x):
    y = np.arcsin(x + 0j)
    return np.real(y)

def arccos(x):
    y = np.arccos(x + 0j)
    return np.real(y)


def final_angle(theta_1_2, deg_thetas, target):
    thetas = [convert_robix_to_degrees(theta_1_2[0], name='theta_1'), convert_robix_to_degrees(theta_1_2[1], name='theta_2')] + deg_thetas
    actual = np.matmul(forward_kinematics(thetas), np.array([[0], [0], [0], [1]]))
    return euclidean(target, actual.reshape(4))

def inverse_kinematics(Q):
    thetas = np.zeros(5)
    d1 = robix['theta_1']['d']
    d2 = robix['theta_2']['d']
    d3 = robix['theta_3']['d']
    d4 = robix['theta_4']['d']
    d5 = robix['theta_5']['d']

    l1 = robix['theta_1']['l']
    l2 = robix['theta_2']['l']
    l3 = robix['theta_3']['l']
    l4 = robix['theta_4']['l']
    l5 = robix['theta_5']['l']

    theta_sum = np.arctan2(Q[0, 2], Q[1, 2])
    thetas[4] = arctan(-1*Q[2, 1]/Q[2, 0])
    thetas[2] = arcsin((Q[2, 3] - d5*Q[2, 2] - d1)/l3)
    thetas[3] = arcsin(Q[2, 0] / np.cos(thetas[4])) - thetas[2]
    #thetas[0] = arcsin((Q[1, 3] - d5*np.sin(theta_sum)*np.cos(thetas[2]+thetas[3]) - l3*np.sin(theta_sum)*np.cos(thetas[2]) + d4*np.cos(theta_sum) - l2*np.sin(theta_sum)) / l1)
    #thetas[1] = theta_sum - thetas[0]

    target = np.matmul(Q, np.array([[0], [0], [0], [1]])).reshape(4)[0:3]
    #minimize(final_angle, [50, 50], (map(np.rad2deg, thetas[2:]), target), method='SLSQP', bounds=[(-1400, 1400), (-1400, 1400)], tol=1e-3)
    best_solution = {'error': float('inf'), 'theta_1': None, 'theta_2': None}
    for i in range(-1400, 1400, 20):
        thetas[0] = np.deg2rad(convert_robix_to_degrees(i, name='theta_1'))
        for j in range(-1400, 1400, 20):
            thetas[1] = np.deg2rad(convert_robix_to_degrees(j, name='theta_2'))
            actual = np.matmul(forward_kinematics(thetas), np.array([[0], [0], [0], [1]]))
            error = euclidean(target, actual.reshape(4)[0:3])
            if error < best_solution['error']:
                best_solution['error'] = error
                best_solution['theta_1'] = thetas[0]
                best_solution['theta_2'] = thetas[1]

    print best_solution['error']
    thetas[0] = best_solution['theta_1']
    thetas[1] = best_solution['theta_2']

    return map(np.rad2deg, thetas)

if __name__ == "__main__":
    np.set_printoptions(suppress=True)

    NUM_TRIALS=10

    actual_thetas = []
    predicted_thetas = []
    theta_x_acc = []

    for thetas in 1400 - 2800*np.random.rand(NUM_TRIALS, 5):
        thetas = convert_robix_to_degrees(thetas)
        forward = forward_kinematics(thetas)
        actual_thetas.append(thetas)
        print thetas
        #t = np.matmul(forward, np.array([[0], [0], [0], [1]]))
        #print t
        #actual_thetas.append(t)
        predicted = inverse_kinematics(forward)
        predicted_thetas.append(predicted)
        print predicted
        #predicted = forward_kinematics(predicted)
        #a = np.matmul(predicted,  np.array([[0], [0], [0], [1]]))
        #predicted_thetas.append(a)
        #print a

    predicted_thetas = np.array(predicted_thetas)
    print np.absolute(np.array(actual_thetas) -predicted_thetas).max(axis=0)
