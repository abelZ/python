#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_words
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

def chinese_to_english(cstr):
    return py.to(cstr)

class xy2_city:
    def __init__(self, min_pos, max_cd, scale):
        self.s_map_min_pos = min_pos
        self.s_map_scale = scale
        self.s_map_max_coordinate = max_cd

city_map = {
    py.to('宝象国') : xy2_city([157,507], [328,216], [1.513,1.51]),
    py.to('火云戈壁') : xy2_city([161,487], [278,166], [1.76,1.75]),
    py.to('平顶山') : xy2_city([158,484], [318,180], [1.55,1.57]),
    py.to('四圣庄') : xy2_city([263,480], [222,216], [1.28,1.27]),
    py.to('万寿山') : xy2_city([222,481], [224,168], [1.64,1.65]),
    py.to('白骨山') : xy2_city([197,480], [254,168], [1.63,1.63])
}

def get_nine_attack(city, coordinate):
    center = abel_window.center_pos
    max_cd = city_map.get(city).s_map_max_coordinate
    fixed_cd = coordinate
    if fixed_cd[0] < 4:
        fixed_cd[0] = 4
    elif fixed_cd[0] > max_cd[0]-4:
        fixed_cd[0] = max_cd[0]-4

    if fixed_cd[1] < 4:
        fixed_cd[1] = 4
    elif fixed_cd[1] > max_cd[1]-4:
        fixed_cd[1] = max_cd[1]-4

    if fixed_cd[0] < 20:
        center[0] = center[0] - (20-fixed_cd[0])*20
    elif fixed_cd[0] > max_cd[0]-20:
        center[0] = center[0] + (fixed_cd[0]+20-max_cd[0])*20

    if fixed_cd[1] < 20:
        center[1] = center[1] + (20-fixed_cd[1])*20
    elif fixed_cd[1] > max_cd[1]-20:
        center[1] = center[1] - (fixed_cd[1]+20-max_cd[1])*20

    return [
        center,
        [center[0]-10, center[1]-10],
        [center[0]-10, center[1]+10],
        [center[0]+10, center[1]-10],
        [center[0]+10, center[1]+10],
        [center[0]-20, center[1]],
        [center[0]+20, center[1]],
        [center[0], center[1]-20],
        [center[0], center[1]+20],
        ]

class point:
    def __init__(self, p, c, e, d=None):
        self.pos = p
        self.city = c
        self.event = e
        self.dst = d

    def __repr__(self):
        return self.city + self.event + str(self.pos)

    def click(self):
        if self.event == 'click_map':
            c = city_map[self.city]
            abel_window.xy2_win.click_smap(self.pos, c.s_map_min_pos, c.s_map_scale)
            return self.check_arrival()
        elif self.event == 'click_double':
            abel_window.xy2_win.click(self.pos[0])
            time.sleep(0.5)
            abel_window.xy2_win.click(self.pos[1])
            time.sleep(0.5)
            return True
        elif self.event == 'click_right':
            abel_window.xy2_win.rightClick(self.pos)
            return self.check_arrival()
        return False

    def check_arrival(self):
        last_cord = []
        arrival = False
        while True:
            try:
                text = ''.join(abel_words.get_coordinate_text())
                tmp = text.split('(')[1].split(')')[0].split(',')
                cord = [int(tmp[0]), int(tmp[1])]
                if abs(cord[0]-self.dst[0]) <= 2 and abs(cord[1]-self.dst[1]) <= 2:
                    arrival = True
                    time.sleep(0.5)
                    break
                else:
                    if cord == last_cord:
                        break
                last_cord = cord
            except:
                pass
        return arrival

class xy2_map:
    def __init__(self):
        self.road = []
        pass

    def addDst(self, pos):
        pass

    def go(self):
        for p in self.road:
            print str(p)
            if p.click() == False:
                return False

class xy2_map_bx_hygb(xy2_map):
    def __init__(self):
        self.route = [
            point([77, 136], py.to('宝象国'), 'click_map', d=[77, 136]),
            point([[487, 89], [233, 377]], py.to('宝象国'), 'click_double', d=[186,72])
        ]

    def addDst(self, pos):
        self.road = self.route
        self.road.append(point(pos, py.to('火云戈壁'), 'click_map', d=pos))

