import cv2
import numpy as np
from window import *
from picture import *

HWND = getHandle("阴阳师-网易游戏")
# 读取图片
captured = captureWindowAs(HWND, "cache/cache.png")

src = captured
cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
cv2.imshow("input", src)
"""
提取图中的黄色部分
"""
cv2.imshow(filterColor("test",
                       np.array([3, 220, 220]), np.array([50, 255, 255])))
cv2.waitKey(0)
cv2.destroyAllWindows()
