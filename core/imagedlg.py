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


def resizeimage(image, scale):
    """Resize of the image, scale is use to Zoom out scale """
    frame_height, frame_width, _ = image.shape
    reimage = cv2.resize(image, (int(frame_width / scale), int(frame_height / scale)))
    return reimage


def image2Frame(image):
    """Convert image to qt frame formate (QImage) """
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    frame = resizeimage(frame, 1)
    frame_height, frame_width, _ = frame.shape
    frame = QImage(frame.data,
                   frame_width,
                   frame_height,
                   frame.strides[0],
                   QImage.Format_RGB888)
    return frame


class CannyDlg(QDialog):

    def __init__(self, parent, init_tuple, init_dict):
        super(CannyDlg, self).__init__()
        loadUi("core/cannydlg.ui", self)
        self.maxvalue = None
        self.minvalue = None
        self.aperture_size = None
        self.buttonBox.accepted.connect(self.get_value)
        self.max_bar_slide.valueChanged.connect(self.update_image)
        self.min_bar_slide.valueChanged.connect(self.update_image)
        self.command = None
        self.image = parent.processing_img
        self.VidFrame = parent.VidFrame
        self.finish_image = None

        if not init_tuple:
            pass
        else:
            self.min_value_spin.setValue(init_tuple[0])
            self.max_value_spin.setValue(init_tuple[1])
            self.aperturesize_spin.setValue(init_tuple[2])

    def get_value(self):
        self.command = ImageProcess('CannyW',
                                  (self.min_value_spin.value(),
                                   self.max_value_spin.value(),
                                   self.aperturesize_spin.value()), {})

    def update_image(self):
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        change_img = cv2.Canny(self.image,
                               self.min_value_spin.value(),
                               self.max_value_spin.value(),
                               apertureSize=self.aperturesize_spin.value())
        # print(self.image)
        self.VidFrame.setImage(image2Frame(change_img))
        self.finish_image = change_img


class ThresholdDlg(QDialog):

    def __init__(self, parent, init_tuple, init_dict):
        super(ThresholdDlg, self).__init__()
        loadUi("core/thresholddlg.ui", self)

        if not init_tuple:
            pass
        else:
            self.min_value_spin.setValue(init_tuple[0])
            self.max_value_spin.setValue(init_tuple[1])
        self.maxvalue = None
        self.minvalue = None
        self.buttonBox.accepted.connect(self.get_value)
        self.max_bar_slide.valueChanged.connect(self.update_image)
        self.min_bar_slide.valueChanged.connect(self.update_image)
        self.command = None
        self.image = parent.processing_img
        self.VidFrame = parent.VidFrame
        self.finish_image = None

    def get_value(self):
        self.command = ImageProcess('threshold',
                                    (self.min_value_spin.value(),
                                     self.max_value_spin.value(),
                                     getattr(cv2, self.threshold_combo.currentText())), {})

    def update_image(self):
        _, change_img = cv2.threshold(self.image,
                                      self.min_value_spin.value(),
                                      self.max_value_spin.value(),
                                      getattr(cv2, self.threshold_combo.currentText()))
        # print(self.image)
        self.VidFrame.setImage(image2Frame(change_img))
        self.finish_image = change_img


class MorphologyDlg(QDialog):
    # TODO : morphology want to build the kernel in this class

    def __init__(self, parent, init_tuple, init_dict):
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

    def __init__(self, parent, init_tuple, init_dict):
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

    def __init__(self, parent, init_tuple, init_dict):
        super(ErodeDlg, self).__init__()
        loadUi("core/dilatedlg.ui", self)
        self.buttonBox.accepted.connect(self.get_value)
        self.command = None

    def get_value(self):
        size = self.kernel_size_spin.value()
        kernel = cv2.getStructuringElement(getattr(cv2, self.kernel_combo.currentText())
                                           , (size, size))
        self.command = ImageProcess('erode', (kernel,), {'iterations': self.iteration_spin.value()})

