#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_words, abel_log
import os, time, random
import cv2
import pyautogui

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
if len(py.word_dict) < 1:
    py.load_word()

def chinese_to_english(cstr):
    return py.to(cstr)

class xy2_city:
    def __init__(self, min_pos, max_cd, scale):
        self.s_map_min_pos = min_pos
        self.s_map_scale = scale
        self.s_map_max_coordinate = max_cd

city_map = {
    py.to('火云洞') : xy2_city([0,0], [89,60], [0,0]),
    py.to('火云戈壁') : xy2_city([161,487], [280,165], [1.76,1.75]),
    py.to('宝象国') : xy2_city([157,507], [328,216], [1.513,1.51]),
    py.to('平顶山') : xy2_city([158,484], [320,180], [1.55,1.57]),
    py.to('四圣庄') : xy2_city([263,480], [224,216], [1.28,1.27]),
    py.to('万寿山') : xy2_city([222,481], [224,168], [1.64,1.65]),
    py.to('白骨山') : xy2_city([197,480], [256,168], [1.63,1.63])
}

class point:
    def __init__(self,
                 p,
                 c,
                 e,
                 d=None,
                 num=1,
                 pinyin = None,
                 satisfy=None,
                 satisfy_region=None,
                 satisfy_score=0):
        self.pos = p
        self.city = c
        self.event = e
        self.count = num
        self.dst = d
        self.pinyin = pinyin
        self.satisfy = None
        self.satisfy_region = satisfy_region
        self.satisfy_score = satisfy_score
        if satisfy is not None:
            self.satisfy = cv2.imread(satisfy, 1)

    def __repr__(self):
        return self.city + ' ' + self.event + ' ' + str(self.pos)

    def click_without_check(self):
        d = self.dst
        self.dst = None
        self.click()
        self.dst = d

    def click(self):
        result = False
        if self.event == 'click_map':
            c = city_map[self.city]
            abel_window.xy2_win.click_smap(self.pos, c.s_map_min_pos, c.s_map_scale)
            result = self.check_arrival()
        elif self.event == 'fly_click_map':
            abel_window.xy2_win.click([672,613])
            time.sleep(0.75)
            abel_window.xy2_win.click([677,493])
            time.sleep(0.25)
            c = city_map[self.city]
            abel_window.xy2_win.click_smap(self.pos, c.s_map_min_pos, c.s_map_scale)
            time.sleep(0.25)
            abel_window.xy2_win.drinkDrug(self.count)
            result = self.check_arrival()
            abel_window.xy2_win.click([672,613])
            time.sleep(0.75)
            abel_window.xy2_win.click([677,493])
            time.sleep(0.25)
        elif self.event == 'click_multiple':
            for i in range(len(self.pos)):
                abel_window.xy2_win.click(self.pos[i])
                time.sleep(0.5)
            result = True
        elif self.event == 'right_click_multiple':
            abel_window.xy2_win.rightClick(self.pos[0])
            time.sleep(0.5)
            for i in range(len(self.pos)):
                abel_window.xy2_win.click(self.pos[i])
                time.sleep(0.5)
            result = True
        elif self.event == 'click_right':
            abel_window.xy2_win.rightClick(self.pos)
            result = self.check_arrival()
        elif self.event == 'auto_road':
            pyautogui.hotkey('alt', '2')
            time.sleep(0.5)
            abel_window.xy2_win.click([176,536])
            time.sleep(0.5)
            pyautogui.typewrite(self.pinyin, 0.25)
            pyautogui.press('enter')
            for i in range(3):
                time.sleep(0.1)
                abel_window.xy2_win.click([562,431])
            time.sleep(0.5)
            abel_window.xy2_win.click(self.pos[0])
            time.sleep(0.5)
            abel_window.xy2_win.rightClick([584,237])
            time.sleep(0.5)
            abel_window.xy2_win.click([584,237])
            time.sleep(0.5)
            pyautogui.hotkey('alt', '2')
            result = self.check_arrival()
            if result == True and len(self.pos) > 1:
                abel_window.xy2_win.click(self.pos[1])
                time.sleep(1.0)

        return result

    def check_arrival(self):
        if self.dst is None:
            return True

        arrival = False
        text = ''
        last_text = ''
        last_cord = []
        while True:
            time.sleep(0.25)
            try:
                text = abel_words.get_coordinate_text()
                tmp = text.split('(')[1].split(')')[0].split(',')
                cord = [int(tmp[0]), int(tmp[1])]
                if abs(cord[0]-self.dst[0]) <= 1 and abs(cord[1]-self.dst[1]) <= 1:
                    self.last_cord = cord
                    arrival = True
                    break
                else:
                    if cord == last_cord:
                        abel_log.write_to_log('same coordinate detected, exit road!')
                        break
                last_cord = cord
                last_text = text
            except Exception as e:
                abel_log.write_to_log(text)
                if text == last_text:
                    abel_log.write_to_log('same text detected, exit road!')
                    arrival = True
                    break
                last_text = text

        if self.satisfy is not None:
            arrival = False
            for i in range(10):
                time.sleep(0.01)
                if abel_window.xy2_win.check_region_score(
                    self.satisfy,
                    self.satisfy_region,
                    self.satisfy_score
                ) == True:
                    arrival = True
                    time.sleep(1.0)
                    break
            if arrival == False:
                abel_log.write_to_log('can not find satisfy region')

        return arrival

