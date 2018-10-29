from frames import frames
from frames.config import config, thetas
import numpy as np
import sys


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
    a_matrices = np.zeros([5], dtype=object)
    for theta in thetas:
        a_matrices[thetas.index(theta)] = frames._compute_a_matrix(theta[0], theta[1])
    for matrix in a_matrices:
        import pdb; pdb.set_trace()
        result = np.matmul(result, matrix)

    return result


def apply_fwd_kin(x=0, y=0, z=0):
    import pdb; pdb.set_trace()
    return np.matmul(forward_kinematics(), np.array([[x],
                                                     [y],
                                                     [z],
                                                     [1]]))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        x, y, z = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        print(apply_fwd_kin(x, y, z))
    else:
        print(apply_fwd_kin())
