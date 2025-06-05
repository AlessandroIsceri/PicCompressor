import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../model')))
from utils import read_img, show_imgs
from compression_scipyDCT import compress_scipy, decompress_scipy

def main(file_path, F, d):
    print("Reading image file...")
    Mat = read_img(file_path)
    Mt1 = Mat.copy()
    print("Compressing...")
    mc = compress_scipy(Mat, F, d)
    print("Decompressing...")
    mu = decompress_scipy(mc, F)
    print("Showing images...")
    show_imgs(Mt1, mu, "Original photo", "Rebuilt photo")