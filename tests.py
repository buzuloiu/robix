import pytest
import numpy as np
from frames import frames


def test_trpy_zeros():
    matrix = frames._compute_trpy_evolving(0, 0, 0, 0, 0, 0)
    assert np.allclose(matrix, np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1]]))


def test_trpy_ones():
    matrix = frames._compute_trpy_evolving(1, 1, 1, 1, 1, 1)
    assert np.allclose(matrix, np.array([[0.2919, -0.0721, 0.9537, 1],
                                         [0.4546, 0.8877, -0.0721, 1],
                                         [-0.8414, 0.4546, 0.2919, 1],
                                         [0, 0, 0, 1]]),
                       rtol=1.e-5, atol=1.e-4)


def test_a_matrix_zeros():
    matrix = frames._compute_a_matrix(0, 0, 0, 0)
    assert np.allclose(matrix, np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1]]),
                       rtol=1.e-5, atol=1.e-4))

def test_we_didnt_totally_fuck_our_config_file():
    matrix = frames._compute_a_matrix(0, 0, 0, 0)
    assert np.allclose(matrix, np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1]]),
                       rtol=1.e-5, atol=1.e-4))
