#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_words, abel_checking
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
    w.set_foreground()
    rect     = win32gui.GetWindowRect(w._handle)
    x_offset = rect[0]
    y_offset = rect[1]
    if sys.argv[1] == '-pos':
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        if w._find:
            rect = win32gui.GetWindowRect(w._handle)
            x_offset = rect[0]
            y_offset = rect[1]
            cursor = win32gui.GetCursorPos()
            print cursor[0] - x_offset, cursor[1] - y_offset
    elif sys.argv[1] == '-bxxm':
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        w.set_foreground()
        rect                 = win32gui.GetWindowRect(w._handle)
        x_offset             = rect[0]
        y_offset             = rect[1]
        # x_head_begin = x_offset + 376
        # y_head_begin = y_offset + 232
        # x_head_end = x_head_begin + 260
        # y_head_end = y_head_begin + 54
        im_head = ImageGrab.grab(
            bbox=(
                x_offset + abel_window.bxxm_pos[0],
                y_offset + abel_window.bxxm_pos[1],
                x_offset + abel_window.bxxm_pos[2],
                y_offset + abel_window.bxxm_pos[3]
            )
        )
        im_head.save(sys.argv[1]+'.png')
        # im = cv2.imread(sys.argv[1]+'.png', 0)
        # im2 = cv2.resize(im, (0,0), fx=3.0, fy=3.0)
        # cv2.imwrite(sys.argv[1]+'.tif', im2)
    elif sys.argv[1] == '-cord':
        pyautogui.keyDown('alt')
        pyautogui.press('1')
        pyautogui.keyUp('alt')
        time.sleep(0.5)
        pyautogui.click(x_offset+275, y_offset+300)
        pyautogui.keyDown('alt')
        pyautogui.press('1')
        pyautogui.keyUp('alt')
        time.sleep(10)
        pyautogui.click(x_offset+487, y_offset+89)
        time.sleep(0.5)
        pyautogui.click(x_offset+233, y_offset+377)
        print abel_words.get_bxxm_task_description(x_offset, y_offset, abel_window.coordinate_pos)
    elif sys.argv[1] == '-blue':
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        w.set_foreground()
        rect                 = win32gui.GetWindowRect(w._handle)
        x_offset             = rect[0]
        y_offset             = rect[1]
        print abel_checking.checkInRange(box=[x_offset+750,y_offset+89,x_offset+752,y_offset+90], lower=0, upper=100)
        # mask = cv2.inRange(im, numpy.array(lower, dtype='uint8'), numpy.array(upper, dtype='uint8'))
        # return cv2.countNonZero(mask) == w*h

