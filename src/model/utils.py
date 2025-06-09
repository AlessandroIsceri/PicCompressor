from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


def read_img(file_path):
    """
    Reads an image from file_path, converts it to grayscale,
    and returns it as a 2D numpy array.
    """
    im = Image.open(file_path).convert("L")
    data = np.array(im.getdata()).reshape(im.size[1], im.size[0])
    return data


def show_imgs(matrix1, matrix2, title1, title2):
    """
    Displays two grayscale images side-by-side for visual comparison.
    matrix1, matrix2: 2D numpy arrays representing images.
    title1, title2: Titles for the respective images.
    """
    img1 = Image.fromarray(matrix1)
    img2 = Image.fromarray(matrix2)

    # Create a 1x2 grid for image display
    _, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Show first image
    axes[0].imshow(img1, cmap='gray')
    axes[0].set_title(title1)
    axes[0].axis('off')

    # Show second image
    axes[1].imshow(img2, cmap='gray')
    axes[1].set_title(title2)
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()


def cut(C, threshold):
    """
    Sets to zero all elements in matrix C whose indices satisfy i + j >= threshold.
    Returns the processed matrix.
    """
    C_copy = C.copy()
    for i in range(len(C_copy)):
        for j in range(len(C_copy[0])):
            if i + j >= threshold:
                C_copy[i][j] = 0
    return C_copy


def clip_and_round(B):
    """
    Rounds values in matrix B to nearest integer and clips all values to be within [0, 255].
    Returns the processed matrix.
    """
    B = B.round(decimals=0)
    for i in range(len(B)):
        for j in range(len(B[0])):
            if B[i][j] < 0:
                B[i][j] = 0
            elif B[i][j] > 255:
                B[i][j] = 255
    return B