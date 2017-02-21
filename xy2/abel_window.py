#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32gui, re
import time, random
import pyautogui
import cv2, numpy
import pyscreenshot as ImageGrab

s_not_moved      = 'not moved'
s_not_in_team    = 'not in team'
s_in_team        = 'in team'

#[x1, y1, x2, y2]
head_pos         = [676, 56, 720, 100]
animal_pos       = [568, 56, 610, 98]
team_pos         = [250, 56, 550, 100]
animal_fight_pos = [0, 56, 84, 98]
red_pos          = [729, 73, 796, 82]
blue_pos         = [730, 88, 797, 94]
drug_pos         = [298, 378, 328, 408]
box_pos          = [343, 367, 354, 390]
bidou_pos        = [507, 408, 593, 423]
bxxm_pos         = [376, 232, 636, 286]
coordinate_pos   = [20,63,143,84]
blue_enough_pos  = [750, 89, 752, 90]#[730,89,800,90]

wild_pos         = [[283,231], [468,283], [378,451], [270,388], [530,367]]
nao_pos          = [[0,0], [0,0], [0,0], [0,0], [0,0]]

blue_range       = [0, 100]

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None
        self._find = False
        self.x = 0
        self.y = 0
        self.template_cache = False
        self.team_template = None
        self.anim_template = None

    def find_window(self, class_name, window_name = None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd
            self._find = True

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
        rect   = win32gui.GetWindowRect(self._handle)
        self.x = rect[0]
        self.y = rect[1]

    def offset(self):
        return self.x, self.y

    def clickAuto(self, count):
        for i in range(count):
            pyautogui.keyDown('alt')
            pyautogui.press('8')
            pyautogui.keyUp('alt')
            if count > 1:
                pyautogui.keyDown('ctrl')
                pyautogui.press('tab')
                pyautogui.keyUp('ctrl')

    def clickDrug(self):
        pyautogui.keyDown('alt')
        pyautogui.press('e')
        pyautogui.keyUp('alt')
        time.sleep(0.2)
        pyautogui.rightClick(
            random.randint(
                self.x+drug_pos[0],
                self.x+drug_pos[2]
            ),
            random.randint(
                self.y+drug_pos[1],
                self.y+drug_pos[3]
            )
        )
        time.sleep(0.2)
        pyautogui.keyDown('alt')
        pyautogui.press('e')
        pyautogui.keyUp('alt')

    def grabImage(self, box):
        absBox = [self.x+box[0], self.y+box[1], self.x+box[2], self.y+box[3]]
        im = ImageGrab.grab(bbox = absBox)
        (w, h) = im.size
        tmp = list(im.getdata())
        np_array = []
        index = 0
        for i in range(h):
            np_array.append(tmp[index:index+w])
            index += w
        srcRGB = numpy.array(np_array, dtype=numpy.uint8)
        return cv2.cvtColor(srcRGB, cv2.COLOR_RGB2BGR),w,h

    def checkBlueEnough(self):
        im,w,h = self.grabImage(blue_enough_pos)
        b,g,r = cv2.split(im)
        mask = cv2.inRange(r,
                           numpy.array([blue_range[0]], dtype='uint8'),
                           numpy.array([blue_range[1]], dtype='uint8'))
        return cv2.countNonZero(mask) == w*h

    def check_out_fight_in_team(self):
        if self.template_cache == False:
            self.template_cache = True
            self.team_template,w,h = self.grabImage(head_pos)
            self.anim_template,w,h = self.grabImage(animal_pos)

        cv_team,w,h = self.grabImage(team_pos)
        res = cv2.matchTemplate(cv_team, self.team_template, eval('cv2.TM_CCOEFF'))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val >= 4500000.0

    def check_if_in_fight(self):
        cv_fight,w,h = self.grabImage(animal_fight_pos)
        res = cv2.matchTemplate(cv_fight, self.anim_template, eval('cv2.TM_CCOEFF'))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val >= 4500000.0

    def full_blue_red(self, count):
        for i in range(count):
            pyautogui.rightClick(
                random.randint(
                    self.x+red_pos[0],
                    self.x+red_pos[2]
                ),
                random.randint(
                    self.y+red_pos[1],
                    self.y+red_pos[3]
                )
            )
            time.sleep(0.2)
            pyautogui.rightClick(
                random.randint(
                    self.x+blue_pos[0],
                    self.x+blue_pos[2]
                ),
                random.randint(
                    self.y+blue_pos[1],
                    self.y+blue_pos[3]
                )
            )
            time.sleep(0.2)
            if count > 1:
                pyautogui.keyDown('ctrl')
                pyautogui.press('tab')
                pyautogui.keyUp('ctrl')

    def attack(self, pos):
        pyautogui.keyDown('alt')
        pyautogui.keyDown('a')
        pyautogui.click(self.x+pos[0], self.y+pos[1])
        pyautogui.keyUp('a')
        pyautogui.keyUp('alt')

