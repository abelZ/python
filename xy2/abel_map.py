#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import time, random

class point:
    def __init__(self, x, y, p, e):
        self.x = x
        self.y = y
        self.pos = p
        self.event = e

    def click(self):
        if self.event == 'click_map':
            pyautogui.keyDown('alt')
            pyautogui.press('1')
            pyautogui.keyUp('alt')
            time.sleep(0.5)
        pyautogui.click()
        if self.event == 'click_map':
            time.sleep(0.5)
            pyautogui.keyDown('alt')
            pyautogui.press('1')
            pyautogui.keyUp('alt')

    def position():
        return self.pos

    def coordinate(self):
        return [self.x, self.y]

bx_hygb = [
    point(x, y, 'baoxiang', 'click_map'),
    point(x, y, 'baoxiang', 'click'),
    point(x, y, 'baoxiang', 'click'),
]

bx_hyd = [
    point(x, y, 'baoxiang', 'click_map'),
    point(x, y, 'baoxiang', 'click'),
    point(x, y, 'baoxiang', 'click'),
    point(x, y, 'huoyungebi', 'click_map'),
    point(x, y, 'huoyungebi', 'click')
]
