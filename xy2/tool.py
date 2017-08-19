#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_words, abel_map, abel_log, abel_baoxiang
import pyscreenshot as ImageGrab
import win32gui
import pyautogui
import sys, time
from multiprocessing import freeze_support
import cv2
import winsound, ctypes

def can_see(p1, p2):
    if abs(p1[0] - p2[0]) <= 20 and abs(p1[1] - p2[1]) <= 15:
        return True
    else:
        return False

if __name__ == '__main__':
    freeze_support()
    w = abel_window.xy2_win
    w.find_window_wildcard(".*Revision.*ID.*")
    if w._find == True:
        w.set_foreground()
    x,y = w.offset()
    if sys.argv[1] == '-pos':
        cursor = win32gui.GetCursorPos()
        print cursor[0] - x, cursor[1] - y
    elif sys.argv[1] == '-bxxm':
        im_head = ImageGrab.grab(
            bbox=(
                x + abel_window.bxxm_pos[0],
                y + abel_window.bxxm_pos[1],
                x + abel_window.bxxm_pos[2],
                y + abel_window.bxxm_pos[3]
            )
        )
        im_head.save(sys.argv[1]+'.png')
    elif sys.argv[1] == '-cord':
        # attack_points = abel_map.get_nine_attack(abel_map.py.to('平顶山'), [132,10])
        # for p in attack_points:
            # w.attack(p)
            # print p
            # time.sleep(0.5)
            # if w.check_out_fight_in_team() == False:
                # find_attack = True
                # break
        t = abel_baoxiang.xy2_baoxiang(4)
        i = 0
        while True:
            i += 1
            if i == 5:
                i = 0
                t.clickAuto()
            for index in range(1):
                if w.checkBlueEnough() == False:
                    w.drinkBlue()
                if w.checkRedEnough() == False:
                    w.drinkRed()
                pyautogui.keyDown('ctrl')
                pyautogui.press('tab')
                pyautogui.keyUp('ctrl')
            if t.excute_one_task() == False:
                winsound.PlaySound('.\\resource\\not_moved.wav', winsound.SND_FILENAME)
                break
            time.sleep(1)
        # t.back_to_start()
        # time.sleep(2)
        # t.excute_one_task()
        # t = abel_words.get_coordinate_text()
        # abel_log.printGbk(''.join(t))
        # m = abel_map.src_bx_map.get(abel_map.py.to('白骨山'))
        # m.addDst([152, 91])
        # m.go()

        # abel_window.xy2_win.click([493,474])
        # abel_window.xy2_win.click([275,300])
        # zero = [158, 506]
        # dst = [180,140]
        # cord = [158+180*1.513, 506-140*1.51]
        # pyautogui.keyDown('alt')
        # pyautogui.press('1')
        # pyautogui.keyUp('alt')
        # time.sleep(0.5)
        # pyautogui.click(x+cord[0], y+cord[1])
        # pyautogui.keyDown('alt')
        # pyautogui.press('1')
        # pyautogui.keyUp('alt')
        # cursor = win32gui.GetCursorPos()
        # pyautogui.click(cursor[0]+100, cursor[1])
        # time.sleep(20)
        # pyautogui.click(cursor[0]+200, cursor[1])
        # pyautogui.click(x+487, y+89)
        # time.sleep(0.5)
        # pyautogui.click(x+233, y+377)
        # print abel_words.get_bxxm_task_description(x, y, abel_window.coordinate_pos)
    elif sys.argv[1] == '-blue':
        t0 = time.clock()
        # m = abel_map.src_bx_map.get('ping ding shan')
        # m.addDst([100, 110])
        # m.go()
        start = [12,7]
        dst = [67,37]
        r1 = [[39,23],[59,32]]
        r2 = [[13,28], [20,40]]
        r3 = [[39,7], [60,14], [74,25]]
        rs = [r1, r2, r3]
        r = []
        if can_see(start, dst) == True:
            pass
        else:
            find = False
            for i in range(len(rs)):
                for j in range(len(rs[i])):
                    if can_see(dst, rs[i][j]):
                        find = True
                        r.append(rs[i][j])
                        break
                    else:
                        r.append(rs[i][j])
                if find == True:
                    break
                else:
                    r = []
        pos = abel_map.get_attack_points('huo yun dong', start)[0]
        pos1 = [pos[0]+(r[0][0]-start[0])*20, pos[1]-(r[0][1]-start[1])*20]
        print pos, pos1
        abel_window.xy2_win.rightClick(pos1)
        time.sleep(10)
        pos2 = abel_map.get_attack_points('huo yun dong', r[0])[0]
        pos3 = [pos2[0]+(r[1][0]-r[0][0])*20, pos2[1]-(r[1][1]-r[0][1])*20]
        print pos2, pos3
        abel_window.xy2_win.rightClick(pos3)
        print 'cost %.2f' % (time.clock() - t0)
        # pyautogui.press('s')
        # pyautogui.press('s')
        # pyautogui.press('z')
        # pyautogui.typewrite('ssz ', interval=0.25)
        # pyautogui.press('space')
        # pyautogui.press('enter')
        # t0 = time.clock()
        # router = abel_map.src_bx_map.get('bai gu shan')
        # router.addDst([100, 110])
        # print router.go()
        # print 'cost %.2f' % (time.clock() - t0)
        # for i in range(50):
            # print i
            # pyautogui.moveTo(x+392, y+250)
            # time.sleep(2)
        # print w.checkBlueEnough()
        # w.drinkBlue()
        # w.drinkRed()
    elif sys.argv[1] == '-capture':
        t = abel_baoxiang.xy2_baoxiang(4)
        t.run_task()
        # cv_image,w,h = w.grabImage()
        # cv2.imwrite(sys.argv[2], cv_image)
    elif sys.argv[1] == '-biao':
        try:
            while True:
                time.sleep(1)
                pyautogui.hotkey('alt', 'q')
                time.sleep(1)
                # w.click([209,471])
                # time.sleep(1)
                w.click([524,259])
                time.sleep(1)
                pyautogui.hotkey('alt', 'q')
        except Exception as e:
            print e


