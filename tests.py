import numpy as np
from kinematics.forward  import convert_robix_to_degrees, convert_degrees_to_robix

angle = 45 # 45 - 90*np.random.rand()
print angle
robix = convert_degrees_to_robix(angle, name='theta_1')
print robix
print convert_robix_to_degrees(robix, name='theta_1')
