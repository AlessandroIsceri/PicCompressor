from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


def read_img(file_path):
    im = Image.open(file_path).convert("L")
    data = np.array(im.getdata()).reshape(im.size[1], im.size[0])
    return data


def show_imgs(matrix1, matrix2, title1, title2):
    img1 = Image.fromarray(matrix1)
    img2 = Image.fromarray(matrix2)

    # grid 1x2 (1 row, 2 cols)
    _, axes = plt.subplots(1, 2, figsize=(12, 4))

    # show each image in a subplot
    axes[0].imshow(img1, cmap='gray')
    axes[0].set_title(title1)
    axes[0].axis('off')

    axes[1].imshow(img2, cmap='gray')
    axes[1].set_title(title2)
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()


def cut(C, threshold):
    C_copy = C.copy()
    for i in range(len(C_copy)):
        for j in range(len(C_copy[0])):
            if i + j >= threshold:
                C_copy[i][j] = 0
    return C_copy


def clip_and_round(B):
    B = B.round(decimals=0)
    for i in range(len(B)):
        for j in range(len(B[0])):
            if B[i][j] < 0:
                B[i][j] = 0
            elif B[i][j] > 255:
                B[i][j] = 255
    return B