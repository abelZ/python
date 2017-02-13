#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abel_window
import pyscreenshot as ImageGrab
import win32gui
import sys
from multiprocessing import freeze_support
import cv2

if __name__ == '__main__':
    freeze_support()
    w = abel_window.WindowMgr()
    w.find_window_wildcard(".*Revision.*ID.*")
    w.set_foreground()
    rect                 = win32gui.GetWindowRect(w._handle)
    x_offset             = rect[0]
    y_offset             = rect[1]
    x_head_begin = x_offset + 376
    y_head_begin = y_offset + 232
    x_head_end = x_head_begin + 260
    y_head_end = y_head_begin + 54
    im_head = ImageGrab.grab(
        bbox=(
            x_head_begin,
            y_head_begin,
            x_head_end,
            y_head_end
        )
    )
    im_head.save(sys.argv[1]+'.png')
    im = cv2.imread(sys.argv[1]+'.png', 0)
    im2 = cv2.resize(im, (0,0), fx=3.0, fy=3.0)
    cv2.imwrite(sys.argv[1]+'.tif', im2)
