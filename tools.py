import cv2
import picture
import threading
import time
import tkinter
import window


def findCirclePictureIn(captured, task,  r):
    Circles = picture.findCircles(captured, r)  # 去掉circles数组一层外括号
    if len(Circles) != 0:
        if task["image"] in cacheMap:
            raw_image = cacheMap[task["image"]]
        else:
            raw_image = cv2.imread(task["image"])
            cacheMap[task["image"]] = raw_image

        expect = picture.processImage(raw_image)
        x, y = picture.findSimilarestPictureWith(
            Circles, captured, expect, compareFunc=picture.compareCircle)
        if x and y:
            return (x, y)
    return None


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
                    config[self.__index]["task"])else "Not found")

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
            res = findCirclePictureIn(
                captured, task, int(task["ratio"] * windowWidth))

        if "then" in task:
            return self.execute(task["then"], res)
        return "otherwise" in task and self.execute(task["otherwise"])


global cacheMap
cacheMap = {}
