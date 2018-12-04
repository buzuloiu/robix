from kinematics.config import robix
from kinematics.forward import forward_kinematics, convert_robix_to_degrees, convert_degrees_to_robix
import numpy as np
import math
import sys

if __name__ == "__main__":
    TRAIN_SIZE=10000
    TEST_SIZE=1000

    train_labels = np.array(map(convert_robix_to_degrees, 1400 - 2800*np.random.rand(TRAIN_SIZE, 5)))
    train_inputs = np.array(map(forward_kinematics, train_labels))

    from sklearn.tree import DecisionTreeRegressor
    model = DecisionTreeRegressor()
    model.fit(train_inputs.reshape(TRAIN_SIZE, 16), train_labels)

    test_labels = np.array(map(convert_robix_to_degrees, 1400 - 2800*np.random.rand(TEST_SIZE, 5)))
    test_inputs = np.array(map(forward_kinematics, test_labels))
    print model.score(test_inputs, test_labels)

    import pdb; pdb.set_trace()
