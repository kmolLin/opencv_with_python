# -*- coding: utf-8 -*-

from typing import List
from numpy import ndarray, ones, uint8
import cv2
from core.cvwrapper import CannyW


class ImageProcess:

    def __init__(self, name: str, args: tuple, kwds: dict):
        # name = method name
        # args according method name
        # kwds according method name
        self.name = name
        self.args = args
        self.kwd = kwds

    def __repr__(self):
        return f"name: {self.name}, parameter: {self.args}, keyword: {self.kwd}"


class CommandStack:

    def __init__(self):
        self.stack: List[ImageProcess] = []

    def append(self, name: str, args: tuple, kwds: dict):
        self.stack.append(ImageProcess(name, args, kwds))

    def insertlist(self, tmp: list):
        for i in tmp:
            self.stack.append(i)

    def apply(self, img: ndarray) -> ndarray:
        # TODO: process for finish image
        img = img.copy()
        for cmd in self.stack:
            if hasattr(cv2, cmd.name):
                fn = getattr(cv2, cmd.name)
            else:
                fn = eval(cmd.name, globals())
            fn(img, dst=img, *cmd.args, **cmd.kwd)
        return img

    def script(self) -> str:
        doc = "from core.cvwrapper import *\n" \
              "from numpy import *\n\n"
        for cmd in self.stack:
            doc += f"{cmd.name}(img, dst=img, *{cmd.args}, **{cmd.kwd})\n"
        return doc


if __name__ == '__main__':

    kernel = ones((5, 5), uint8)
    stack = CommandStack()
    stack.append('threshold', (127, 255, cv2.THRESH_BINARY), {})
    stack.append('erode', (kernel,), {'iterations': 1})
    stack.append('CannyW', (100, 150), {})
    img = cv2.imread("123.jpg", 0)
    img = stack.apply(img)
    print(stack.script())

