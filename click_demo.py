# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 14:02:23 2021

@author: 羽
"""

import pyautogui
import sys

def game_click(pic_x,pic_y):
    pyautogui.click(pic_x,pic_y)

if len(sys.argv) >= 3:
	pix_x = int(sys.argv[1])
	pix_y = int(sys.argv[2])
else:
	pix_x = int(input("x坐标:"))
	pix_y = int(input("y坐标:"))

game_click(pix_x, pix_y)