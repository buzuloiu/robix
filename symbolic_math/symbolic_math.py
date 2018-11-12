from sympy import Symbol, cos, sin
from sympy.printing.latex import print_latex
from sympy.matrices import Matrix

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

a_1 = Matrix([])


e = 1/cos(t_1)
print_latex(e.series(t_1, 0, 10))
