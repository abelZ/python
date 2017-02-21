#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_words
import pyscreenshot as ImageGrab
import win32gui
import pyautogui
import sys, time
from multiprocessing import freeze_support
import cv2

if __name__ == '__main__':
    freeze_support()
    w = abel_window.WindowMgr()
    w.find_window_wildcard(".*Revision.*ID.*")
    if w._find == False:
        return
    w.set_foreground()
    x,y = w.offset()
    if sys.argv[1] == '-pos':
        cursor = win32gui.GetCursorPos()
        print cursor[0] - x, cursor[1] - y
    elif sys.argv[1] == '-bxxm':
        im_head = ImageGrab.grab(
            bbox=(
                x + abel_window.bxxm_pos[0],
                y + abel_window.bxxm_pos[1],
                x + abel_window.bxxm_pos[2],
                y + abel_window.bxxm_pos[3]
            )
        )
        im_head.save(sys.argv[1]+'.png')
    elif sys.argv[1] == '-cord':
        pyautogui.keyDown('alt')
        pyautogui.press('1')
        pyautogui.keyUp('alt')
        time.sleep(0.5)
        pyautogui.click(x+275, y+300)
        pyautogui.keyDown('alt')
        pyautogui.press('1')
        pyautogui.keyUp('alt')
        time.sleep(10)
        pyautogui.click(x+487, y+89)
        time.sleep(0.5)
        pyautogui.click(x+233, y+377)
        print abel_words.get_bxxm_task_description(x, y, abel_window.coordinate_pos)
    elif sys.argv[1] == '-blue':
        return w.checkBlueEnough()

