from math import atan2, cos, sin, sqrt, pi
import cv2
import math
import numpy as np
import os
from image_tools.dxf_to_png import OUTPUT_PATH, SOURCE_PATH

source_path = SOURCE_PATH
prod_path = OUTPUT_PATH


def hu_moment_calculate(img):
    """
        takes an img as an argument and calculates its HuMoments
    """
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    moments = cv2.moments(thresh)
    hu_moments = cv2.HuMoments(moments)

    for i in range(0, 7):
        hu_moments[i][0] = np.round(
            (
                -1
                * math.copysign(1.0, hu_moments[i][0])
                * math.log10(abs(hu_moments[i][0]))
            ),
            3,
        )
    return hu_moments


def check_symilarity(i1, i2):
    """
        check similarity between two images using Hull Moments
    """

    hu1 = hu_moment_calculate(i1)
    hu2 = hu_moment_calculate(i2)
    # error margin
    epsilon = 0.001
    if (
        hu2[0][0] - epsilon < hu1[0][0] < hu2[0][0] + epsilon
        or hu1[0][0] - epsilon < hu2[0][0] < hu1[0][0] + epsilon
    ):
        print(f"the shapes {i1} and {i2} ares similar")

    if hu1[6][0] == -1 * math.copysign(1, hu2[6][0]) * hu2[6][0]:
        print(f"shape{i1} and {i2} are symmetrical")


def absoluteFilePaths(directory):
    """
        returns filenames with absolute path
    """
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def main():
    source_files = list(absoluteFilePaths(source_path))
    prod_files = list(absoluteFilePaths(prod_path))
    for s in source_files:
        for p in prod_files:
            check_symilarity(s, p)


if __name__ == "__main__":
    main()
