import numpy as np

from sympy import Symbol, cos, sin, asin, acos, atan
from sympy.matrices import Matrix, eye
from sympy.printing import latex
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
