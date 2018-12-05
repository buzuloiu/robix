from kinematics.config import robix
from kinematics.forward import forward_kinematics, convert_robix_to_degrees, convert_degrees_to_robix
import numpy as np
import math
import sys

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

    theta_sum = np.arctan(Q[0, 2]/Q[1, 2])
    thetas[4] = np.arctan(-1*Q[2, 1]/Q[2, 0])
    thetas[2] = np.arcsin((Q[2, 3] - d5*Q[2, 2] - d1)/l3)

    thetas[3] = np.arcsin(Q[2, 0] / np.cos(thetas[4])) - thetas[2]
    thetas[3] += np.arcsin(-1 * Q[2, 1] / np.sin(thetas[4])) - thetas[2]
    thetas[3] *= 0.5

#    thetas[0] = np.real(np.arcsin((Q[1, 3] - d5*np.sin(theta_sum)*np.cos(thetas[2]+thetas[3]) - l3*np.sin(theta_sum)*np.cos(thetas[2]) + d4*np.cos(theta_sum) - l2*np.sin(theta_sum)) / l1 +0j))
#    thetas[1] = theta_sum - thetas[0]

    best_solution = (float('inf'), None)
    target = np.matmul(Q, np.array([[0], [0], [0], [1]]))
    for i in range(-1400, 1400):
        thetas[0] = np.deg2rad(convert_robix_to_degrees(i, name='theta_1'))
        thetas[1] = theta_sum - thetas[0]
        actual = np.matmul(forward_kinematics(map(np.rad2deg, thetas)), np.array([[0], [0], [0], [1]]))
        error = np.absolute(target - actual).mean()
        if error < best_solution[0]:
            best_solution = (error, thetas[0])

    thetas[0] = best_solution[1]
    thetas[1] = theta_sum - thetas[0]

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
        actual_thetas.append(np.matmul(forward, np.array([[0], [0], [0], [1]])))
        predicted = inverse_kinematics(forward)
        predicted = forward_kinematics(predicted)
        predicted_thetas.append(np.matmul(predicted,  np.array([[0], [0], [0], [1]])))

    predicted_thetas = np.array(predicted_thetas)
    print np.absolute(np.array(actual_thetas) -predicted_thetas).max(axis=0)
