#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abel_window
import cv2
import pyscreenshot as ImageGrab
import pyautogui
import win32gui
import time, random

class xy2_wild:
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
        in_fight_count       = 0
        out_fight_count    = 0
        head_captured        = False
        drink_drug           = False
        status_change_by_out = False
        status_change_by_in  = False
        last_status_out      = False
        cv_template          = None
        while self.bquit == False:
            try:
                time.sleep(1)
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
                    in_fight_count = in_fight_count + 1
                    if in_fight_count == 15:
                        in_fight_count = 0
                        self.role_status = abel_window.s_not_moved
                        status_change_by_in = True

                    if in_out_fight_count % 5 == 0:
                        for i in range(self.count):
                            pyautogui.keyDown('alt')
                            pyautogui.press('8')
                            pyautogui.keyUp('alt')
                            if self.count > 1:
                                pyautogui.keyDown('ctrl')
                                pyautogui.press('tab')
                                pyautogui.keyUp('ctrl')

                    if in_out_fight_count >= 15:
                        in_out_fight_count = 0
                        drink_drug = True

                else:
                    if last_status_out == False:
                        time.sleep(1)
                        last_status_out = True

                    if status_change_by_in == True:
                        status_change_by_in = False
                        status_change_by_out = True
                        self.role_status = abel_window.s_not_moved

                    in_fight_count = 0
                    if drink_drug:
                        drink_drug = False
                        time.sleep(0.5)
                        pyautogui.keyDown('alt')
                        pyautogui.press('e')
                        pyautogui.keyUp('alt')
                        time.sleep(0.5)
                        pyautogui.rightClick(
                            x_offset+abel_window.drug_pos[0],
                            y_offset+abel_window.drug_pos[1]
                        )
                        time.sleep(0.5)
                        pyautogui.keyDown('alt')
                        pyautogui.press('e')
                        pyautogui.keyUp('alt')

                    out_fight_count = out_fight_count + 1
                    if out_fight_count == 15:
                        out_fight_count = 0
                        self.role_status = abel_window.s_not_moved
                        status_change_by_out = True

                    if self.role_status != abel_window.s_not_moved:
                        rand_index = random.randint(0, len(abel_window.wild_pos)-1)
                        x_map_min = x_offset + abel_window.wild_pos[rand_index][0]-2
                        x_map_max = x_offset + abel_window.wild_pos[rand_index][0]+2
                        y_map_min = y_offset + abel_window.wild_pos[rand_index][1]-2
                        y_map_max = y_offset + abel_window.wild_pos[rand_index][1]+2
                        pyautogui.keyDown('alt')
                        pyautogui.press('1')
                        pyautogui.keyUp('alt')
                        time.sleep(0.5)
                        pyautogui.click(
                            random.randint(x_map_min, x_map_max),
                            random.randint(y_map_min, y_map_max)
                        )
                        time.sleep(0.5)
                        pyautogui.keyDown('alt')
                        pyautogui.press('1')
                        pyautogui.keyUp('alt')
            except:
                pass
