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
        animal_captured     = False
        head_captured       = False
        drink_drug          = False
        in_out_fight_count  = 0
        out_fight_count     = 0
        check_in_team_count = 0
        w = abel_window.WindowMgr()
        w.find_window_wildcard(".*Revision.*ID.*")
        if w._find == False:
            print 'can\'t find xy2 window.'
            return

        w.set_foreground()
        rect              = win32gui.GetWindowRect(w._handle)
        x_offset          = rect[0]
        y_offset          = rect[1]
        im_head_cap       = '.\\auto\\head_capture.png'
        im_team_cap       = '.\\auto\\team_capture.png'
        im_anim_cap       = '.\\auto\\animal_capture.png'
        im_anim_fight_cap = '.\\auto\\annimal_fight_capture.png'
        cv_template       = None
        cv_template2      = None
        while self.bquit == False:
            try:
                time.sleep(1)
                #check if it's in team
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
                    if max_val < 4500000.0:
                        check_in_team_count = check_in_team_count + 1
                        if check_in_team_count == 5:
                            self.role_status = abel_window.s_not_in_team
                            check_in_team_count = 0
                    else:
                        if out_fight_count > 0:
                            in_out_fight_count = in_out_fight_count + 1
                            out_fight_count = 0
                        check_in_team_count = 0
                        self.role_status = abel_window.s_in_team
                        if in_out_fight_count >= 4:
                            in_out_fight_count = 0
                            drink_drug = True
                            for i in range(self.count):
                                pyautogui.keyDown('alt')
                                pyautogui.press('8')
                                pyautogui.keyUp('alt')
                                if self.count > 1:
                                    pyautogui.keyDown('ctrl')
                                    pyautogui.press('tab')
                                    pyautogui.keyUp('ctrl')
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
                        pyautogui.keyDown('alt')
                        pyautogui.press('e')
                        pyautogui.keyUp('alt')
                        time.sleep(0.5)
                        pyautogui.rightClick(
                            random.randint(
                                x_offset+abel_window.drug_pos[0],
                                x_offset+abel_window.drug_pos[2]
                            ),
                            random.randint(
                                y_offset+abel_window.drug_pos[1],
                                y_offset+abel_window.drug_pos[3]
                            )
                        )
                        time.sleep(0.5)
                        pyautogui.keyDown('alt')
                        pyautogui.press('e')
                        pyautogui.keyUp('alt')
            except:
                pass

