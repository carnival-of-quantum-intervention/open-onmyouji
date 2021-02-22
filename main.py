# 加载环境包
import json
from window import *
from picture import *
import keyboard
import time

configs = json.load(open("config.json", 'r', encoding="utf-8"))
print(configs)
index = int(input("Input the index of the configure you'd like to use."))
HWND = getHandle(configs["title"])
if HWND == 0:
    print("Can't find onmyouji.")
    exit(1)

config = configs["config"][index]

ScreenWidth, ScreenHeight = getScreenSize()

global left, top, right, bottom
left, top, right, bottom = getRect(HWND)
WindowWidth = right - left

global on
on = True


def watchEsc(Event):
    if Event.event_type == 'down':
        if Event.name == 'esc':
            global on
            on = False
        if Event.name == 'f5':
            global left, top, right, bottom, WindowWidth
            left, top, right, bottom = getRect(HWND)
            WindowWidth = right - left


keyboard.hook(watchEsc)
while(on):

    captureWindowAs(HWND, "cache/cache.png")
    img = cv2.imread('cache/cache.png')  # 读取图片
    r = int(config["ratio"] * WindowWidth)
    Circles = findCircles(img, r)[0]  # 去掉circles数组一层外括号

    raw_image = cv2.imread(config["image"])
    image = processImage(raw_image)

    x, y = findSimilarestPictureWith(Circles, img, image)
    X = x + left
    Y = y + top
    if x and y:
        print("Willing to click ", X, Y)
        click(X, Y)

    time.sleep(1)
