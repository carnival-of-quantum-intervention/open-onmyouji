# 加载环境包
import json
import keyboard
import mouse
import tkinter
import tools
import window


configs = json.load(open("config.json", 'r', encoding="utf-8"))
configList = [item["name"] for item in configs["config"]]

HWND = window.getHandle(configs["title"])
if HWND == 0:
    print("Can't find such window.")
    exit(1)


def packPos(a, b):
    return str([round(i, 6) for i in a]) + "->"+str([round(i, 6) for i in b])


global mouseFrom, mouseTo
mouseFrom = (0, 0)
mouseTo = (0, 0)


ROOT = tkinter.Tk()

global mainThread
mainThread = tools.thread(HWND, configs, -1)
mainThread.start()

state = tkinter.Label(ROOT, textvariable=mainThread.stateStr)
state.pack()
result = tkinter.Label(ROOT, textvariable=mainThread.resultStr)
result.pack()
pos = tkinter.Label(ROOT, textvariable=mainThread.posStr)
pos.pack()


def watchKeyBoard(Event):
    global mouseFrom, mouseTo
    if Event.event_type == 'up':
        if Event.name == 'ctrl':
            mouseTo = window.getRelativePos(HWND, mouse.getPos())
            mainThread.posStr.set(packPos(mouseFrom, mouseTo))
    if Event.event_type == 'down':
        if Event.name == 'space':
            mainThread.set(-1)
            mainThread.stateStr.set("Paused")
        elif Event.name == 'ctrl':
            mouseFrom = window.getRelativePos(HWND, mouse.getPos())
            mainThread.posStr.set(packPos(mouseFrom, mouseTo))


keyboard.hook(watchKeyBoard)


def CallOn(event):
    print(event)
    mainThread.set(event.widget.curselection()[0])


# 双击命令
lb = tkinter.Listbox(ROOT)
lb.bind('<Double-Button-1>', CallOn)
lb.insert(tkinter.END, *configList)
lb.pack()

ROOT.mainloop()
mainThread.__del__()
