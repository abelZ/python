#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_checking
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

    def prepareEnvironment(self):
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        if w._find == False:
            print 'can\'t find xy2 window.'
            return False

        w.set_foreground()
        rect          = win32gui.GetWindowRect(w._handle)
        self.x_offset = rect[0]
        self.y_offset = rect[1]
        x_head_begin  = self.x_offset + abel_window.head_pos[0]
        y_head_begin  = self.y_offset + abel_window.head_pos[1]
        x_head_end    = x_head_begin + abel_window.head_pos[2]
        y_head_end    = y_head_begin + abel_window.head_pos[3]
        self.cv_template = abel_checking.grabImage(
            box=[x_head_begin, y_head_begin, x_head_end, y_head_end]
        )
        x_anim_begin = self.x_offset + abel_window.animal_pos[0]
        y_anim_begin = self.y_offset + abel_window.animal_pos[1]
        x_anim_end   = x_anim_begin + abel_window.animal_pos[2]
        y_anim_end   = y_anim_begin + abel_window.animal_pos[3]
        self.cv_template2 = abel_checking.grabImage(
            box=[x_anim_begin, y_anim_begin, x_anim_end, y_anim_end]
        )

    def run_task(self):
        drink_drug          = False
        in_out_fight_count  = 0
        out_fight_count     = 0
        check_in_team_count = 0
        if !prepareEnvironment():
            return

        while self.bquit == False:
            try:
                time.sleep(1)
                #check if it's in team
                x_team_begin = x_offset + abel_window.team_pos[0]
                y_team_begin = y_offset + abel_window.team_pos[1]
                x_team_end = x_team_begin + abel_window.team_pos[2]
                y_team_end = y_team_begin + abel_window.team_pos[3]
                b_in_team = abel_checking.check_out_fight_in_team(
                    box=[x_team_begin, y_team_begin, x_team_end, y_team_end],
                    template = self.cv_template
                )
                if !b_in_team:
                    x_anim_fight_begin = x_offset + abel_window.animal_fight_pos[0]
                    y_anim_fight_begin = y_offset + abel_window.animal_fight_pos[1]
                    x_anim_fight_end = x_anim_fight_begin + abel_window.animal_fight_pos[2]
                    y_anim_fight_end = y_anim_fight_begin + abel_window.animal_fight_pos[3]
                    b_in_fight = abel_checking.check_if_in_fight(
                        box=[
                            x_anim_fight_begin,
                            y_anim_fight_begin,
                            x_anim_fight_end,
                            y_anim_fight_end
                        ]
                    )
                    if !b_in_fight:
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
                            abel_window.clickAuto(self.count)
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
                        b_need_drug = abel_checking.checkInRange(
                            box=[],
                            lower=[],
                            upper=[]
                        )
                        if b_need_drug:
                            abel_window.clickDrug(self.x_offset, self.y_offset)
            except:
                pass

