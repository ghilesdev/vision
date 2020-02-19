import cv2
from matplotlib import pyplot as plt
from imutils import auto_canny
import numpy as np

img = cv2.imread("image.bmp")
# taking only one channel because the three channels are already in gray
img = img[:, :, 0]
equalized = cv2.equalizeHist(img)
canny = cv2.Canny(equalized, 50, 255)
houghp = cv2.HoughLinesP(
    equalized, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10
)

for x1, y1, x2, y2 in houghp[0]:
    cv2.line(equalized, (x1, y1), (x2, y2), (0, 255, 0), 1)
plt.imshow(equalized)

# autocanny = auto_canny(equalized)

# plt.subplot(1, 2, 1)
# plt.imshow(canny, cmap="gray")
# plt.subplot(1, 2, 2)
# plt.imshow(autocanny, cmap="gray")

# plt.imshow(equalized, cmap="gray")
# cv2.imwrite("equalized.bmp", equalized)
# cv2.imshow("img", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# print(img.shape)
