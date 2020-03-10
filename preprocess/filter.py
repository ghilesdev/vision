import cv2
import numpy as np

img = cv2.imread("result.bmp")
blurred = cv2.GaussianBlur(img, (15, 15), 15)
ker = np.ones((5, 5), dtype=np.uint8)
errode = cv2.erode(blurred, ker)
cv2.imwrite("errod.bmp", errode)
