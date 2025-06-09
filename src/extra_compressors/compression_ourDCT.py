from DCT1D import compute_D
from DCT2D import DCT2D, IDCT2D
import numpy as np
from utils import clip_and_round, cut


def compress_our(F, block_dim, threshold):
    """
    Compress an image using 2D Discrete Cosine Transform (DCT) and coefficient thresholding.
    
    Parameters:
    - F: 2D numpy array representing the grayscale image.
    - block_dim: Dimension of the square blocks to divide the image into.
    - threshold: Integer value to set to zero all elements in in each block whose indexes satisfy i + j >= threshold in each block.
    
    Returns:
    - compressed_pic: 2D numpy array containing the compressed pic.
    
    Procedure:
    1. Shift image pixel values by subtracting 128.
    2. Divide image into non-overlapping blocks of size block_dim x block_dim.
    3. Apply 2D DCT on each block.
    4. Set to zero all elements in each block whose indexes satisfy i + j >= threshold.
    5. Store the truncated DCT coefficients into the compressed image array.
    """
    n = len(F)
    m = len(F[0])

    # Adjust pic's values
    F -= 128
    D = compute_D(block_dim)

    # Divide pic into blocks
    n_rows = n // block_dim
    n_cols = m // block_dim

    compressed_pic = np.zeros((n_rows * block_dim, n_cols * block_dim))
    cur_row = 0
    for _ in range(n_rows):
        cur_col = 0
        for _ in range(n_cols):
            # Extract block
            B = F[cur_row:cur_row + block_dim, cur_col: cur_col + block_dim]
            
            # Apply 2D DCT to block B
            C = DCT2D(B, D)
            C = C.round(decimals=0)
            
            # Delete coefficients based on the threshold
            C_cut = cut(C, threshold)
            
            # Store compressed block
            compressed_pic[cur_row:cur_row + block_dim,
                           cur_col: cur_col + block_dim] = C_cut
            cur_col = cur_col + block_dim
        cur_row = cur_row + block_dim

    return compressed_pic


def decompress_our(C, block_dim):
    """
    Decompress an image using IDCT2D.
    
    Parameters:
    - C: 2D numpy array (compressed pic).
    - block_dim: Dimension of the square blocks used during compression.
    
    Returns:
    - decompressed_pic: 2D numpy array representing the decompressed grayscale image.
    
    Procedure:
    1. Divide the compressed pic into blocks.
    2. Apply 2D inverse DCT on each block.
    3. Shift pixel values back by adding 128.
    4. Clip values to valid image pixel range [0,255] and round.
    5. Bebuild the full image using decompressed blocks.
    """
    n = len(C)
    m = len(C[0])

    D = compute_D(block_dim)

    # Divide pic into blocks
    n_rows = n // block_dim
    n_cols = m // block_dim

    decompressed_pic = np.zeros((n_rows * block_dim, n_cols * block_dim))
    cur_row = 0
    for _ in range(n_rows):
        cur_col = 0
        for _ in range(n_cols):
            # Extract block
            B = C[cur_row:cur_row + block_dim, cur_col: cur_col + block_dim]
            
            # Apply IDCT2 to block B
            B = IDCT2D(B, D)
            B += 128
            B = clip_and_round(B)
            
            # Store decompressed block
            decompressed_pic[cur_row:cur_row + block_dim,
                             cur_col: cur_col + block_dim] = B
            cur_col = cur_col + block_dim
        cur_row = cur_row + block_dim

    return decompressed_pic