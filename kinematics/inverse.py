from kinematics.config import robix
from frames.frames import _compute_trpy_evolving
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
    if x1 == x2 == 0:
        return 0
    angle = np.degrees(np.arctan2(x1, x2))
    return angle
    """
    if angle > 0:
        return angle % 180
    if angle < 0:
        return angle % -1*180
    """


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
    import pdb; pdb.set_trace()
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


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    #x, y, z, r, p, y = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    x, y, z, r, p, y = 27+0j, 0+0j, 8+0j, 0+0j, 90+0j, 0+0j
    matrix = _compute_trpy_evolving(x, y, z, r, p, y)
    print(matrix)
    print(np.round(inverse_kinematics(matrix)))
