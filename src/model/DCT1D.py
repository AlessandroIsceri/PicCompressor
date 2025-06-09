import math
import numpy as np


def compute_D(n):
    """
    Compute the DCT (Discrete Cosine Transform) matrix of size n x n.
    """
    D = np.zeros((n, n))
    alpha = 1 / math.sqrt(n)
    for k in range(n):
        for j in range(n):
            D[k, j] = alpha * np.cos(k * np.pi * ((2 * j + 1) / (2 * n)))
        alpha = math.sqrt(2) / math.sqrt(n)
    return D


def DCT1D(D, f_camp):
    """
    Compute the 1D Discrete Cosine Transform of the input vector f_camp
    using the precomputed DCT matrix D.
    """
    return np.dot(D, f_camp)


def IDCT1D(D, c):
    """
    Compute the inverse 1D Discrete Cosine Transform of the coefficient vector c
    by multiplying with the transpose of the DCT matrix D.
    """
    return np.dot(D.transpose(), c)


def main_DCT1D(f_camp):
    D = compute_D(len(f_camp))
    DCT1D(D, f_camp)
