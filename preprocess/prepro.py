import cv2
import numpy as np
import copy
import imutils
from skimage import img_as_ubyte

from matplotlib import pyplot as plt


# load
img = cv2.imread("result.bmp")
copy = copy.deepcopy(img)

# preprocess
blurred = cv2.GaussianBlur(copy, (51, 51), 0)
_, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(thresh, kernel, iterations=1)
canny = cv2.Canny(erosion, 75, 200)
cv2.imshow("", canny)
cv2.waitKey(0)
# find lines
min_line_lengh = 100
max_line_gap = 20
# lines_p = cv2.HoughLinesP(
#     canny, 1, np.pi / 180, 100, minLineLength=min_line_lengh, maxLineGap=max_line_gap,
# )
# print(lines_p[0])
# for x1, y1, x2, y2 in lines_p[0]:
#     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)


lines = cv2.HoughLines(canny, 1, np.pi / 180, 200)
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# find countours
cnt = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnt)
# cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
black = np.zeros_like(img)
for c in cnts:
    # print(cv2.contourArea(c))
    if cv2.contourArea(c) > 1000:
        cv2.drawContours(black, [c], -1, (0, 255, 0), 5)

cv2.imwrite("cnt.jpg", black)
cv2.imwrite("lines.jpg", img)
