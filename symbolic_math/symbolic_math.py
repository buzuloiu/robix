from sympy import Symbol, cos, sin, asin, acos, atan
from sympy import *
from sympy.printing import latex
from sympy.matrices import Matrix, eye
from numpy import deg2rad
from sympy.solvers import solve

t_1 = Symbol('theta_1')
t_2 = Symbol('theta_2')
t_3 = Symbol('theta_3')
t_4 = Symbol('theta_4')
t_5 = Symbol('theta_5')

d_1 = Symbol('d_1')
d_2 = Symbol('d_2')
d_3 = Symbol('d_3')
d_4 = Symbol('d_4')
d_5 = Symbol('d_5')

l_1 = Symbol('l_1')
l_2 = Symbol('l_2')
l_3 = Symbol('l_3')
l_4 = Symbol('l_4')
l_5 = Symbol('l_5')

a_1 = Symbol('alpha_1')
a_2 = Symbol('alpha_2')
a_3 = Symbol('alpha_3')
a_4 = Symbol('alpha_4')
a_5 = Symbol('alpha_5')

q_23 = Symbol('Q_23')
q_24 = Symbol('Q_24')
q_31 = Symbol('Q_31')
q_32 = Symbol('Q_32')
q_34 = Symbol('Q_34')
q_33 = Symbol('Q_33')


subs = [
    (a_1, deg2rad(0)),
    (a_2, deg2rad(90)),
    (a_3, deg2rad(0)),
    (a_4, deg2rad(90)),
    (a_5, deg2rad(0)),
    (d_1, 16.39),
    (d_2, 0),
    (d_3, 0),
    (d_4, 0),
    (d_5, 10),
    (l_1, 9.28),
    (l_2, 9.15),
    (l_3, 5.74),
    (l_4, 0),
    (l_5, 0),
]


def a_matrix(theta, alpha, l, d):
    return Matrix([[cos(theta), -1*(sin(theta)*cos(alpha)), sin(theta)*sin(alpha), l*cos(theta)],
                   [sin(theta), cos(theta)*cos(alpha), -1*cos(theta)*sin(alpha), l*sin(theta)],
                   [0, sin(alpha), cos(alpha), d],
                   [0, 0, 0, 1]])


def round_expr(expr, num_digits):
    return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})


output = eye(4)
a_matrices = [a_matrix(t_1, a_1, l_1, d_1),
              a_matrix(t_2, a_2, l_2, d_2),
              a_matrix(t_3, a_3, l_3, d_3),
              a_matrix(t_4, a_4, l_4, d_4),
              a_matrix(t_5, a_5, l_5, d_5)]

for matrix in a_matrices:
    output = output*matrix

# q1
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
