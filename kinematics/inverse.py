from kinematics.config import robix
import numpy as np
import sys


def asind(input):
    print(input)
    input = np.round(input, 5)
    return np.degrees(np.arcsin(input))


def sind(degrees):
    return np.sin(np.deg2rad(degrees))


def cosd(degrees):
    return np.cos(np.deg2rad(degrees))


def atan2d(x1, x2):
    angle = np.degrees(np.arctan2(x1, x2))
    if angle > 0:
        return angle % 180
    if angle < 0:
        return angle % -1*180



def inverse_kinematics(q_matrix):
    q11 = q_matrix[0, 0]
    q12 = q_matrix[0, 1]
    q13 = q_matrix[0, 2]
    q14 = q_matrix[0, 3]
    q21 = q_matrix[1, 0]
    q22 = q_matrix[1, 1]
    q23 = q_matrix[1, 2]
    q24 = q_matrix[1, 3]
    q31 = q_matrix[2, 0]
    q32 = q_matrix[2, 1]
    q33 = q_matrix[2, 2]
    q34 = q_matrix[2, 3]

    # Defining Di and Li
    # Di vaLues
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

    """
    # finding thetas
    """

    # Theta 3
    T3 = asind((q34-d5*q33-d1)/l3)

    # Theta 4
    T4 = asind(q33)-T3

    # Theta 5
    T5 = atan2d(-1*q32, q31)-10

    # Theta Unofficials
    T1 = 0
    T2 = 0
    TA = T1 + T2
    TB = T3 + T4

    # Theta 1
    T1 = asind((q24-d5*sind(TA)*cosd(TB)-l3*sind(TA)*cosd(T3)+d4*cosd(TA)-l2*sind(TA))/l1)

    # Theta 2
    if q31 == 0:
        T2 = atan2d(q23, q13)-T1
    else:
        T2 = asind(q23*cosd(T5)/q31)-T1

    """
    iterate
    """
    TA = T1 + T2
    TB = T3 + T4

    # Theta 1
    T1 = asind((q24-d5*sind(TA)*cosd(TB)-l3*sind(TA)*cosd(T3)+d4*cosd(TA)-l2*sind(TA))/l1)

    # Theta 2

    if q31 == 0:
        T2 = atan2d(q23, q13)-T1

    else:
        T2 = asind(q23*cosd(T5)/q31)-T1
    """
    iterate
    """
    TA = T1 + T2
    TB = T3 + T4

    # Theta 1
    T1 = asind((q24-d5*sind(TA)*cosd(TB)-l3*sind(TA)*cosd(T3)+d4*cosd(TA)-l2*sind(TA))/l1)

    # Theta 2
    if q31 == 0:
        T2 = atan2d(q23, q13)-T1
    else:
        T2 = asind(q23*cosd(T5)/q31)-T1

    """
    # The just incases
    # T2 = acosd(q13/cosd(TA))-T3
    # T2 = acosd(q13*cosd(T5)/q31)-T1
    # T2 = atan2d(q23, q13)-T1
    # T2 = acosd((q13*cosd(atan2d(-q32, q31)))/q31)-T1
    # T2 = asind(q23*cosd(T5)/q31)-T1
    """
    t = [np.round(-1*np.real(T1), 1),
         np.round(-1*np.real(T2), 1),
         np.round(-1*np.real(T3), 1),
         np.round(np.real(T4), 1),
         np.round(-1*np.real(T5), 1)]

    for item in t:
        _item = np.round(item, 1)
        if not (_item >= robix['theta_{}'.format(t.index(item)+1)]['min'] and _item <= robix['theta_{}'.format(t.index(item)+1)]['max']):
            raise ValueError("calculated theta_{} = {} out of range [{}, {}]: not a valid robot config"
                             .format(t.index(item)+1, item, robix['theta_{}'.format(t.index(item)+1)]['min'],
                                     robix['theta_{}'.format(t.index(item)+1)]['max']))
    return t


"""
import numpy as np

from sympy import Symbol, cos, sin, asin, acos, atan
from sympy.matrices import Matrix, eye
from sympy.solvers import solve

t_1 = Symbol('theta_1')
t_2 = Symbol('theta_2')
t_3 = Symbol('theta_3')
t_4 = Symbol('theta_4')
t_5 = Symbol('theta_5')

def a_matrix(theta, alpha, l, d):
    return Matrix([[cos(theta), -1*(sin(theta)*cos(alpha)), sin(theta)*sin(alpha), l*cos(theta)],
                   [sin(theta), cos(theta)*cos(alpha), -1*cos(theta)*sin(alpha), l*sin(theta)],
                   [0, sin(alpha), cos(alpha), d],
                   [0, 0, 0, 1]])

output = eye(4)
a_matrices = [a_matrix(t_1, np.deg2rad(config.robix['theta_1']['alpha']), config.robix['theta_1']['l'], config.robix['theta_1']['d']),
              a_matrix(t_2, np.deg2rad(config.robix['theta_2']['alpha']), config.robix['theta_2']['l'], config.robix['theta_2']['d']),
              a_matrix(t_3, np.deg2rad(config.robix['theta_3']['alpha']), config.robix['theta_3']['l'], config.robix['theta_3']['d']),
              a_matrix(t_4, np.deg2rad(config.robix['theta_4']['alpha']), config.robix['theta_4']['l'], config.robix['theta_4']['d']),
              a_matrix(t_5, np.deg2rad(config.robix['theta_5']['alpha']), config.robix['theta_5']['l'], config.robix['theta_5']['d'])]

for matrix in a_matrices:
    output = output*matrix

#q1
q_1 = asin(((q_24-d_5*q_23-((l_3*q_23))/sin(t_3+t_4))-(l_2*q_23/sin(t_3+t_4)))/l_1)

q_2 = asin((q_23)/(sin(t_3+t_4)))-t_1

q_3 = asin((q_34-d_5*q_33-d_1)/l_3)

q_4 = asin(q_33)-t_3

q_5 = atan(-1*q_32/q_31)


print(latex((round_expr(output.subs(subs), 2))))
print(latex(q_1))
print(latex(q_2))
print(latex(q_3))
print(latex(q_4))
print(latex(q_5))
"""


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    print(np.round(inverse_kinematics(np.matrix([[0.98, -0.17,  0,   18.43],
                                                 [-0.17, -0.98, 0,   0],
                                                 [0,    0,   -1,    2.4],
                                                 [0,    0,    0,    1]])), 2))
