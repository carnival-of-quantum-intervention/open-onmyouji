# 加载环境包
import json
from os import stat
from typing import Mapping
from window import *
from picture import *
import threading
import keyboard
import time
import tkinter


global cacheMap
cacheMap = {}


def work(task):
    global cacheMap, WindowWidth

    captureWindowAs(HWND, "cache/cache.png")
    img = cv2.imread('cache/cache.png')  # 读取图片
    r = int(task["ratio"] * WindowWidth)
    Circles = findCircles(img, r)[0]  # 去掉circles数组一层外括号

    if task["image"] in cacheMap:
        raw_image = cacheMap[task["image"]]
    else:
        raw_image = cv2.imread(task["image"])
        cacheMap[task["image"]] = raw_image

    image = processImage(raw_image)

    x, y = findSimilarestPictureWith(Circles, img, image)
    if x and y:
        X = x + left
        Y = y + top
        print("Willing to click ", X, Y)
        click(X, Y)
    elif "fallback" in task:
        work(task["fallback"])


configs = json.load(open("config.json", 'r', encoding="utf-8"))
configList = [item["name"] for item in configs["config"]]

HWND = getHandle(configs["title"])
if HWND == 0:
    print("Can't find such window.")
    exit(1)


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
            global left, top, right, bottom, windowWidth
            left, top, right, bottom = getRect(HWND)
            windowWidth = right - left
        if Event.name == 'space':
            global mainThread, stateStr
            mainThread.set(-1)
            stateStr.set("Paused")


keyboard.hook(watchEsc)

ROOT = tkinter.Tk()

global stateStr
stateStr = tkinter.StringVar()
stateStr.set("Waiting")
state = tkinter.Label(ROOT, textvariable=stateStr)
state.pack()


class thread(threading.Thread):
    def __init__(self, index):
        self.__index = index
        threading.Thread.__init__(self)

    def set(self, index):
        self.__index = index

    def run(self):
        global stateStr
        while on:
            if self.__index >= 0:
                stateStr.set("Working")
                work(configs["config"][self.__index]["task"])
            time.sleep(1)
        stateStr.set("Dead")


global mainThread
mainThread = thread(-1)
mainThread.start()
lb = tkinter. Listbox(ROOT)


def CallOn(event):
    global mainThread
    print(mainThread)
    mainThread.set(lb.curselection()[0])


# 双击命令
lb.bind('<Double-Button-1>', CallOn)
lb.insert(tkinter.END, *configList)
lb.pack()
ROOT.mainloop()
