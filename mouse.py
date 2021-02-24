

def click(x, y):
    import pyautogui
    # pyautogui.moveTo(x, y)
    pyautogui.click(x, y)


def getPos():
    import pyautogui
    pos = pyautogui.position()
    return pos
