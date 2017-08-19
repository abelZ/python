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
drug_blue_pos    = [298, 378, 328, 408]
drug_red_pos     = [247, 379, 273, 408]
box_pos          = [343, 367, 354, 390]
bidou_pos        = [507, 408, 593, 423]
bxxm_task_pos    = [376, 232, 636, 286] #bxxm
coordinate_pos   = [20,63,143,84]
blue_enough_pos  = [755, 89, 757, 90]#[730,89,800,90]
red_enough_pos   = [770, 74, 772, 75]#[730,74,800,75]

wild_pos         = [[283,231], [468,283], [378,451], [270,388], [530,367]]
nao_pos          = [[216,274], [236,210], [230,163]]#hua 282,42
# nao_pos          = [[222,386], [222,356], [227,332]]#hua ben 365,71
# nao_pos          = [[263,80], [238,118], [294,147]]#tian 152,293

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
            pyautogui.hotkey('alt', '8')
            if count > 1:
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'tab')

    def clickDrug(self, pos):
        pyautogui.hotkey('alt', 'e')
        time.sleep(0.25)
        pyautogui.click(self.x+348,self.y+385)
        time.sleep(0.25)
        pyautogui.rightClick(
            random.randint(
                self.x+pos[0],
                self.x+pos[2]
            ),
            random.randint(
                self.y+pos[1],
                self.y+pos[3]
            )
        )
        time.sleep(0.25)
        pyautogui.hotkey('alt', 'e')

    def drinkBlue(self):
        time.sleep(0.1)
        self.clickDrug(drug_blue_pos)

    def drinkRed(self):
        time.sleep(0.1)
        self.clickDrug(drug_red_pos)

    def drinkDrug(self, count):
        for i in range(count):
            if self.checkBlueEnough() == False:
                self.drinkBlue()
            if self.checkRedEnough() == False:
                self.drinkRed()
            if count > 1:
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'tab')

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

    def checkRedEnough(self):
        im,w,h = self.grabImage(red_enough_pos)
        b,g,r = cv2.split(im)
        mask = cv2.inRange(b,
                           numpy.array([blue_range[0]], dtype='uint8'),
                           numpy.array([blue_range[1]], dtype='uint8'))
        return cv2.countNonZero(mask) == w*h

    def check_cache(self):
        if self.template_cache == False:
            self.template_cache = True
            self.team_template,w,h = self.grabImage(head_pos)
            self.anim_template,w,h = self.grabImage(animal_pos)

    def check_out_fight_in_team(self):
        self.check_cache()
        cv_team,w,h = self.grabImage(team_pos)
        res = cv2.matchTemplate(cv_team, self.team_template, eval('cv2.TM_CCOEFF'))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print max_val
        return max_val >= 15000000.0

    def check_if_in_fight(self):
        self.check_cache()
        cv_fight,w,h = self.grabImage(animal_fight_pos)
        res = cv2.matchTemplate(cv_fight, self.anim_template, eval('cv2.TM_CCOEFF'))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val >= 15000000.0

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
            pyautogui.rightClick(self.x+red_pos[0]-100,
                                 self.y+red_pos[1])
            time.sleep(0.2)
            pyautogui.rightClick(self.x+blue_pos[0]-100,
                                 self.y+blue_pos[1])
            time.sleep(0.2)
            if count > 1:
                pyautogui.hotkey('ctrl', 'tab')
                # pyautogui.press('tab')
                # pyautogui.keyUp('ctrl')

    def attack(self, pos):
        pyautogui.hotkey('alt', 'a')
        try:
            pyautogui.click(self.x+pos[0], self.y+pos[1])
        except:
            pass

    def click(self, pos):
        try:
            pyautogui.click(self.x+pos[0], self.y+pos[1])
        except:
            pass

    def rightClick(self, pos):
        try:
            pyautogui.rightClick(self.x+pos[0], self.y+pos[1])
        except:
            pass

    def click_smap(self, pos, begin, scale):
        relative_pos = [
            int(begin[0]+pos[0]*scale[0]),
            int(begin[1]-pos[1]*scale[1])
        ]
        pyautogui.hotkey('alt', '1')
        time.sleep(0.75)
        try:
            pyautogui.click(self.x+relative_pos[0], self.y+relative_pos[1])
        except:
            pass
        time.sleep(0.5)
        pyautogui.hotkey('alt', '1')

    def check_region_score(self, template, region, score):
        cv_region,w,h = self.grabImage(region)
        res = cv2.matchTemplate(cv_region, template, eval('cv2.TM_CCOEFF'))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return max_val >= score

xy2_win = WindowMgr()
