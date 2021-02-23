import cv2
import numpy as np
from window import *

HWND = getHandle("阴阳师-网易游戏")
# 读取图片
captured = captureWindowAs(HWND, "cache/cache.png")

src = captured
cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
cv2.imshow("input", src)
"""
提取图中的红色部分
"""
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
low_hsv = np.array([3, 220, 220])
high_hsv = np.array([50, 255, 255])
mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
cv2.imshow("test", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
