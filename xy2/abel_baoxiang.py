#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_map, abel_words, abel_log
import cv2
import pyscreenshot as ImageGrab
import pyautogui
import win32gui
import time, random

class xy2_baoxiang:
    def __init__(self, number = 1):
        self.quit = False
        self.count = number
        self.win = abel_window.xy2_win
        self.role_status = abel_window.s_in_team

    def quit(self):
        self.quit = True

    def accept_task(self):
        #get the task
        p2 = abel_map.point(x, y, abel_map.py.to('宝象国'), 'click')
        p3 = abel_map.point(x, y, abel_map.py.to('宝象国'), 'click')
        #close the task window
        self.w.click(x, y)
        #recognize the task by tesseract
        self.task = abel_words.get_bxxm_task_description()

    def analize_normal_task(self):
        tmp = ''.join(self.task).split('(')
        if len(tmp) < 2:
            message = 'ERROR: ' + self.task
            abel_log.write_to_log(message)
            return '',[]
        tmp1 = tmp[1].split(')')[0]
        tmp2 = tmp1.split(',')
        if len(tmp2) != 3:
            message = 'ERROR: ' + self.task
            abel_log.write_to_log(message)
            return '',[]
        message = 'SUCCESS: ' + ' '.join(tmp2)
        abel_log.write_to_log(message)
        return abel_map.py.to(tmp2[0]), [int(tmp2[1]), int(tmp2[2])]

    def analize_longma_task(self):
        c = ''
        if self.task[2] == '火':
            c = ''.join(self.task[2:6])
        else:
            c = ''.join(self.task[2:5])
        tmp = ''.join(self.task).split('(')
        if len(tmp) < 3:
            message = 'ERROR: ' + self.task
            abel_log.write_to_log(message)
            return '',[],[]
        tmp1 = tmp[1].split(')')[0]
        tmp2 = tmp[2].split(')')[0]
        tmp11= tmp1.split(',')
        tmp21= tmp2.split(',')
        if len(tmp11) != 2 or len(tmp21) != 2:
            message = 'ERROR: ' + self.task
            abel_log.write_to_log(message)
            return '',[],[]
        message = 'SUCCESS: ' + ' '.join(tmp11) + ' '.join(tmp21)
        abel_log.write_to_log(message)
        return abel_map.py.to(c), [int(tmp11[0]), int(tmp11[1])], [int(tmp21[0]), int(tmp21[1])]

    def do_naomrl_task(self, city, pos):
        if city == '':
            self.cancel_task()
            return True
        router = abel_map.src_bx_map.get(city)
        if router is None:
            self.cancel_task()
            return True
        router.addDst(pos)
        if router.go() == False:
            return False
        return self.attack(city, pos)

    def do_longma_task(self, city, pos1, pos2):
        if city == '':
            self.cancel_task()
            return True
        router = abel_map.src_bx_map.get(city)
        if router is None:
            self.cancel_task()
            return True
        router.addDst(pos1)
        if router.go() == False:
            return False
        refresh_task = abel_words.get_bxxm_task_description()
        if refresh_task[0] == '白':
            return self.attack(city, pos1)
        else:
            p2 = abel_map.point(pos2, city, 'click_map', d=pos2)
            p2.click()
            return self.attack(city, pos2)

    def cancel_task(self):
        #cancel the task
        p2 = abel_map.point(x, y, abel_map.py.to('宝象国'), 'click')
        p3 = abel_map.point(x, y, abel_map.py.to('宝象国'), 'click')
        p3 = abel_map.point(x, y, abel_map.py.to('宝象国'), 'click')
        #close the task window
        self.win.click(x, y)

    def attack(self, c, pos):
        attack_points = abel_map.get_nine_attack(c, pos)
        find_attack = False
        for p in attack_points:
            self.win.attack(p)
            time.sleep(0.5)
            if self.win.check_out_fight_in_team() == False:
                find_attack = True
                break
        while find_attack:
            if self.win.check_out_fight_in_team() == True:
                self.back_to_start()
                break
            time.sleep(0.1)
        return find_attack

    def back_to_start(self):
        pass

    def excute_one_task(self):
        #move to a fixed position
        p1 = abel_map.point(abel_window.bxxm_start_pos,
                            abel_map.py.to('宝象国'),
                            'click_map',
                            d=abel_window.bxxm_start_pos)
        p1.click()
        self.accept_task()
        result = False
        if p1.task[0] == '前' and p1.[1] == '往':
            c,pos1,pos2 = self.analize_longma_task()
            result = self.do_longma_task(c, pos1, pos2)
        else:
            c,pos = self.analize_normal_task()
            result = self.do_naomrl_task(c, pos)
        return result

    def run_task(self):
        drink_drug          = False
        in_out_fight_count  = 0
        out_fight_count     = 0
        check_in_team_count = 0
        if self.win._find == False:
            print 'can\'t find xy2 window.'
            return False

        self.win.set_foreground()
        while self.bquit == False:
            try:
                if self.role_status == abel_window.s_in_team:
                    if self.excute_one_task() == False:
                        self.role_status = abel_window.s_not_moved
            except:
                pass
