# 加载环境包
import json
from window import *
from picture import *
import keyboard
import time


configs = json.loads("config.json")
print(configs)
index = int(input("Input the index of the configure you'd like to use."))
HWND = getHandle(configs["title"])
if HWND == 0:
    print("Can't find onmyouji.")
    exit(1)

config = configs["config"][index]

ScreenWidth, ScreenHeight = getScreenSize()
LEFT, TOP, RIGHT, BOTTOM = getRect(HWND)
WindowWidth = RIGHT - LEFT

global on
on = True


def watchEsc(Event):
    if Event.event_type == 'down' and Event.name == 'esc':
        global on
        on = False


keyboard.hook(watchEsc)
while(on):
    import shutil
    shutil.rmtree("./cache")

    captureWindowAs(HWND, "cache/cache.png")
    img = cv2.imread('cache/cache.png')  # 读取图片
    r = int(config["ratio"] * WindowWidth)
    P = findCircles(img, r)[0]  # 去掉circles数组一层外括号

    test = processImage(cv2.imread("pic.png"))

    x, y = findSimilarestPictureWith(P, img, test)
    X = x + LEFT
    Y = y + TOP
    if(len(P) > 0):
        print("Willing to click ", X, Y)
        click(X, Y)

    time.sleep(1)
