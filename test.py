import cv2
import numpy as np
from window import *
from picture import *
from find_pic import *

HWND = getHandle("阴阳师-网易游戏")
# 读取图片
captured = captureWindowAs(HWND, "cache/cache.png")

src = captured
"""
提取图中的黄色部分
"""
filtered = filterColor(src,
                       np.array([3, 220, 220]), np.array([50, 255, 255]))
cv2.imshow("mask", filtered)
print(find_full(filtered, cv2.cvtColor(
    cv2.imread("picture/full.png"), cv2.COLOR_BGR2GRAY)))
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imshow()
# cv2.waitKey(0)
# cv2.destroyAllWindows()
