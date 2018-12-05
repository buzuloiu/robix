import numpy as np
import sys
from frames.config import config

def _compute_trpy_evolving(t_x, t_y, t_z, r_z, r_y, r_x):
    return np.array([[np.cos(r_z)*np.cos(r_y), ((np.cos(r_z)*np.sin(r_y)*np.sin(r_x))-(np.sin(r_z)*np.cos(r_x))), ((np.cos(r_z)*np.sin(r_y)*np.cos(r_x))+(np.sin(r_z)*np.sin(r_x))), t_x],
                     [np.sin(r_z)*np.cos(r_y), ((np.sin(r_z)*np.sin(r_y)*np.sin(r_x))+(np.cos(r_z)*np.cos(r_x))), ((np.sin(r_z)*np.sin(r_y)*np.cos(r_x))-(np.cos(r_z)*np.sin(r_x))), t_y],
                     [   -1*np.sin(r_y),                               np.cos(r_y)*np.sin(r_x),                                 np.cos(r_y)*np.cos(r_x),                             t_z],
                     [         0,                                                0,                                                        0,                                         1 ]])


def _compute_a_matrix(name, degrees):
    l = config[name]['l']
    d = config[name]['d']
    alpha = np.deg2rad(config[name]['alpha'])
    theta = np.deg2rad((degrees*config[name]['theta_sign'])+config[name]['theta_offset'])
    return np.array([[np.cos(theta), (-1*np.sin(theta)*np.cos(alpha)),  (np.sin(theta)*np.sin(alpha)),   l*np.cos(theta)],
                     [np.sin(theta),    np.cos(theta)*np.cos(alpha),   (-1*np.cos(theta)*np.sin(alpha)), l*np.sin(theta)],
                     [      0,                 np.sin(alpha),                 np.cos(alpha),                   d        ],
                     [      0,                       0,                            0,                          1        ]])

if __name__ == "__main__":
    x, y, z, r, p, y = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    print(_compute_trpy_evolving(x, y, z, r, p, y))
