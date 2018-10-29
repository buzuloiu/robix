from frames import frames
from frames.config import config, thetas
import numpy as np


def generate_robix_command(theta1, theta2, theta3, theta4, theta5, theta6):
    return "MOVE 1 TO {}, 2 TO {}, 3 TO {}, 4 TO {}, 5 TO {}, 6 TO {}".format(
        convert_degrees_to_robix('theta1', theta1),
        convert_degrees_to_robix('theta2', theta2),
        convert_degrees_to_robix('theta3', theta3),
        convert_degrees_to_robix('theta4', theta4),
        convert_degrees_to_robix('theta5', theta5),
        convert_degrees_to_robix('theta6', theta6),
    )


def convert_degrees_to_robix(name, degrees):
    return int(
        ((config[name]['max'] - config[name]['min']) / 2800.)*degrees + config[name]['offset']
    )


def forward_kinematics():
    result = np.identity(4)
    a_matrices = np.empty([0, 0])
    for theta in thetas:
        np.append(a_matrices, frames._compute_a_matrix(theta, thetas[theta]))
    for matrix in a_matrices:
        result = np.matmul(result, matrix)

    return result


if "__name__" == "__main__":
    print(forward_kinematics())
