#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window
import cv2
import pyscreenshot as ImageGrab
import pyautogui
import win32gui
import time, random

class xy2_xiu:
    def __init__(self, number = 1):
        self.count = number
        self.bquit = False
        self.role_status = abel_window.s_in_team

    def quit(self):
        self.bquit = True

    def run_task(self):
        drink_drug          = True
        in_out_fight_count  = 0
        out_fight_count     = 0
        check_in_team_count = 0
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        if w._find == False:
            print 'can\'t find xy2 window.'
            return False

        w.set_foreground()
        while self.bquit == False:
            try:
                time.sleep(1)
                if w.check_out_fight_in_team() == False:
                    if w.check_if_in_fight() == False:
                        check_in_team_count = check_in_team_count + 1
                        if check_in_team_count == 5:
                            self.role_status = abel_window.s_not_in_team
                            check_in_team_count = 0
                    else:
                        if out_fight_count > 0:
                            in_out_fight_count = in_out_fight_count + 1
                            out_fight_count = 0
                            drink_drug = True
                        check_in_team_count = 0
                        self.role_status = abel_window.s_in_team
                        if in_out_fight_count >= 5:
                            in_out_fight_count = 0
                            w.clickAuto(self.count)
                else:
                    check_in_team_count = 0
                    if self.role_status != abel_window.s_not_moved:
                        self.role_status = abel_window.s_in_team

                    out_fight_count = out_fight_count + 1
                    if out_fight_count == 120:
                        out_fight_count = 0
                        self.role_status = abel_window.s_not_moved

                    if drink_drug:
                        drink_drug = False
                        if w.checkBlueEnough() == False:
                            print "drink drug"
                            w.drinkBlue()
                        if w.checkRedEnough() == False:
                            print 'drink red'
                            w.drinkRed()
            except:
                pass

