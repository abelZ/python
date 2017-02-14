#!/usr/bin/env python
# -*- coding: utf-8 -*-

def write_to_log(log_text):
    f = open('.\\log.txt', 'a')
    f.write(log_text)
    f.write('\n')
    f.close()
