import numpy as np

from camera.object_detector import ObjectDetector
from camera.stream import stream
from kinematics.forward import convert_degrees_to_robix
from kinematics.inverse import inverse_kinematics

def trpy_evolving(x, y, z, r_z, r_y, r_x):
    r_z = np.deg2rad(r_z)
    r_y = np.deg2rad(r_y)
    r_x = np.deg2rad(r_x)
    return np.array([[np.cos(r_z)*np.cos(r_y), ((np.cos(r_z)*np.sin(r_y)*np.sin(r_x))-(np.sin(r_z)*np.cos(r_x))), ((np.cos(r_z)*np.sin(r_y)*np.cos(r_x))+(np.sin(r_z)*np.sin(r_x))),  x],
                     [np.sin(r_z)*np.cos(r_y), ((np.sin(r_z)*np.sin(r_y)*np.sin(r_x))+(np.cos(r_z)*np.cos(r_x))), ((np.sin(r_z)*np.sin(r_y)*np.cos(r_x))-(np.cos(r_z)*np.sin(r_x))),  y],
                     [   -1*np.sin(r_y),                               np.cos(r_y)*np.sin(r_x),                                 np.cos(r_y)*np.cos(r_x),                              z],
                     [         0,                                                0,                                                        0,                                         1]])

def generate_robix_command(thetas):
    return "MOVE 1 TO {}, 2 TO {}, 3 TO {}, 4 TO {}, 5 TO {}, 6 TO {};".format(
        convert_degrees_to_robix('theta_1', thetas[0]),
        convert_degrees_to_robix('theta_2', thetas[1]),
        convert_degrees_to_robix('theta_3', thetas[2]),
        convert_degrees_to_robix('theta_4', thetas[3]),
        convert_degrees_to_robix('theta_5', thetas[4]),
        convert_degrees_to_robix('theta_6', thetas[5]),
    )

def pick_and_place(block, slot):
    try:
        locate_block = inverse_kinematics(trpy_evolving(block['center'][0], block['center'][1], 4.5, block['orientation'], 90, 0))
        pick_block   = inverse_kinematics(trpy_evolving(block['center'][0], block['center'][1], 2.5, block['orientation'], 45, 0))
    except:
        print '{} is out of workspace'.format(block['class'])
        return ''

    try:
        locate_slot  = inverse_kinematics(trpy_evolving(slot['center'][0], slot['center'][1], 4.5, slot['orientation'], 90, 0))
        place_slot   = inverse_kinematics(trpy_evolving(slot['center'][0], slot['center'][1], 2.5, slot['orientation'], 45, 0))
    except:
        print '{} is out of workspace'.format(slot['class'])
        return ''

    # pick and place routine
    cmd=''
    cmd += generate_robix_command(locate_block + [-1400])
    cmd += generate_robix_command(pick_block + [-1400])
    cmd += generate_robix_command(pick_block + [1400])
    cmd += generate_robix_command(locate_block + [1400])
    cmd += generate_robix_command(locate_slot + [1400])
    cmd += generate_robix_command(place_slot + [1400])
    cmd += generate_robix_command(place_slot + [-1400])
    cmd += generate_robix_command(locate_slot + [-1400])
    return cmd

if __name__ == '__main__':
    object_detector = ObjectDetector()
    regions = object_detector.clasified_regions(stream.read()[1])
    regions = map(object_detector.wrt_base, regions)
    for region in regions:
        print region
    blocks = [ region for region in regions if region['class'].endswith('block') ]
    slots = [ region for region in regions if region['class'].endswith('slot') ]

    cmd=''
    for block in blocks:
        block_type = block['class'].split('_')[0]
        slot = [slot for slot in slots if slot['class'].startswith(block_type)]
        if len(slot) < 0:
            print 'could not find slot for {}'.format(block['class'])
            continue

        cmd += pick_and_place(block, slot[0])

    print cmd
