global config

config = {
    'theta1': {'min': -80.0, 'max': 80.0, 'offset': 95.7, 'l': 9.28, 'd': 16.39, 'alpha':  0.0, 'theta_offset': 0, 'theta_sign':-1},
    'theta2': {'min': 0,     'max':    1, 'offset':    1, 'l': 9.15, 'd':  0, 'alpha': 90.0, 'theta_offset': 0, 'theta_sign':-1},
    'theta3': {'min': 0,     'max':    1, 'offset':    1, 'l': 5.74, 'd':   0.0, 'alpha':  0.0, 'theta_offset': 0, 'theta_sign':-1},
    'theta4': {'min': 0,     'max':    1, 'offset':    1, 'l':  0.0, 'd': 0, 'alpha': 90.0, 'theta_offset': 90, 'theta_sign':1},
    'theta5': {'min': 0,     'max':    1, 'offset':    1, 'l':  0.0, 'd':  10, 'alpha':  0.0, 'theta_offset': 10, 'theta_sign':-1}
}

thetas = [
    ['theta1', 90],
    ['theta2', -90],
    ['theta3',-45],
    ['theta4', -80],
    ['theta5', 0]
]
