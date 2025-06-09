import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../model')))
from utils import read_img, show_imgs
from compression_scipyDCT import compress_scipy, decompress_scipy

def main(file_path, F, d):
    # Load the image from file_path into a matrix
    print("Reading image file...")
    Mat = read_img(file_path)
    Mt1 = Mat.copy()
    
    # Compress the image
    print("Compressing...")
    mc = compress_scipy(Mat, F, d)
    
    # Decompress the compressed image
    print("Decompressing...")
    mu = decompress_scipy(mc, F)
    
    # Display the original and decompressed images
    print("Showing images...")
    show_imgs(Mt1, mu, "Original photo", "Rebuilt photo")