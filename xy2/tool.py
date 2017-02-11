#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window
import pyscreenshot as ImageGrab
import win32gui
import sys

w = abel_window.WindowMgr()
w.find_window_wildcard(".*Revision.*ID.*")
w.set_foreground()
rect                 = win32gui.GetWindowRect(w._handle)
x_offset             = rect[0]
y_offset             = rect[1]
x_head_begin = x_offset +
y_head_begin = y_offset +
x_head_end = x_head_begin +
y_head_end = y_head_begin +
im_head = ImageGrab.grab(
    bbox=(
        x_head_begin,
        y_head_begin,
        x_head_end,
        y_head_end
    )
)
im_head.save(sys.argv[1])
