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
        if self.win._find == False:
            self.win.find_window_wildcard(".*Revision.*ID.*")
            self.win.check_out_fight_in_team()
            self.win.check_if_in_fight()
        self.role_status = abel_window.s_in_team
        self.fight = 0
        self.begin_point = abel_map.point([90, 85],
                                          abel_map.py.to('宝象国'),
                                          'click_map',
                                          d = [89, 85],
                                          satisfy = '.\\resource\\bx_task.bmp',
                                          satisfy_region = [220,65,288,146],
                                          satisfy_score = 19000000.0)

    def quit(self):
        self.quit = True

    def clickAuto(self):
        self.auto = True

    def go_to_begin(self):
        if self.win.check_region_score(self.begin_point.satisfy,
                                       self.begin_point.satisfy_region,
                                       self.begin_point.satisfy_score) == False:
            self.begin_point.click()

    def accept_task(self):
        self.go_to_begin()
        abel_log.write_to_log('accept task')
        #get the task
        p2 = abel_map.point([[345,255],[258,358]], abel_map.py.to('宝象国'), 'click_multiple')
        p2.click()
        #close the task window
        self.refresh()
        #recognize the task by tesseract
        self.task = abel_words.get_bxxm_task_description()

    def analize_normal_task(self):
        tmp = self.task.split('(')
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
        message = c + ' ' + ','.join(tmp2)
        abel_log.write_to_log(message)
        return abel_map.py.to(tmp2[0]), [int(tmp2[1]), int(tmp2[2])]

    def analize_longma_task(self):
        c = ''
        if self.task[6:9] == '火':
            c = self.task[6:18]
        else:
            c = self.task[6:15]
        tmp = self.task.split('(')
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
        message = c +' ' + ','.join(tmp11) + ' ' + ','.join(tmp21)
        abel_log.write_to_log(message)
        return abel_map.py.to(c), [int(tmp11[0]), int(tmp11[1])], [int(tmp21[0]), int(tmp21[1])]

    def do_naomrl_task(self, router, pos, city):
        router.addDst(pos)
        router.road[0].click_without_check()
        self.check_drug()
        if router.go() == False:
            return False
        return self.attack(city, pos)

    def do_longma_task(self, router, pos1, pos2, city):
        router.addDst(pos1)
        router.road[0].click_without_check()
        self.check_drug()
        if router.go() == False:
            return False
        self.back_to_start()
        refresh_task = abel_words.get_bxxm_task_description()
        if refresh_task[0:3] == '白':
            self.refresh()
            return self.attack(city, pos1)
        else:
            p = abel_map.point(pos2, city, 'click_map', d=pos2, fly=True)
            p.click()
            self.back_to_start()
            self.refresh()
            return self.attack(city, pos2)

    def cancel_task(self):
        self.go_to_begin()
        abel_log.write_to_log('cancel this task')
        # self.go_to_begin()
        pos = [[345,255],[249,375],[164,344]]
        for i in range(len(pos)):
            self.win.click(pos[i])
            time.sleep(0.5)

    def cancel_task2(self):
        self.go_to_begin()
        abel_log.write_to_log('cancel this task2')
        # self.go_to_begin()
        pos = [[345,255],[222,395],[170,343]]
        for i in range(len(pos)):
            self.win.click(pos[i])
            time.sleep(0.5)

    def attack(self, c, pos):
        attack_points = abel_map.get_attack_points(c, pos)
        find_attack = False
        for p in attack_points:
            self.win.attack(p)
            time.sleep(1)
            if self.win.check_if_in_fight() == True:
                abel_log.write_to_log('attack ' + str(p) + ' success')
                find_attack = True
                self.fight += 1
                if self.fight % 5 == 0:
                    self.win.clickAuto(self.count)
                break
            else:
                abel_log.write_to_log('attack ' + str(p) + ' fail')
        while find_attack:
            if self.win.check_out_fight_in_team() == True:
                time.sleep(0.5)
                self.back_to_start()
                abel_log.write_to_log('back to start')
                break
            time.sleep(0.1)
        return find_attack

    def back_to_start(self):
        time.sleep(0.1)
        pyautogui.keyDown('alt')
        pyautogui.press('e')
        pyautogui.keyUp('alt')
        time.sleep(0.5)
        self.win.click([348,557])
        time.sleep(0.5)
        self.win.rightClick([310,442])
        pyautogui.keyDown('alt')
        pyautogui.press('e')
        pyautogui.keyUp('alt')
        time.sleep(0.1)

    def refresh(self):
        time.sleep(0.1)
        pyautogui.keyDown('alt')
        pyautogui.press('e')
        pyautogui.keyUp('alt')
        time.sleep(0.25)
        self.win.click([348,385])
        time.sleep(0.5)
        self.win.rightClick([203,543])
        time.sleep(0.5)
        self.win.click([187,480])
        time.sleep(0.25)
        pyautogui.keyDown('alt')
        pyautogui.press('e')
        pyautogui.keyUp('alt')
        time.sleep(0.1)

    def check_drug(self):
        self.win.drinkDrug(self.count)

    def excute_one_task(self):
        result = False
        for i in range(5):
            self.accept_task()
            if self.task[0:3] == '前' and self.task[3:6] == '往':
                c,pos1,pos2 = self.analize_longma_task()
                router = abel_map.src_bx_map.get(c)
                if router is None:
                    self.cancel_task()
                    continue
                result = self.do_longma_task(router, pos1, pos2, c)
            elif self.task[0:3] == '三':
                c,pos = self.analize_normal_task()
                router = abel_map.src_bx_map.get(c)
                if router is None:
                    self.cancel_task()
                    continue
                result = self.do_naomrl_task(router, pos, c)
            elif self.task[0:3] == '义':
                self.cancel_task2()
                continue
            else:
                self.refresh()
                self.go_to_begin()
            break
        return result

    def run_task(self):
        if self.win._find == False:
            print 'can\'t find xy2 window.'
            return False

        self.win.set_foreground()
        while self.bquit == False:
            try:
                if self.excute_one_task() == False:
                    break
            except:
                pass
