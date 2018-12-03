from frames import frames
from frames.config import config, thetas
# from kinematics.forward import forward_kinematics
from kinematics.inverse import inverse_kinematics
import numpy as np
import sys


def generate_robix_command(theta1, theta2, theta3, theta4, theta5):
    return "MOVE 1 TO {}, 2 TO {}, 3 TO {}, 4 TO {}, 5 TO {}".format(
        convert_degrees_to_robix('theta1', theta1),
        convert_degrees_to_robix('theta2', theta2),
        convert_degrees_to_robix('theta3', theta3),
        convert_degrees_to_robix('theta4', theta4),
        convert_degrees_to_robix('theta5', theta5),
    )


def convert_degrees_to_robix(name, degrees):
    if degrees < config[name]['min'] and degrees > config[name]['max']:
        raise Exception('Robix motor "{}" is out of range ({}, {})'.format(name,
                                                                           config[name]['min'], config[name]['max']))
    return int(
        (2800./(config[name]['max'] - config[name]['min']))*degrees + config[name]['offset']
    )


def forward_kinematics():
    result = np.identity(4)
    a_matrices = np.zeros([5], dtype=object)
    for theta in thetas:
        a_matrices[thetas.index(theta)] = frames._compute_a_matrix(theta[0], theta[1])
    for matrix in a_matrices:
        # print(np.around(matrix, 2))
        result = np.matmul(result, matrix)
    # print(np.around(result, 2))
    return result


def apply_fwd_kin(x=0, y=0, z=0):
    return np.around(np.matmul(forward_kinematics(), np.array([[x],
                                                               [y],
                                                               [z],
                                                               [1]])), 2)


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    print(generate_robix_command(
        thetas[0][1],  # config['theta1']['theta_sign'],
        thetas[1][1],  # config['theta2']['theta_sign'],
        thetas[2][1],  # config['theta3']['theta_sign'],
        thetas[3][1],  # config['theta4']['theta_sign'],
        thetas[4][1],  # config['theta5']['theta_sign']
    ))
    if len(sys.argv) == 4:
        x, y, z = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        fwd_q = forward_kinematics(x, y, z)
    else:
        fwd_q = forward_kinematics()
    print(np.round(fwd_q, 3))

    inverse = inverse_kinematics(fwd_q)
    print(np.round(inverse, 3))
