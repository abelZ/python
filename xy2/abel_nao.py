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
        im_head_cap = '.\\auto\\head_capture.png'
        im_team_cap = '.\\auto\\team_capture.png'
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        if w._find == False:
            print 'can\'t find xy2 window.'
            return

        w.set_foreground()
        rect                 = win32gui.GetWindowRect(w._handle)
        x_offset             = rect[0]
        y_offset             = rect[1]
        in_out_fight_count   = 0
        out_fight_count      = 0
        head_captured        = False
        drink_drug           = True
        status_change_by_out = False
        last_status_out      = False
        cv_template          = None
        while self.bquit == False:
            try:
                time.sleep(3)
                if head_captured == False:
                    head_captured = True
                    x_head_begin = x_offset + abel_window.head_pos[0]
                    y_head_begin = y_offset + abel_window.head_pos[1]
                    x_head_end = x_head_begin + abel_window.head_pos[2]
                    y_head_end = y_head_begin + abel_window.head_pos[3]
                    im_head = ImageGrab.grab(
                        bbox=(
                            x_head_begin,
                            y_head_begin,
                            x_head_end,
                            y_head_end
                        )
                    )
                    im_head.save(im_head_cap)
                    cv_template = cv2.imread(im_head_cap, 0)

                x_team_begin = x_offset + abel_window.team_pos[0]
                y_team_begin = y_offset + abel_window.team_pos[1]
                x_team_end = x_team_begin + abel_window.team_pos[2]
                y_team_end = y_team_begin + abel_window.team_pos[3]
                im_team = ImageGrab.grab(
                    bbox=(
                        x_team_begin,
                        y_team_begin,
                        x_team_end,
                        y_team_end
                    )
                )
                im_team.save(im_team_cap)

                cv_team = cv2.imread(im_team_cap, 0)
                method = eval('cv2.TM_CCOEFF')
                res = cv2.matchTemplate(cv_team, cv_template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                print 'team match %f' % max_val
                if max_val < 4500000.0:
                    if last_status_out == True:
                        in_out_fight_count = in_out_fight_count + 1
                        last_status_out = False

                    if status_change_by_out == True:
                        self.role_status = abel_window.s_in_team
                        status_change_by_out = False

                    out_fight_count = 0
                    if in_out_fight_count > 5:
                        in_out_fight_count = 0
                        for i in range(self.count):
                            pyautogui.keyDown('alt')
                            pyautogui.press('8')
                            pyautogui.keyUp('alt')
                            if self.count > 1:
                                pyautogui.keyDown('ctrl')
                                pyautogui.press('tab')
                                pyautogui.keyUp('ctrl')

                else:
                    if last_status_out == False:
                        time.sleep(1)
                        last_status_out = True

                    if drink_drug and self.role_status != abel_window.s_not_moved:
                        for i in range(self.count):
                            pyautogui.rightClick(
                                random.randint(
                                    x_offset+abel_window.red_pos[0],
                                    x_offset+abel_window.red_pos[2]
                                ),
                                random.randint(
                                    y_offset+abel_window.red_pos[1],
                                    y_offset+abel_window.red_pos[3]
                                )
                            )
                            time.sleep(0.5)
                            pyautogui.rightClick(
                                random.randint(
                                    x_offset+abel_window.blue_pos[0],
                                    x_offset+abel_window.blue_pos[2]
                                ),
                                random.randint(
                                    y_offset+abel_window.blue_pos[1],
                                    y_offset+abel_window.blue_pos[3]
                                )
                            )
                            time.sleep(0.5)
                            if self.count > 1:
                                pyautogui.keyDown('ctrl')
                                pyautogui.press('tab')
                                pyautogui.keyUp('ctrl')

                    out_fight_count = out_fight_count + 1
                    if out_fight_count == 10:
                        out_fight_count = 0
                        self.role_status = abel_window.s_not_moved
                        status_change_by_out = True

                    if self.role_status != abel_window.s_not_moved:
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('a')
                        index = random.randint(0, len(abel_window.nao_pos)-1)
                        pyautogui.click(
                            x_offset+abel_window.nao_pos[index][0],
                            y_offset+abel_window.nao_pos[index][1]
                        )
                        pyautogui.keyUp('a')
                        pyautogui.keyUp('alt')
            except:
                pass