def get_attack_points(city, coordinate):
    max_w = 19
    max_h = 14
    center = [392, 331]
    cord = coordinate
    try:
        text = abel_words.get_coordinate_text()
        tmp = text.split('(')[1].split(')')[0].split(',')
        cord = [int(tmp[0]), int(tmp[1])]
    except:
        cord = coordinate

    max_cd = city_map.get(city).s_map_max_coordinate
    if cord[0] < max_w:
        center[0] = center[0] - (max_w-cord[0])*20
    elif cord[0] > max_cd[0]-max_w:
        center[0] = center[0] + (cord[0]+max_w-max_cd[0])*20

    if cord[1] < max_h:
        center[1] = center[1] + (max_h-cord[1])*20
    elif cord[1] > max_cd[1]-max_h:
        center[1] = center[1] - (cord[1]+max_h-max_cd[1])*20

    return [center, [center[0]+40, center[1]], [center[0]-20, center[1]]]

class xy2_map:
    def __init__(self):
        self.road = []
        pass

    def addDst(self, pos, count):
        pass

    def go(self):
        result = True
        for p in self.road:
            if p.click() == False:
                abel_log.write_to_log('X -> ' + str(p))
                result = False
                break
            else:
                abel_log.write_to_log('O -> ' + str(p))
        return result

class xy2_map_bx_hygb(xy2_map):
    def __init__(self):
        self.route = [
            point([[358,391],[204,376]], py.to('宝象国'), 'auto_road', d=[20,100], pinyin='huoygb ')
        ]

    def addDst(self, pos, count):
        self.road = [r for r in self.route]
        self.road.append(point(pos, py.to('火云戈壁'), 'fly_click_map', d=pos, num=count))

class xy2_map_bx_pds(xy2_map):
    def __init__(self):
        self.route = [
            point([[312,383],[203,360]], py.to('宝象国'), 'auto_road', d=[251,149], pinyin='pds ')
        ]

    def addDst(self, pos, count):
        self.road = [r for r in self.route]
        self.road.append(point(pos, py.to('平顶山'), 'fly_click_map', d=pos, num=count))

class xy2_map_bx_ssz(xy2_map):
    def __init__(self):
        self.route = [
            point([[354,392],[207,361]], py.to('宝象国'), 'auto_road', d=[360,68], pinyin='ssz ')
        ]

    def addDst(self, pos, count):
        self.road = [r for r in self.route]
        self.road.append(point(pos, py.to('四圣庄'), 'fly_click_map', d=pos, num=count))

class xy2_map_bx_wss(xy2_map):
    def __init__(self):
        self.route = [
            point([[349,392],[201,359]], py.to('宝象国'), 'auto_road', d=[253,91], pinyin='wss ')
        ]

    def addDst(self, pos, count):
        self.road = [r for r in self.route]
        self.road.append(point(pos, py.to('万寿山'), 'fly_click_map', d=pos, num=count))

class xy2_map_bx_bgs(xy2_map):
    def __init__(self):
        self.route = [
            point([[339,392]], py.to('宝象国'), 'auto_road', d=[18,149], pinyin='bgs ')
        ]

    def addDst(self, pos, count):
        self.road = [r for r in self.route]
        self.road.append(point(pos, py.to('白骨山'), 'fly_click_map', d=pos, num=count))

src_bx_map = {
    # py.to('火云洞') : xy2_map_bx_byd(),
    # py.to('金兜洞') : xy2_map_bx_jdd(),
    # py.to('波月洞') : xy2_map_bx_byd(),
    py.to('平顶山') : xy2_map_bx_pds(),
    # py.to('莲花洞') : xy2_map_bx_lhd(),
    py.to('四圣庄') : xy2_map_bx_ssz(),
    py.to('万寿山') : xy2_map_bx_wss(),
    py.to('白骨山') : xy2_map_bx_bgs(),
    py.to('火云戈壁') : xy2_map_bx_hygb()
}