class xy2_map_bx_hyd(xy2_map):
    def __init__(self):
        self.route = [
            point(77, 136, py.to('宝象国'), 'click_map'),
            point(487, 89, py.to('宝象国'), 'click'),
            point([233, 377], py.to('宝象国'), 'click', d=[186,72]),
            point([], py.to('火云戈壁'), 'click_map'),
            point([], py.to('火云戈壁'), 'click')
        ]

    def addDst(self, pos):
        self.road = self.route
        #find map
        #add them to map

class xy2_map_bx_jdd(xy2_map):
    def __init__(self):
        self.route = [
            point([77,136], py.to('宝象国'), 'click_map'),
            point([487,89], py.to('宝象国'), 'click'),
            point([233,377], py.to('宝象国'), 'click', d=[186,72]),
            point([], py.to('火云戈壁'), 'click_map'),
            point([], py.to('火云戈壁'), 'click')
        ]

    def addDst(self, pos):
        self.road = self.route

class xy2_map_bx_pds(xy2_map):
    def __init__(self):
        self.route = [
            point([221,21], py.to('宝象国'), 'click_map', d=[221,21]),
            point([[279,283],[259,379]], py.to('宝象国'), 'click_double', d=[20,100])
        ]

    def addDst(self, pos):
        self.road = self.route
        self.road.append(point(pos, py.to('平顶山'), 'click_map', d=pos))

class xy2_map_bx_byd(xy2_map):
    def __init__(self):
        self.route = [
            point([221,21], py.to('宝象国'), 'click_map'),
            point([279,283], py.to('宝象国'), 'click'),
            point([259,379], py.to('宝象国'), 'click', d=[20,100]),
            point([], py.to('平顶山'), 'click_map'),
            point([], py.to('平顶山'), 'click')
        ]

    def addDst(self, pos):
        self.road = self.route

class xy2_map_bx_lhd(xy2_map):
    def __init__(self):
        self.route = [
            point([221,21], py.to('宝象国'), 'click_map'),
            point([279,283], py.to('宝象国'), 'click'),
            point([259,379], py.to('宝象国'), 'click', d=[20,100]),
            point([], py.to('平顶山'), 'click_map'),
            point([], py.to('平顶山'), 'click')
        ]

    def addDst(self, pos):
        self.road = self.route

class xy2_map_bx_ssz(xy2_map):
    def __init__(self):
        self.route = [
            point([221,21], py.to('宝象国'), 'click_map', d=[221,21]),
            point([[279,283],[259,379]], py.to('宝象国'), 'click_double', d=[63,209]),
            point([[355,273],[224,353]], py.to('长安城'), 'click_double', d=[]),
            point([[356,254],[240,411]], py.to('长安城'), 'click_double', d=[]),
            point([[363,244],[218,363]], py.to('洛阳城'), 'click_double', d=[])
        ]

    def addDst(self, pos):
        self.road = self.route
        self.road.append(point(pos, py.to('四圣庄'), 'click_map', d=pos))

class xy2_map_bx_wss(xy2_map):
    def __init__(self):
        self.route = [
            point([221,21], py.to('宝象国'), 'click_map', d=[221,21]),
            point([[279,283],[259,379]], py.to('宝象国'), 'click_double', d=[63,209]),
            point([[355,273],[230,405]], py.to('长安城'), 'click_double', d=[]),
            point([[356,277],[226,428]], py.to('长安城'), 'click_double', d=[])
        ]

    def addDst(self, pos):
        self.road = self.route
        self.road.append(point(pos, py.to('万寿山'), 'click_map', d=pos))

class xy2_map_bx_bgs(xy2_map):
    def __init__(self):
        self.route = [
            point([221,21], py.to('宝象国'), 'click_map', d=[221,21]),
            point([[279,283],[259,379]], py.to('宝象国'), 'click_double', d=[63,209]),
            point([[355,273],[230,405]], py.to('长安城'), 'click_double', d=[]),
            point([[356,277],[207,447]], py.to('长安城'), 'click_double', d=[]),
            point([290,599], py.to('白骨洞'), 'click_right', d=[18,149])
        ]

    def addDst(self, pos):
        self.road = self.route
        self.road.append(point(pos, py.to('白骨山'), 'click_map', d=pos))

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

