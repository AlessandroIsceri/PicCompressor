from DCT1D import compute_D
from DCT2D import DCT2D, IDCT2D
import numpy as np
from utils import clip_and_round, cut


def compress_our(F, block_dim, threshold):
    n = len(F)
    m = len(F[0])

    # adjust pic's values
    F -= 128
    D = compute_D(block_dim)

    # divide pic into blocks
    n_rows = n // block_dim
    n_cols = m // block_dim

    compressed_pic = np.zeros((n_rows * block_dim, n_cols * block_dim))
    cur_row = 0
    for _ in range(n_rows):
        cur_col = 0
        for _ in range(n_cols):
            B = F[cur_row:cur_row + block_dim, cur_col: cur_col + block_dim]
            
            # execute DCT2 on block B
            C = DCT2D(B, D)
            C = C.round(decimals=0)
            C_cut = cut(C, threshold)
            compressed_pic[cur_row:cur_row + block_dim,
                           cur_col: cur_col + block_dim] = C_cut
            cur_col = cur_col + block_dim
        cur_row = cur_row + block_dim

    return compressed_pic


def decompress_our(C, block_dim):
    n = len(C)
    m = len(C[0])

    D = compute_D(block_dim)

    n_rows = n // block_dim
    n_cols = m // block_dim

    decompressed_pic = np.zeros((n_rows * block_dim, n_cols * block_dim))
    cur_row = 0
    for _ in range(n_rows):
        cur_col = 0
        for _ in range(n_cols):
            B = C[cur_row:cur_row + block_dim, cur_col: cur_col + block_dim]
            
            # execute IDCT2 on block B
            B = IDCT2D(B, D)
            B += 128
            B = clip_and_round(B)

            decompressed_pic[cur_row:cur_row + block_dim,
                             cur_col: cur_col + block_dim] = B
            cur_col = cur_col + block_dim
        cur_row = cur_row + block_dim

    return decompressed_pic