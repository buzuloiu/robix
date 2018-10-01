import numpy as np

def trpy_evolving(t_x, t_y, t_z, r_z, r_y, r_x):
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
