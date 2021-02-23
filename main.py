# 加载环境包
import json
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
    # 读取图片
    captured = captureWindowAs(HWND, "cache/cache.png")
    r = int(task["ratio"] * WindowWidth)
    Circles = findCircles(captured, r)  # 去掉circles数组一层外括号
    if len(Circles) != 0:
        if task["image"] in cacheMap:
            raw_image = cacheMap[task["image"]]
        else:
            raw_image = cv2.imread(task["image"])
            cacheMap[task["image"]] = raw_image

        expect = processImage(raw_image)
        x, y = findSimilarestPictureWith(Circles, captured, expect)
        if x and y:
            X = x + left
            Y = y + top
            print("Willing to click ", X, Y)
            click(X, Y)
            return True
        return "fallback" in task and work(task["fallback"])


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

global stateStr, resultStr
stateStr = tkinter.StringVar()
stateStr.set("Waiting")
state = tkinter.Label(ROOT, textvariable=stateStr)
state.pack()
resultStr = tkinter.StringVar()
resultStr.set("Not found")
result = tkinter.Label(ROOT, textvariable=resultStr)
result.pack()


class thread(threading.Thread):
    def __init__(self, index):
        self.__index = index
        threading.Thread.__init__(self)

    def set(self, index):
        self.__index = index

    def run(self):
        global stateStr
        config = configs["config"]
        while on:
            if self.__index >= 0:
                stateStr.set("Working")
                global resultStr
                resultStr = "Found"if work(
                    config[self.__index]["task"])else "Not found"

            time.sleep(1)
        stateStr.set("Dead")


global mainThread
mainThread = thread(-1)
mainThread.start()
lb = tkinter. Listbox(ROOT)


def CallOn(event):
    global mainThread
    mainThread.set(lb.curselection()[0])


# 双击命令
lb.bind('<Double-Button-1>', CallOn)
lb.insert(tkinter.END, *configList)
lb.pack()
ROOT.mainloop()
