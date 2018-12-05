import numpy as np

from sympy import trigsimp, simplify, Symbol, cos, sin, asin, acos, atan
from sympy.matrices import Matrix, eye
from sympy.printing import latex
from sympy.solvers import solve
config = {
    'theta_1': {'min': -80.0, 'max': 80.0, 'offset': 0, 'l': 9.28, 'd': 16.39, 'alpha':  0.0, 'theta_offset': 0,  'theta_sign': -1},
    'theta_2': {'min': -80.0, 'max': 75.0, 'offset': 0, 'l': 9.15, 'd': 0,     'alpha': 90.0, 'theta_offset': 0,  'theta_sign': -1},
    'theta_3': {'min': -80.0, 'max': 85.0, 'offset': 0, 'l': 5.74, 'd': 0,     'alpha':  0.0, 'theta_offset': 0,  'theta_sign': -1},
    'theta_4': {'min': -85.0, 'max': 85.0, 'offset': 0, 'l':  0.0, 'd': 0,     'alpha': 90.0, 'theta_offset': 90, 'theta_sign':  1},
    'theta_5': {'min': -75.0, 'max': 75.0, 'offset': 0, 'l':  0.0, 'd': 10,    'alpha':  0.0, 'theta_offset': 10, 'theta_sign': -1}
}



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
a_matrices = [a_matrix(t_1, np.deg2rad(config['theta_1']['alpha']), config['theta_1']['l'], config['theta_1']['d']),
              a_matrix(t_2, np.deg2rad(config['theta_2']['alpha']), config['theta_2']['l'], config['theta_2']['d']),
              a_matrix(t_3, np.deg2rad(config['theta_3']['alpha']), config['theta_3']['l'], config['theta_3']['d']),
              a_matrix(t_4, np.deg2rad(config['theta_4']['alpha']), config['theta_4']['l'], config['theta_4']['d']),
              a_matrix(t_5, np.deg2rad(config['theta_5']['alpha']), config['theta_5']['l'], config['theta_5']['d'])]

for matrix in a_matrices:
    output = output*matrix
print(latex(simplify(trigsimp(output[0,0]))) +'\n')
print(latex(simplify(trigsimp(output[0,1]))) +'\n')
print(latex(simplify(trigsimp(output[0,2]))) +'\n')
print(latex(simplify(trigsimp(output[0,3]))) +'\n')
print(latex(simplify(trigsimp(output[1,0]))) +'\n')
print(latex(simplify(trigsimp(output[1,1]))) +'\n')
print(latex(simplify(trigsimp(output[1,2]))) +'\n')
print(latex(simplify(trigsimp(output[1,3]))) +'\n')
print(latex(simplify(trigsimp(output[2,0]))) +'\n')
print(latex(simplify(trigsimp(output[2,1]))) +'\n')
print(latex(simplify(trigsimp(output[2,2]))) +'\n')
print(latex(simplify(trigsimp(output[2,3]))) +'\n')
#q1
q_1 = asin(((q_24-d_5*q_23-((l_3*q_23))/sin(t_3+t_4))-(l_2*q_23/sin(t_3+t_4)))/l_1)

q_2 = asin((q_23)/(sin(t_3+t_4)))-t_1

q_3 = asin((q_34-d_5*q_33-d_1)/l_3)

q_4 = asin(q_33)-t_3

q_5 = atan(-1*q_32/q_31)

'''
print(latex((round_expr(output.subs(subs), 2))))
print(latex(q_1))
print(latex(q_2))
print(latex(q_3))
print(latex(q_4))
print(latex(q_5))
'''
