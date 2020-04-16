__author__ = "Yu-Sheng Lin"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyquino@gmail.com"

import sys
import cv2

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *

from core.image_class import CommandStack, ImageProcess


class CannyDlg(QDialog):

    def __init__(self):
        super(CannyDlg, self).__init__()
        loadUi("core/cannydlg.ui", self)
        self.maxvalue = None
        self.minvalue = None
        self.aperture_size = None
        self.buttonBox.accepted.connect(self.get_value)
        self.command = None

    def get_value(self):
        self.command = ImageProcess('CannyW',
                                  (self.min_value_spin.value(),
                                   self.max_value_spin.value(),
                                   self.aperturesize_spin.value()), {})


class ThresholdDlg(QDialog):

    def __init__(self):
        super(ThresholdDlg, self).__init__()
        loadUi("core/thresholddlg.ui", self)
        self.maxvalue = None
        self.minvalue = None
        self.buttonBox.accepted.connect(self.get_value)
        self.command = None

    def get_value(self):
        self.command = ImageProcess('threshold',
                                  (self.min_value_spin.value(),
                                   self.max_value_spin.value(),
                                   getattr(cv2, self.threshold_combo.currentText())), {})


class MorphologyDlg(QDialog):
    # TODO : morphology want to build the kernel in this class

    def __init__(self):
        super(MorphologyDlg, self).__init__()
        loadUi("core/morphologydlg.ui", self)
        self.buttonBox.accepted.connect(self.get_value)
        self.command = None
        self.MORPH_kernel = None
        self.kernel_size = None

    def get_value(self):
        size = self.kernel_size_spin.value()
        kernel = cv2.getStructuringElement(getattr(cv2, self.kernel_combo.currentText())
                                           , (size, size))
        method = getattr(cv2, self.morphset_combo.currentText())
        self.command = ImageProcess('morphologyEx', (method, kernel), {'iterations': self.iteration_spin.value()})


class DilateDlg(QDialog):

    def __init__(self):
        super(DilateDlg, self).__init__()
        loadUi("core/dilatedlg.ui", self)
        self.buttonBox.accepted.connect(self.get_value)
        self.command = None

    def get_value(self):
        size = self.kernel_size_spin.value()
        kernel = cv2.getStructuringElement(getattr(cv2, self.kernel_combo.currentText())
                                           , (size, size))
        self.command = ImageProcess('dilate', (kernel,), {'iterations': self.iteration_spin.value()})


class ErodeDlg(QDialog):

    def __init__(self):
        super(ErodeDlg, self).__init__()
        loadUi("core/dilatedlg.ui", self)
        self.buttonBox.accepted.connect(self.get_value)
        self.command = None

    def get_value(self):
        size = self.kernel_size_spin.value()
        kernel = cv2.getStructuringElement(getattr(cv2, self.kernel_combo.currentText())
                                           , (size, size))
        self.command = ImageProcess('erode', (kernel,), {'iterations': self.iteration_spin.value()})

