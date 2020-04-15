__author__ = "Yu-Sheng Lin"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyquino@gmail.com"

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *


class CannyDlg(QDialog):

    def __init__(self):
        super(CannyDlg, self).__init__()
        loadUi("core/cannydlg.ui", self)
        self.maxvalue = None
        self.minvalue = None
        self.aperture_size = None
        self.buttonBox.accepted.connect(self.get_value)

    def get_value(self):
        self.maxvalue = self.max_value_spin.value()
        self.minvalue = self.min_value_spin.value()
        self.aperture_size = self.aperturesize_spin.value()


class ThresholdDlg(QDialog):

    def __init__(self):
        super(ThresholdDlg, self).__init__()
        loadUi("core/thresholddlg.ui", self)
        self.maxvalue = None
        self.minvalue = None
        self.comboText = None
        self.buttonBox.accepted.connect(self.get_value)

    def get_value(self):
        self.maxvalue = self.max_value_spin.value()
        self.minvalue = self.min_value_spin.value()
        self.comboText = self.threshold_combo.currentText()


class MorphologyDlg(QDialog):
    # TODO : morphology want to build the kernel in this class

    def __init__(self):
        super(MorphologyDlg, self).__init__()
        loadUi("core/morphologydlg.ui", self)

    def test(self):
        pass


class DilateDlg(QDialog):

    def __init__(self):
        super(DilateDlg, self).__init__()
        loadUi("core/dilatedlg.ui", self)

    def test(self):
        pass


class ErodeDlg(QDialog):

    def __init__(self):
        super(ErodeDlg, self).__init__()
        loadUi("core/dilatedlg.ui", self)

    def test(self):
        pass

