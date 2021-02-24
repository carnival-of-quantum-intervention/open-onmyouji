

def getScreenSize():
    import win32api
    import win32con
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得X轴屏幕分辨率
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得Y轴屏幕分辨率
    return width, height


def getHandle(titlename):
    import win32gui
    # 获取句柄
    return win32gui.FindWindow(0, titlename)
# 确定圆大小


def getRect(hwnd):
    import win32gui
    import win32api
    import win32con
    # 获取窗口左上角和右下角坐标
    wLeft, wTop, wRight, wBottom = win32gui.GetWindowRect(hwnd)
    #cLeft, cTop, cRight, cBottom = win32gui.GetClientRect(hwnd)
    hTitle = win32api.GetSystemMetrics(win32con.SM_CYSIZE)
    return wLeft, hTitle + wTop, wRight,  wBottom


def getSize(hwnd):
    left, top, right, bottom = getRect(hwnd)
    return right - left, top - bottom


def getRelativePos(hwnd, pos):
    left, top, right, bottom = getRect(hwnd)
    width = right-left
    height = bottom-top
    return (pos.x - left) / width, (pos.y - top) / height


def getAbsolutePos(hwnd, pos):
    left, top, right, bottom = getRect(hwnd)
    width = right-left
    height = bottom-top
    return pos[0] * width + left, pos[1] * height + top


def captureWindowAs(hwnd, filename):
    from PIL import ImageGrab
    import numpy as np
    import cv2

    img = ImageGrab.grab()

    # PIL image to OpenCV image
    im = np.array(img)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    left, top, right, bottom = getRect(hwnd)
    im = im[top:bottom, left:right]
    cv2.imwrite(filename, im)
    return im
