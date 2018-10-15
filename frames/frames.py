import numpy as np


def _compute_trpy_evolving(t_x, t_y, t_z, r_z, r_y, r_x):
    return np.array([[np.cos(r_z)*np.cos(r_y),
                      ((np.cos(r_z)*np.sin(r_y)*np.sin(r_x))-(np.sin(r_z)*np.cos(r_x))),
                      ((np.cos(r_z)*np.sin(r_y)*np.cos(r_x))+(np.sin(r_z)*np.sin(r_x))),
                      t_x],
                     [np.sin(r_z)*np.cos(r_y),
                      ((np.sin(r_z)*np.sin(r_y)*np.sin(r_x))+(np.cos(r_z)*np.cos(r_x))),
                      ((np.sin(r_z)*np.sin(r_y)*np.cos(r_x))-(np.cos(r_z)*np.sin(r_x))),
                      t_y],
                     [-1*np.sin(r_y),
                      np.cos(r_y)*np.sin(r_x),
                      np.cos(r_y)*np.cos(r_x), t_z],
                     [0, 0, 0, 1]])


def _compute_a_matrix(l, d, alpha, theta):
    alpha = np.deg2rad(alpha)
    theta = np.deg2rad(theta)
    return np.array([[np.cos(theta),
                      (-1*np.sin(theta)*np.cos(alpha)),
                      (np.sin(theta)*np.cos(alpha)),
                      (l*np.cos(theta))],
                     [np.sin(theta),
                      np.cos(theta)*np.cos(alpha),
                      (-1*np.cos(theta)*np.sin(alpha)),
                      l*np.sin(theta)],
                     [0,
                      np.sin(alpha),
                      np.cos(alpha),
                      d],
                     [0, 0, 0, 1]])
