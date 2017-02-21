#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window
import cv2
import pyscreenshot as ImageGrab
import pyautogui
import win32gui
import time, random

class xy2_nao:
    def __init__(self, number = 1):
        self.count = number
        self.bquit = False
        self.role_status = abel_window.s_in_team

    def quit(self):
        self.bquit = True

    def run_task(self):
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        if w._find == False:
            print 'can\'t find xy2 window.'
            return

        w.set_foreground()
        in_out_fight_count   = 0
        out_fight_count      = 0
        drink_drug           = True
        status_change_by_out = False
        last_status_out      = False
        while self.bquit == False:
            try:
                time.sleep(3)
                if w.check_out_fight_in_team() == False:
                    if last_status_out == True:
                        in_out_fight_count = in_out_fight_count + 1
                        last_status_out = False

                    if status_change_by_out == True:
                        self.role_status = abel_window.s_in_team
                        status_change_by_out = False

                    drink_drug = True
                    out_fight_count = 0
                    if in_out_fight_count >= 5:
                        in_out_fight_count = 0
                        w.clickAuto(self.count)
                else:
                    if last_status_out == False:
                        last_status_out = True

                    if drink_drug and self.role_status != abel_window.s_not_moved:
                        drink_drug = False
                        w.full_blue_red(self.count)

                    out_fight_count = out_fight_count + 1
                    if out_fight_count == 10:
                        out_fight_count = 0
                        self.role_status = abel_window.s_not_moved
                        status_change_by_out = True

                    if self.role_status != abel_window.s_not_moved:
                        index = random.randint(0, len(abel_window.nao_pos)-1)
                        w.attack(abel_window.nao_pos[index])
            except:
                pass

