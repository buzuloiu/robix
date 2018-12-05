from kinematics import config
import sys
import numpy as np

def convert_degrees_to_robix(name, degrees):
    if degrees < config.robix[name]['min'] and degrees > config.robix[name]['max']:
        raise Exception('Robix motor "{}" is out of range ({}, {})'.format(name, config.robix[name]['min'], config.robix[name]['max']))
    return int(
        (2800./(config.robix[name]['max'] - config.robix[name]['min']))*degrees
    )

def convert_robix_to_degrees(name, robix):
    robix = int(robix)
    if robix not in range(-1400, 1401):
        raise Exception('Robix motor "{}" is out of range (-1400, 1400)'.format(name))
    return ((config.robix[name]['max'] - config.robix[name]['min'])*(robix))/2800.

def compute_a_matrix(name, degrees):
    l = config.robix[name]['l']
    d = config.robix[name]['d']
    alpha = np.deg2rad(config.robix[name]['alpha'])
    theta = np.deg2rad(config.robix[name]['theta_sign']*degrees+config.robix[name]['theta_offset'])
    return np.array([[np.cos(theta), (-1*np.sin(theta)*np.cos(alpha)),  (np.sin(theta)*np.sin(alpha)),   l*np.cos(theta)],
                     [np.sin(theta),    np.cos(theta)*np.cos(alpha),   (-1*np.cos(theta)*np.sin(alpha)), l*np.sin(theta)],
                     [      0,                 np.sin(alpha),                 np.cos(alpha),                   d        ],
                     [      0,                       0,                            0,                          1        ]])

def forward_kinematics(thetas):
    effector_base = np.eye(4)

    effector_base = np.matmul(effector_base, compute_a_matrix('theta_1', thetas[0]))
    effector_base = np.matmul(effector_base, compute_a_matrix('theta_2', thetas[1]))
    effector_base = np.matmul(effector_base, compute_a_matrix('theta_3', thetas[2]))
    effector_base = np.matmul(effector_base, compute_a_matrix('theta_4', thetas[3]))
    effector_base = np.matmul(effector_base, compute_a_matrix('theta_5', thetas[4]))

    return effector_base


if __name__ == '__main__':
    base = np.array([[0], [0], [0], [1]])
    effector_base = forward_kinematics([int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]),
                                        int(sys.argv[4]), int(sys.argv[5])])

    print ('x: {}'.format(effector_base[0]))
    print ('y: {}'.format(effector_base[1]))
    print ('z: {}'.format(effector_base[2]))
