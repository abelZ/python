#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window, abel_log
import cv2
import os, time, random, subprocess
import pyautogui

def run_tesseract(input_filename, output_filename_base, lang=None, boxes=False, config=None):
    cmd = 'tesseract-ocr\\tesseract'
    command = [cmd, input_filename, output_filename_base]

    if lang is not None:
        command += ['-l', lang]

    if boxes:
        command += ['batch.nochop', 'makebox']

    if config:
        command += shlex.split(config)

    proc = subprocess.Popen(command,
            stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())

def image_to_string(input_file_name, lang=None, boxes=False, config=None):
    output_file_name_base = input_file_name
    if not boxes:
        output_file_name = '%s.txt' % output_file_name_base
    else:
        output_file_name = '%s.box' % output_file_name_base
    try:
        status, error_string = run_tesseract(
            input_file_name,
            output_file_name_base,
            lang=lang,
            boxes=boxes,
            config=config,
        )
        if status:
            return ''
        f = open(output_file_name)
        try:
            return f.read().rstrip()
        finally:
            f.close()
    finally:
        os.remove(output_file_name)

def get_bxxm_task_description():
    tmp_tif = '.\\auto\\bxxm_tmp.bmp'
    pyautogui.keyDown('alt')
    pyautogui.press('q')
    pyautogui.keyUp('alt')
    time.sleep(0.5)
    im,w,h = abel_window.xy2_win.grabImage(abel_window.bxxm_task_pos)
    pyautogui.keyDown('alt')
    pyautogui.press('q')
    pyautogui.keyUp('alt')
    im2 = cv2.resize(im, (0,0), fx=3.0, fy=3.0)
    cv2.imwrite(tmp_tif, im2)
    original = image_to_string(tmp_tif, lang='chi_sim', boxes=True)
    log_code = ''
    mid_text = ''
    for line in original.split('\n'):
        word = line.split()[0]
        log_code += repr(word)
        log_code += word
        mid_text += word
    # abel_log.write_to_log(log_code)
    os.remove(tmp_tif)
    return mid_text.\
            replace('\xe3\x80\x94', '(').\
            replace('\xe3\x80\x95', ')').\
            replace('\xef\xbc\x8c', ',').\
            replace('\xe2\x80\xb2', ',').\
            replace('誓主', '往').\
            replace('千主', '往').\
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
            replace('T', '7').\
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

def get_coordinate_text(f=None):
    tmp_tif = f
    if f is None:
        tmp_tif = '.\\auto\\cord_tmp.bmp'
    im,w,h = abel_window.xy2_win.grabImage(abel_window.coordinate_pos)
    im2 = cv2.resize(im, (0,0), fx=3.0, fy=3.0)
    cv2.imwrite(tmp_tif, im2)
    original = image_to_string(tmp_tif, lang='chi_sim', boxes=True)
    log_code = ''
    mid_text = ''
    for line in original.split('\n'):
        word = line.split()[0]
        log_code += repr(word)
        log_code += word
        mid_text += word
    if f is None:
        os.remove(tmp_tif)
    return mid_text.\
            replace('\xe3\x80\x94', '(').\
            replace('\xe3\x80\x95', ')').\
            replace('\xef\xbc\x8c', ',').\
            replace('\xe2\x80\xb2', ',').\
            replace('\xe3\x80\x8d', ',').\
            replace('【', '(').\
            replace('】', ')').\
            replace('[', '(').\
            replace(']', ')').\
            replace('哇', '4').\
            replace('喹', '4').\
            replace('碟', '4').\
            replace('?', '7').\
            replace('T', '7').\
            replace('了', '7').\
            replace('g', '9').\
            replace('D', '0').\
            replace('B', '6').\
            replace('S', '5').\
            replace('s', '5').\
            replace('!', '7').\
            replace('U', '0').\
            replace('O', '0').\
            replace('o', '0').\
            replace('I', '1').\
            replace('l', '1').\
            replace('\xe5\x99\xbb', '4').\
            replace('\xe9\xad\x8f', '4').\
            replace('\xe8\x9d\xb6', '4').\
            replace('\xe3\x80\x91', '1').\
            replace('曰', '白').\
            replace('臼', '白').\
            replace('胃', '骨').\
            replace('音', '骨').\
            replace('晋', '骨')

