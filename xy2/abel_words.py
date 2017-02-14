#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_log
import cv2
import pytesseract
from PIL import Image
import time, random
import pyautogui

def get_bxxm_task_description(x_offset, y_offset):
    pyautogui.keyDown('alt')
    pyautogui.press('q')
    pyautogui.keyUp('alt')
    time.sleep(0.5)
    im_head = ImageGrab.grab(
        bbox=(
            x_offset + abel_window.bxxm_pos[0],
            y_offset + abel_window.bxxm_pos[1],
            x_offset + abel_window.bxxm_pos[2],
            y_offset + abel_window.bxxm_pos[3]
        )
    )
    pyautogui.keyDown('alt')
    pyautogui.press('q')
    pyautogui.keyUp('alt')
    tmp = '.\\auto\\bxxm_tmp.png'
    tmp_tif = tmp + '.tif'
    im_head.save(tmp)
    im = cv2.imread(tmp, 0)
    im2 = cv2.resize(im, (0,0), fx=3.0, fy=3.0)
    cv2.imwrite(tmp_tif, im2)

    tesseract_cmd = 'tesseract-ocr\\tesseract'
    original = pytesseract.image_to_string(
        Image.open(tmp_tif),
        lang='chi_sim',
        boxes=True,
        cmd=tesseract_cmd
    )
    log_text = None
    log_code = None
    for line in original.split('\n'):
        word = line.split()[0]
        log_code += repr(word)
        log_text += word
        text4= text3.replace('\xe3\x80\x94', '(').\
            replace('\xe3\x80\x95', ')').\
            replace('\xef\xbc\x8c', ',').\
            replace('誓主', '往').\
            replace('窄查', '松').\
            replace('木木', '林').\
            replace('i昊', '误').\
            replace('_卜圣', '怪').\
            replace('_r量', '性').\
            replace('_r生', '性').\
            replace('急、', '急').\
            replace('萝己', '兜').\
            replace('耍己', '兜').\
            replace('茎同', '洞').\
            replace('春肖', '消').\
            replace('塞肖', '消').\
            replace('\xe8\x96\xb9同', '洞').\
            replace('哇', '4').\
            replace('喹', '4').\
            replace('?', '7').\
            replace('\xe8\x8e\x92', '营').\
            replace('茅寺', '持').\
            replace('琶彗', '智慧').\
            replace('于窜', '神').\
            replace('弋盅', '通').\
            replace('弋重', '通').\
            replace('蜃', '魔').\
            replace('葭', '尊').\
            replace('乘幔', '剩').\
            replace('禾少', '秒').\
            replace(';欠', '次').\
            replace('开多', '形').\
            replace('开萎', '形').\
            replace('主奈', '探').\
            replace('干', '天').\
            replace('目冒', '眼').\
            replace('言庾', '波').\
            replace('春皮', '波').\
            replace('曰', '白').\
            replace('胃', '骨').\
            replace('\xe2\x80\xa6蓼', '多').\
            replace('\\副', '闻').\
            replace('士或', '域').\
            replace('口亚', '哑').\
            replace('讳且', '粗').\
            replace('\'J、', '小').\
            replace('\'怪', '怪').\
            replace('霄人', '队').\
            replace('韦贞', '锁').\
            replace('妊', '妖').\
            replace('炊二', '火').\
            replace('f壬', '任')
    abel_log.write_to_log(log_code)
    abel_log.write_to_log(log_text)
    return log_text
