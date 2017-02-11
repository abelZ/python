#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32gui, re

s_not_moved = 'not moved'
s_not_in_team = 'not in team'
s_in_team = 'in team'

#[x, y, w, h]
head_pos = [676, 56, 44, 44]
animal_pos = [568, 56, 42, 42]
team_pos = [250, 56, 300, 44]
animal_fight_pos = [0, 56, 84, 42]

#[x1, y1, x2, y2]
red_pos = [729, 73, 796, 82]
blue_pos = [730, 88, 797, 94]
drug_pos = [298, 378, 328, 408]
box_pos = [343, 367, 354, 390]

wild_pos = [[283,231], [468,283], [378,451], [270,388], [530,367]]
nao_pos = [[0,0], [0,0], [0,0], [0,0], [0,0]]

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None
        self._find = False

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

