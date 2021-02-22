# 加载环境包
import keyboard
import cv2
import time
import numpy as np


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
    # 获取窗口左上角和右下角坐标
    return win32gui.GetWindowRect(hwnd)


def getRadius(screenWidth, windowWidth):
    # 结果
    Radius = 70 * windowWidth / screenWidth
    return Radius


def findCircles(img, r):
    # 图片简单处理
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化
    GrayImage = cv2.equalizeHist(GrayImage)
    GrayImage = cv2.medianBlur(GrayImage, 5)  # 中值模糊

    # 阈值处理，输入图片默认为单通道灰度图片
    ret, th1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)  # 固定阈值二值化
    # threshold为固定阈值二值化
    # 第二参数为阈值
    # 第三参数为当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值（一般情况下，都是256色，所以默认最大为255）
    # thresh_binary是基于直方图的二值化操作类型，配合threshold一起使用。此外还有cv2.THRESH_BINARY； cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC； cv2.THRESH_TOZERO；	cv2.THRESH_TOZERO_INV
    th2 = cv2.adaptiveThreshold(
        GrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C,  cv2.THRESH_BINARY, 3, 5)
    # adaptiveThreshold自适应阈值二值化，自适应阈值二值化函数根据图片一小块区域的值来计算对应区域的阈值，从而得到也许更为合适的图片。
    # 第二参数为当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值（一般情况下，都是256色，所以默认最大为255）
    # 第三参数为阈值计算方法，类型有cv2.ADAPTIVE_THRESH_MEAN_C，cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    # 第四参数是基于直方图的二值化操作类型，配合threshold一起使用。此外还有cv2.THRESH_BINARY； cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC； cv2.THRESH_TOZERO；cv2.THRESH_TOZERO_INV
    # 第五参数是图片中分块的大小
    # 第六参数是阈值计算方法中的常数项
    th3 = cv2.adaptiveThreshold(
        GrayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 5)
    # 同上
    kernel = np.ones((5, 5), np.uint8)  # 创建全一矩阵，数值类型设置为uint8
    erosion = cv2.erode(th3, kernel, iterations=1)  # 腐蚀处理
    dilation = cv2.dilate(erosion, kernel, iterations=1)  # 膨胀处理

    imgray = cv2.Canny(dilation, 30, 100)  # Canny边缘检测算子

    # cv2.imshow('Step 1',th3)#第一参数为窗口名称
    # cv2.imshow('Step 2',erosion)#第一参数为窗口名称
    # cv2.imshow('Step 3',imgray)#第一参数为窗口名称

    circles = cv2.HoughCircles(imgray, method=cv2.HOUGH_GRADIENT, dp=1,
                               minDist=80, param1=100, param2=20, minRadius=r-5, maxRadius=r+5)  # 霍夫圆变换
    if circles is None:
        print("No circles found.")
        return [[]]
    # 第3参数默认为1
    # 第4参数表示圆心与圆心之间的距离（太大的话，会很多圆被认为是一个圆）
    # 第5参数默认为100
    # 第6参数根据圆大小设置(圆越小设置越小，检测的圆越多，但检测大圆会有噪点)
    # 第7圆最小半径
    # 第8圆最大半径

    circles = np.uint16(np.around(circles))
    # np.uint16数组转换为16位，0-65535
    # np.around返回四舍五入后的值
    return circles


def compare(img1, img2):
    res = 0
    all_sum = 0
    width = img1.shape[0]
    height = img1.shape[1]
    rx = width/2
    ry = height/2
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            all_sum += int(img1[i, j])+int(img2[i, j])
            #print(pow(rx-i,2),"+",pow(ry-j,2) ,"?", pow(width/2,2))
            if pow(rx-i, 2)+pow(ry-j, 2) > pow(width/2, 2):
                # print(i,",",j)
                continue
            res += abs(int(img1[i, j])-int(img2[i, j]))
    return res/(all_sum/2)


def findSimilarestPictureWith(Circles, ExpectImg):
    count = 0

    potentialPoints = []

    for i in Circles:
        if i[1]-i[2] < 0 or i[0]-i[2] < 0 or i[1]+i[2] > (img.shape)[1] or i[0]+i[2] > (img.shape)[0]:
            continue
        cropImg = img[i[1]-i[2]:i[1]+i[2], i[0]-i[2]:i[0]+i[2]]
        cv2.imwrite("cache/"+str(count)+".jpg", cropImg)
        cropImg = cv2.resize(cropImg, (100, 100),
                             interpolation=cv2.INTER_CUBIC)
        cropImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
        ret = compare(cropImg, test)
        potentialPoints.append([i[0], i[1], ret])
        count += 1

    # potentialPoints.sort(key=operator.itemgetter(2), reverse=True)
    potentialPoints.sort(key=lambda _tuple: _tuple[2])
    print(potentialPoints)
    ChosenPoint = potentialPoints[0]
    return ChosenPoint[0], ChosenPoint[1]


def captureWindowsAs(hwnd, filename):
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


def ProcessImage(image):
    image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def click(x, y):
    import pyautogui
    pyautogui.moveTo(x, y)
    # pyautogui.click(x, y)


hwnd = getHandle("阴阳师-网易游戏")
if hwnd == 0:
    print("Can't find onmyouji.")
    exit(-1)

ScreenWidth, ScreenHeight = getScreenSize()
LEFT, TOP, RIGHT, BOTTOM = getRect(hwnd)
WindowWidth = RIGHT - LEFT

global on
on = True


def watchEsc(Event):
    if Event.event_type == 'down' and Event.name == 'esc':
        global on
        on = False


keyboard.hook(watchEsc)
while(on):
    captureWindowsAs(hwnd, "cache/cache.png")
    img = cv2.imread('cache/cache.png')  # 读取图片
    r = int(getRadius(ScreenWidth, WindowWidth))
    P = findCircles(img, r)[0]  # 去掉circles数组一层外括号

    print("圆的个数是：", len(P))
    for i in P:
        print("圆心坐标为：", (int(i[0]), int(i[1])), "圆的半径是：", int(i[2]))
    test = ProcessImage(cv2.imread("pic.png"))

    x, y = findSimilarestPictureWith(P, test)
    X = x + LEFT
    Y = y + TOP
    if(len(P) > 0):
        print("Willing to click ", X, Y)
        click(X, Y)

    time.sleep(1)
