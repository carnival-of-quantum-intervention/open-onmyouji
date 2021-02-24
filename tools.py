import cv2
import mouse
import picture
import threading
import tkinter
import time
import window


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

    def execute(self, task):
        global cacheMap
        HWND = self.__hwnd
        left, top, right, bottom = window.getRect(HWND)
        windowWidth, windowHeight = right - left, top - bottom
        # 读取图片
        captured = window.captureWindowAs(HWND, "cache/cache.png")

        r = int(task["ratio"] * windowWidth)
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
                X = x + left
                Y = y + top
                print("Willing to click ", X, Y)
                mouse.click(X, Y)
                return True
            return "otherwise" in task and self.execute(task["otherwise"])


global cacheMap
cacheMap = {}
