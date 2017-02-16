#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import os, time, random

class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = dict_file


    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with file(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]


    def hanzi2pinyin(self, string=""):
        result = []
        if not isinstance(string, unicode):
            string = string.decode("utf-8")

        for char in string:
            key = '%X' % ord(char)
            value = self.word_dict.get(key, char).split()[0][:-1].lower()
            if value != u'':
                result.append(value)

        return result


    def to(self, string, split=" "):
        result = self.hanzi2pinyin(string)
        return split.join(result)

py = PinYin()
py.load_word()
w = abel_window.WindowMgr()
w.find_window_wildcard(".*Revision.*ID.*")
rect = win32gui.GetWindowRect(w._handle)

def chinese_to_english(cstr):
    return py.to(cstr)

class point:
    def __init__(self, x, y, p, e):
        self.x = x
        self.y = y
        self.pos = p
        self.event = e

    def click(self):
        if self.event == 'click_map':
            pyautogui.keyDown('alt')
            pyautogui.press('1')
            pyautogui.keyUp('alt')
            time.sleep(0.5)
        pyautogui.click()
        if self.event == 'click_map':
            time.sleep(0.5)
            pyautogui.keyDown('alt')
            pyautogui.press('1')
            pyautogui.keyUp('alt')

    def position(self):
        return self.pos

    def coordinate(self):
        return [self.x, self.y]

class xy2_map:
    def __init__(self):
        self.road = []
        pass

    def addDst(self, x, y):
        pass

    def route(self):
        for point in self.road:
            point.click()

class xy2_map_bx_hygb(xy2_map):
    def __init__(self):
        self.route = [
            point(275, 300, py.to('宝象国'), 'click_map'),
            point(487, 89, py.to('宝象国'), 'click'),
            point(233, 377, py.to('宝象国'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route
        self.road.append(point(x, y, py.to('火云戈壁'), 'click_map'))

class xy2_map_bx_hyd(xy2_map):
    def __init__(self):
        self.route = [
            point(275, 300, py.to('宝象国'), 'click_map'),
            point(487, 89, py.to('宝象国'), 'click'),
            point(233, 377, py.to('宝象国'), 'click')
            point(x, y, py.to('火云戈壁'), 'click_map'),
            point(x, y, py.to('火云戈壁'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route
        #find map
        #add them to map

class xy2_map_bx_jdd(xy2_map):
    def __init__(self):
        self.route = [
            point(275, 300, py.to('宝象国'), 'click_map'),
            point(487, 89, py.to('宝象国'), 'click'),
            point(233, 377, py.to('宝象国'), 'click')
            point(x, y, py.to('火云戈壁'), 'click_map'),
            point(x, y, py.to('火云戈壁'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route
        #

class xy2_map_bx_pds(xy2_map):
    def __init__(self):
        self.route = [
            point(493, 474, py.to('宝象国'), 'click_map'),
            point(279, 283, py.to('宝象国'), 'click'),
            point(259, 379, py.to('宝象国'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route
        self.road.append(point(x, y, py.to('平顶山'), 'click_map'))

class xy2_map_bx_byd(xy2_map):
    def __init__(self):
        self.route = [
            point(493, 474, py.to('宝象国'), 'click_map'),
            point(279, 283, py.to('宝象国'), 'click'),
            point(259, 379, py.to('宝象国'), 'click')
            point(x, y, py.to('平顶山'), 'click_map'),
            point(x, y, py.to('平顶山'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route

class xy2_map_bx_lhd(xy2_map):
    def __init__(self):
        self.route = [
            point(493, 474, py.to('宝象国'), 'click_map'),
            point(279, 283, py.to('宝象国'), 'click'),
            point(259, 379, py.to('宝象国'), 'click')
            point(x, y, py.to('平顶山'), 'click_map'),
            point(x, y, py.to('平顶山'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route

class xy2_map_bx_ssz(xy2_map):
    def __init__(self):
        self.route = [
            point(493, 474, py.to('宝象国'), 'click_map'),
            point(279, 283, py.to('宝象国'), 'click'),
            point(216, 394, py.to('宝象国'), 'click')
            point(355, 273, py.to('长安城'), 'click'),
            point(224, 353, py.to('长安城'), 'click'),
            point(356, 254, py.to('长安城'), 'click'),
            point(240, 411, py.to('长安城'), 'click'),
            point(363, 244, py.to('洛阳城'), 'click'),
            point(218, 363, py.to('洛阳城'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route
        self.road.append(point(x, y, py.to('四圣庄'), 'click_map'))

class xy2_map_bx_wss(xy2_map):
    def __init__(self):
        self.route = [
            point(x, y, py.to('宝象国'), 'click_map'),
            point(x, y, py.to('宝象国'), 'click'),
            point(x, y, py.to('宝象国'), 'click'),
            point(x, y, py.to('长安城'), 'click'),
            point(x, y, py.to('长安城'), 'click'),
            point(x, y, py.to('长安城'), 'click'),
            point(x, y, py.to('长安城'), 'click')
        ]

    def addDst(self, x, y):
        self.road = self.route
        self.road.append(point(x, y, py.to('万寿山'), 'click_map'))

class xy2_map_bx_bgs(xy2_map):
    def __init__(self):
        self.route = [
            point(x, y, py.to('宝象国'), 'click_map'),
            point(x, y, py.to('宝象国'), 'click'),
            point(x, y, py.to('宝象国'), 'click'),
            point(x, y, py.to('长安城'), 'click'),
            point(x, y, py.to('长安城'), 'click'),
            point(x, y, py.to('长安城'), 'click'),
            point(x, y, py.to('长安城'), 'click'),
            point(x, y, py.to('白骨洞'), 'click')
        ]

    def addDst(self):
        self.road = self.route
        self.road.append(point(x, y, py.to(白骨山), 'click_map'))

src_bx_dst = [
    py.to('火云洞'),
    py.to('金兜洞'),
    py.to('波月洞'),
    py.to('平顶山'),
    py.to('莲花洞'),
    py.to('四圣庄'),
    py.to('万寿山'),
    py.to('白骨山'),
    py.to('火云戈壁')
]
src_bx_map = {
    py.to('火云洞') : bx_hyd,
    py.to('金兜洞') : bx_jdd,
    py.to('波月洞') : bx_byd,
    py.to('平顶山') : bx_pds,
    py.to('莲花洞') : bx_lhd,
    py.to('四圣庄') : bx_ssz,
    py.to('万寿山') : bx_wss,
    py.to('白骨山') : bx_bgs,
    py.to('火云戈壁') : bx_hygb
}

