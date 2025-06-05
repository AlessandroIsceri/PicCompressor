import numpy as np

from DCT1D import DCT1D, IDCT1D, compute_D


def DCT2D(F, D):
    n = len(F)
    C = F.copy()
    for j in range(n):
        C[:, j] = DCT1D(D, C[:, j])
    for i in range(n):
        C[i, :] = DCT1D(D, C[i, :].transpose()).transpose()
    return C


def IDCT2D(F, D):
    n = len(F)
    C = F.copy()
    for j in range(n):
        C[:, j] = IDCT1D(D, C[:, j])
    for i in range(n):
        C[i, :] = IDCT1D(D, C[i, :].transpose()).transpose()
    return C


def main_DCT2D(F):
    n = len(F)
    D = compute_D(n)
    C = DCT2D(F, D)
    return C