import cv2
from numpy.lib.npyio import NpzFile
import mouse
import picture
import threading
import time
import tkinter
import window
import cache


def readImage(filename):
    return cache.readBy(filename, cv2.imread)


def findCirclePictureIn(captured, task,  r):
    Circles = picture.findCircles(captured, r)  # 去掉circles数组一层外括号
    if len(Circles) != 0:
        raw_image = readImage(task["image"])
        expect = picture.processImage(raw_image)
        x, y = picture.findSimilarestPictureWith(
            Circles, captured, expect, compareFunc=picture.compareCircle)
        if x and y:
            return (x, y)
    return None


def clickAt(captured, task, points, hwnd):
    point = None
    if points == None or len(points) == 0:
        if "position" in task and len(task["position"]) >= 2:
            a = task["position"][0]
            b = task["position"][1]
            point = a
        else:
            point = None
    else:
        if len(points[0] >= 2):
            point = points[0][0:2]
    if point != None:
        mouse.click(*window.getAbsolutePos(hwnd, point))
    return point


class thread(threading.Thread):
    def __init__(self, HWND, configs, index):
        self.__index = index
        self.__configs = configs

        self.__on = True
        self.__hwnd = HWND

        self.stateStr = tkinter.StringVar()
        self.stateStr.set("Waiting")
        self.resultStr = tkinter.StringVar()
        self.resultStr.set("Uninitialized")
        self.posStr = tkinter.StringVar()
        self.posStr.set("Uninitialized")

        threading.Thread.__init__(self)

    def set(self, index):
        self.__index = index

    def __del__(self):
        self.__on = False

    def run(self):
        config = self.__configs["config"]
        while self.__on:
            if self.__index >= 0:
                self.stateStr.set("Working")
                global resultStr
                self.resultStr.set("Found"if self.execute(
                    config[self.__index]["task"], None)else "Not found")

            time.sleep(1)

    def execute(self, task, arg):
        global cacheMap
        HWND = self.__hwnd
        left, top, right, bottom = window.getRect(HWND)
        windowWidth, windowHeight = right - left, top - bottom
        # 读取图片
        captured = window.captureWindowAs(HWND, "cache/cache.png")

        res = None
        if "type"not in task:
            print("Please specify the task type.")
            return
        if task["type"] == "locate":
            if "shape" in task:
                if task["shape"] == "circle":
                    res = findCirclePictureIn(
                        captured, task, int(task["ratio"] * windowWidth))
                else:
                    print("Unrecognized shape", task["shape"])
            elif "color" in task:
                if "model" in task["color"]:
                    if task["color"]["model"] == "hsv":
                        if "image" in task["color"]:
                            res = picture.findColor(
                                captured, readImage(task["color"]["image"]))
                    else:
                        print("Unrecognized color model",
                              task["color"]["model"])
        elif task["type"] == "click":
            res = clickAt(captured, task, arg, HWND)
        elif task["type"] == "count":
            if arg != None:
                res = len(arg)
            else:
                res = 0
        elif task["type"] == "take":
            if "count" not in task:
                res = None
            else:
                res = arg[0:task["count"]]
        elif task["type"] == "compare":
            if arg < task["value"]:
                return ()
            else:
                return None
        else:
            print("Unrecognized type", task["type"])
            return None

        if "then" in task:
            return self.execute(task["then"], res)
        return "otherwise" in task and self.execute(task["otherwise"], arg)


global cacheMap
cacheMap = {}
