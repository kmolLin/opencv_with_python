# -*- coding: utf-8 -*-

import cv2
from numpy import ndarray


def CannyW(img: ndarray, *arg, dst: ndarray, **kwd):
    dst[:] = cv2.Canny(img, *arg, **kwd)
