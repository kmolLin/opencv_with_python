# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_calibation import Ui_Dialog
from .calibration.calibration_calc import calibation

class Dialog(QDialog, Ui_Dialog):
    """
    calc the matrix
    """
    def __init__(self, parent=None):
        
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_calibation_clicked(self):
        self.w = self.chessew.value()
        self.l = self.chessel.value()
        self.distance = self.chessboard_dis.value()
        self.locate = self.imagePath.text()
        print(self.locate)
        
        self.call = calibation(self.w, self.l , self.distance)
        ret, mtx, dist, rvecs, tvecs = self.call.calcmatrix(self.locate)
        print(ret, mtx, dist, rvecs, tvecs)
        # TODO: need to calc
        
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_undistort_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_imagePbtn_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Save File", ".calibation_data/data.jpg", QFileDialog.ShowDirsOnly)
        if dir:
            print(dir)
            self.imagePath.insert(dir)
        
