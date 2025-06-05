import math
import numpy as np


def compute_D(n):
    D = np.zeros((n, n))
    alpha = 1 / math.sqrt(n)
    for k in range(n):
        for j in range(n):
            D[k, j] = alpha * np.cos(k * np.pi * ((2 * j + 1) / (2 * n)))
        alpha = math.sqrt(2) / math.sqrt(n)
    return D


def DCT1D(D, f_camp):
    return np.dot(D, f_camp)


def IDCT1D(D, c):
    return np.dot(D.transpose(), c)


def main_DCT1D(f_camp):
    D = compute_D(len(f_camp))
    DCT1D(D, f_camp)
