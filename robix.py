from frames import frames
from frames.config import config
from kinematics.forward import forward_kinematics, convert_degrees_to_robix
from kinematics.inverse import inverse_kinematics
import numpy as np
import sys


def generate_robix_command(thetas):
    return "MOVE 1 TO {}, 2 TO {}, 3 TO {}, 4 TO {}, 5 TO {}".format(
        convert_degrees_to_robix('theta_1', thetas[0]),
        convert_degrees_to_robix('theta_2', thetas[1]),
        convert_degrees_to_robix('theta_3', thetas[2]),
        convert_degrees_to_robix('theta_4', thetas[3]),
        convert_degrees_to_robix('theta_5', thetas[4]),
    )

"""
def convert_degrees_to_robix(name, degrees):
    if degrees < config[name]['min'] and degrees > config[name]['max']:
        raise Exception('Robix motor "{}" is out of range ({}, {})'.format(name,
                                                                           config[name]['min'], config[name]['max']))
    return int(
        (2800./(config[name]['max'] - config[name]['min']))*degrees + config[name]['offset']
    )
"""

"""
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
"""


def apply_fwd_kin(x=0, y=0, z=0):
    return np.around(np.matmul(forward_kinematics(), np.array([[x],
                                                               [y],
                                                               [z],
                                                               [1]])), 2)


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    if len(sys.argv) == 6:
        thetas = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])]
    print(generate_robix_command(thetas))
    fwd_q = forward_kinematics(thetas)
    print(np.round(fwd_q, 3))

    inverse = inverse_kinematics(fwd_q)
    print(np.round(inverse, 3))
    print(generate_robix_command(inverse))

    new_fwd = forward_kinematics(inverse)
    print(np.round(new_fwd, 3))
    print(np.allclose(np.round(new_fwd, 3), fwd_q, rtol=1.e-1))
