

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


def click(x, y):
    import pyautogui
    # pyautogui.moveTo(x, y)
    pyautogui.click(x, y)


def getRect(hwnd):
    import win32gui
    # 获取窗口左上角和右下角坐标
    wLeft, wTop, wRight, wBottom = win32gui.GetWindowRect(hwnd)
    cLeft, cTop, cRight, cBottom = win32gui.GetClientRect(hwnd)
    return wLeft+cLeft, wTop+cTop, wLeft+cRight, wTop+cBottom


def captureWindowAs(hwnd, filename):
    """ hwnd为窗口的编号，0号表示当前活跃窗口"""
    import win32gui
    import win32ui
    import win32con
    import win32api
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
