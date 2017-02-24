#!/usr/bin/env python
# -*- coding: utf-8 -*-

def printGbk(text):
    print text.decode('utf-8').encode('gbk')

def write_to_log(log_text, to_screen = False):
    if to_screen:
        printGbk(log_text)
    f = open('.\\auto\\log.txt', 'a')
    f.write(log_text)
    f.write('\n')
    f.close()
