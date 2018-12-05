import numpy as np
from kinematics.forward  import convert_robix_to_degrees, convert_degrees_to_robix

robixs = 1400-2800*np.random.rand(5) # 45 - 90*np.random.rand()
print 'Robix {}'.format(robixs)
angles = convert_robix_to_degrees(robixs)
print 'Angle {}'.format(angles)
print 'Robix {}'.format(convert_degrees_to_robix(angles))
