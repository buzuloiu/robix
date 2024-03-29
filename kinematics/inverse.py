from kinematics.config import robix
from kinematics.forward import forward_kinematics, convert_robix_to_degrees, convert_degrees_to_robix
from scipy.spatial.distance import euclidean
import numpy as np


def asind(input):
    return np.degrees(np.real(np.arcsin(input+0j)))


def acosd(input):
    return np.degrees(np.real(np.arccos(input+0j)))


def arccos(x):
    y = np.arccos(x + 0j)
    return np.real(y)


def final_angle(theta_1_2, deg_thetas, target):
    thetas = [convert_robix_to_degrees(theta_1_2[0], name='theta_1'), convert_robix_to_degrees(theta_1_2[1], name='theta_2')] + deg_thetas
    actual = np.matmul(forward_kinematics(thetas), np.array([[0], [0], [0], [1]]))
    return euclidean(target, actual.reshape(4))


def cosd(degrees):
    return np.cos(np.deg2rad(degrees))


def sind(degrees):
    return np.sin(np.deg2rad(degrees))


def atan2d(x1, x2):
    angle = np.degrees(np.real(np.arctan2(x1, x2)))
    return angle


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
    T4 = acosd(-1*q33)-T3-90

    # Theta 5
    T5 = atan2d(-1*q32, q31)-10

    m = (q11)/((q23/q13)*sind(T5+10)-q33*cosd(T5+10))

    n = (q12)/(cosd(T5+10)+(q13/q23)*q33*sind(T5+10))

    T1 = atan2d((q24-10*q23-l3*n*cosd(T3)-l2*n),
                (q14-10*q13-l3*m*cosd(T3)-l2*m))

    T2 = atan2d(q23, q13)-T1


    t = [np.round(-1*np.real(T1), 1),
         np.round(-1*np.real(T2), 1),
         np.round(-1*np.real(T3), 1),
         np.round(np.real(T4), 1),
         np.round(-1*np.real(T5), 1)]

    for item in t:
        _item = _item = np.round(item, 1)
        if not (_item >= robix['theta_{}'.format(t.index(item)+1)]['min'] and _item <= robix['theta_{}'.format(t.index(item)+1)]['max']):
            error = ValueError("calculated theta_{} = {} out of range [{}, {}]: not a valid robot config"
                             .format(t.index(item)+1, item, robix['theta_{}'.format(t.index(item)+1)]['min'],
                                     robix['theta_{}'.format(t.index(item)+1)]['max']))
            raise(error)
    

    t_robix = t
    for i in range(len(t)):
        t_robix[i] = convert_degrees_to_robix('theta_{}'.format(i+1), t[i])

    return t_robix


if __name__ == "__main__":
    np.set_printoptions(suppress=True)

    NUM_TRIALS = 100

    actual_thetas = []
    predicted_thetas = []
    theta_x_acc = []
    errors = 0

    for thetas in 60 - 120*np.random.rand(NUM_TRIALS, 5):

        # t = np.matmul(forward, np.array([[0], [0], [0], [1]]))
        # print t
        # actual_thetas.append(t)
        print("input angles: {}".format(np.round(thetas, 2)))
        thetas_robix = []
        for i in range(len(thetas)):
            thetas_robix.append(convert_degrees_to_robix('theta_{}'.format(i+1), thetas[i]))
        print("input robix: {}".format(thetas_robix))
        try:
            forward = forward_kinematics(thetas)
            predicted = inverse_kinematics(forward)
            actual_thetas.append(thetas_robix)
            predicted_thetas.append(predicted)
            print("predicted inverse robix: {}".format(predicted))
        except ValueError as e:
            print(e)
            errors += 1
    print("errors: {}".format(errors))

    predicted_thetas = np.array(predicted_thetas)
    print(np.absolute(np.array(actual_thetas) - predicted_thetas).max(axis=0))
