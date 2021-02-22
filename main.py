# 加载环境包
from window import *
from picture import *
import keyboard
import time


def getRadius(screenWidth, windowWidth):
    # 结果
    Radius = 70 * windowWidth / screenWidth
    return Radius


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
    captureWindowAs(hwnd, "cache/cache.png")
    img = cv2.imread('cache/cache.png')  # 读取图片
    r = int(getRadius(ScreenWidth, WindowWidth))
    P = findCircles(img, r)[0]  # 去掉circles数组一层外括号

    print("圆的个数是：", len(P))
    for i in P:
        print("圆心坐标为：", (int(i[0]), int(i[1])), "圆的半径是：", int(i[2]))
    test = processImage(cv2.imread("pic.png"))

    x, y = findSimilarestPictureWith(P, test)
    X = x + LEFT
    Y = y + TOP
    if(len(P) > 0):
        print("Willing to click ", X, Y)
        click(X, Y)

    time.sleep(1)
