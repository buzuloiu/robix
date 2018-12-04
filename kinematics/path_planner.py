from camera.object_detector import ObjectDetector
from kinematics.forward import convert_degrees_to_robix

def trpy_evolving(x, y, z, r_z, r_y, r_x):
    return np.array([[np.cos(r_z)*np.cos(r_y), ((np.cos(r_z)*np.sin(r_y)*np.sin(r_x))-(np.sin(r_z)*np.cos(r_x))), ((np.cos(r_z)*np.sin(r_y)*np.cos(r_x))+(np.sin(r_z)*np.sin(r_x))),  t],
                     [np.sin(r_z)*np.cos(r_y), ((np.sin(r_z)*np.sin(r_y)*np.sin(r_x))+(np.cos(r_z)*np.cos(r_x))), ((np.sin(r_z)*np.sin(r_y)*np.cos(r_x))-(np.cos(r_z)*np.sin(r_x))),  t],
                     [   -1*np.sin(r_y),                               np.cos(r_y)*np.sin(r_x),                                 np.cos(r_y)*np.cos(r_x),                              t],
                     [         0,                                                0,                                                        0,                                         1]])


def generate_robix_command(theta1, theta2, theta3, theta4, theta5, theta6):
    return "MOVE 1 TO {}, 2 TO {}, 3 TO {}, 4 TO {}, 5 TO {}, 6 TO {};\n".format(
        convert_degrees_to_robix('theta1', theta1),
        convert_degrees_to_robix('theta2', theta2),
        convert_degrees_to_robix('theta3', theta3),
        convert_degrees_to_robix('theta4', theta4),
        convert_degrees_to_robix('theta5', theta5),
        convert_degrees_to_robix('theta6', theta6),
    )

def pick_and_place(block, slot):
    locate_block = trpy_evolving()
    pick_block   = trpy_evolving()
    locate_slot  = trpy_evolving()
    place_slot   = trpy_evolving()

    cmd=''
    cmd += generate_robix_command(*locate_block, -1400)

if __name__ == '__main__':
    object_detector = ObjectDetector()
    regions = object_detector.clasified_regions()

    blocks = [ region for region in regions if region['class'].endswith('block') ]
    slots = [ region for region in regions if region['class'].endswith('slot') ]

    cmd=''
    for block in blocks:
        block_type = block['class'].split('_')[0]
        slot = [slot for slot in slots if slot['class'].startswith(block_type)][0]

        cmd += pick_and_place(block, slot)
