#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window
import cv2
import pyscreenshot as ImageGrab
import pyautogui
import win32gui
import time, random

class xy2_bidou:
    def __init__(self, number = 1):
        self.count = number
        self.bquit = False
        self.role_status = abel_window.s_in_team

    def quit(self):
        self.bquit = True

    def run_task(self):
        im_anim_cap       = '.\\auto\\animal_capture.png'
        im_anim_fight_cap = '.\\auto\\annimal_fight_capture.png'
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
        animal_captured      = False
        status_change_by_out = False
        last_status_out      = False
        cv_template2         = None
        while self.bquit == False:
            try:
                time.sleep(1)
                if animal_captured == False:
                    animal_captured = True
                    x_anim_begin = x_offset + abel_window.animal_pos[0]
                    y_anim_begin = y_offset + abel_window.animal_pos[1]
                    x_anim_end = x_anim_begin + abel_window.animal_pos[2]
                    y_anim_end = y_anim_begin + abel_window.animal_pos[3]
                    im_anim = ImageGrab.grab(
                        bbox=(
                            x_anim_begin,
                            y_anim_begin,
                            x_anim_end,
                            y_anim_end
                        )
                    )
                    im_anim.save(im_anim_cap)
                    cv_template2 = cv2.imread(im_anim_cap, 0)

                x_anim_fight_begin = x_offset + abel_window.animal_fight_pos[0]
                y_anim_fight_begin = y_offset + abel_window.animal_fight_pos[1]
                x_anim_fight_end = x_anim_fight_begin + abel_window.animal_fight_pos[2]
                y_anim_fight_end = y_anim_fight_begin + abel_window.animal_fight_pos[3]
                im_anim_fight = ImageGrab.grab(
                    bbox=(
                        x_anim_fight_begin,
                        y_anim_fight_begin,
                        x_anim_fight_end,
                        y_anim_fight_end
                    )
                )
                im_anim_fight.save(im_anim_fight_cap)
                cv_fight = cv2.imread(im_anim_fight_cap, 0)
                method = eval('cv2.TM_CCOEFF')
                res = cv2.matchTemplate(cv_fight, cv_template2, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                print 'animal match %f' % max_val
                if max_val >= 4500000.0:
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

                    for i in range(self.count):
                        pyautogui.click(
                            random.randint(
                                x_offset+abel_window.bidou_pos[0],
                                x_offset+abel_window.bidou_pos[2]
                            ),
                            random.randint(
                                y_offset+abel_window.bidou_pos[1],
                                y_offset+abel_window.bidou_pos[3]
                            )
                        )
                        time.sleep(0.5)
                        if self.count > 1:
                            pyautogui.keyDown('ctrl')
                            pyautogui.press('tab')
                            pyautogui.keyUp('ctrl')
            except:
                print e
                pass

