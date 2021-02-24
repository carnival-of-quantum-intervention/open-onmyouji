# 加载环境包
import json
import mouse
from window import *
from picture import *
import threading
import keyboard
import time
import tkinter


global cacheMap
cacheMap = {}


def work(task):
    global cacheMap, windowWidth
    # 读取图片
    captured = captureWindowAs(HWND, "cache/cache.png")
    r = int(task["ratio"] * windowWidth)
    Circles = findCircles(captured, r)  # 去掉circles数组一层外括号
    if len(Circles) != 0:
        if task["image"] in cacheMap:
            raw_image = cacheMap[task["image"]]
        else:
            raw_image = cv2.imread(task["image"])
            cacheMap[task["image"]] = raw_image

        expect = processImage(raw_image)
        x, y = findSimilarestPictureWith(
            Circles, captured, expect, compareFunc=compareCircle)
        if x and y:
            X = x + left
            Y = y + top
            print("Willing to click ", X, Y)
            mouse.click(X, Y)
            return True
        return "fallback" in task and work(task["fallback"])


configs = json.load(open("config.json", 'r', encoding="utf-8"))
configList = [item["name"] for item in configs["config"]]

HWND = getHandle(configs["title"])
if HWND == 0:
    print("Can't find such window.")
    exit(1)


global left, top, right, bottom, windowWidth, windowHeight
left, top, right, bottom = getRect(HWND)
windowWidth = right - left
windowHeight = bottom - top

global on
on = True


def packPos(a, b):
    return str([round(i, 6) for i in a]) + "->"+str([round(i, 6) for i in b])


global mouseFrom, mouseTo
mouseFrom = (0, 0)
mouseTo = (0, 0)


def watchKeyBoard(Event):
    global posStr, mouseFrom, mouseTo
    if Event.event_type == 'up':
        if Event.name == 'ctrl':
            mouseTo = getRelativePos(HWND, mouse.getPos())
            posStr.set(packPos(mouseFrom, mouseTo))
    if Event.event_type == 'down':
        if Event.name == 'f5':
            global left, top, right, bottom, windowWidth, windowHeight
            left, top, right, bottom = getRect(HWND)
            windowWidth = right - left
            windowHeight = bottom - top
        elif Event.name == 'space':
            global mainThread, stateStr
            mainThread.set(-1)
            stateStr.set("Paused")
        elif Event.name == 'ctrl':
            mouseFrom = getRelativePos(HWND, mouse.getPos())
            posStr.set(packPos(mouseFrom, mouseTo))


keyboard.hook(watchKeyBoard)

ROOT = tkinter.Tk()

global stateStr, resultStr, posStr
stateStr = tkinter.StringVar()
stateStr.set("Waiting")
state = tkinter.Label(ROOT, textvariable=stateStr)
state.pack()
resultStr = tkinter.StringVar()
resultStr.set("Uninitialized")
result = tkinter.Label(ROOT, textvariable=resultStr)
result.pack()
posStr = tkinter.StringVar()
posStr.set("Uninitialized")
pos = tkinter.Label(ROOT, textvariable=posStr)
pos.pack()


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
                resultStr.set("Found"if work(
                    config[self.__index]["task"])else "Not found")

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
on = False
