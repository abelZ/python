#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2, numpy
import pyscreenshot as ImageGrab

def grabImage(box=[]):
    im = ImageGrab.grab(bbox = box)
    (w, h) = im.size
    tmp = list(im.getdata())
    np_array = []
    index = 0
    for i in range(h):
        np_array.append(tmp[index:index+w])
        index += w
    srcRGB = numpy.array(np_array, dtype=numpy.uint8)
    return cv2.cvtColor(srcRGB, cv2.COLOR_RGB2BGR)

def checkInRange(box=[], lower=[], upper=[]):
    im = grabImage(box)
    mask = cv2.inRange(im, numpy.array(lower, dtype='uint8'), numpy.array(upper, dtype='uint8'))
    return cv2.countNonZero(mask) == w*h

def check_out_fight_in_team(box=[], template=None):
    cv_team = grabImage(box)
    res = cv2.matchTemplate(cv_team, template, eval('cv2.TM_CCOEFF'))
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val >= 4500000.0

def check_if_in_fight(box=[], template=None):
    cv_fight = grabImage(box)
    res = cv2.matchTemplate(cv_fight, cv_template2, eval('cv2.TM_CCOEFF'))
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val >= 4500000.0