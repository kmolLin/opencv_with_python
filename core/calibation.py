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
        
        self.calb = calibation(self.w, self.l , self.distance)
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = self.calb.calcmatrix(self.locate)
        print(self.ret, self.mtx, self.dist)
        # TODO: need to calc
        
    @pyqtSlot()
    def on_undistort_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Save File", ".calibation_data/data.jpg", "Text files (*.jpg)")
        if filename:
            self.calb.Opencv_undistort(filename, self.mtx, self.dist)
    
    @pyqtSlot()
    def on_initundistort_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Save File", ".calibation_data/data.jpg", "Text files (*.jpg)")
        if filename:
            self.calb.Opencv_initdis(filename, self.mtx, self.dist)
    
    @pyqtSlot()
    def on_imagePbtn_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Save File", ".calibation_data/data.jpg", QFileDialog.ShowDirsOnly)
        if dir:
            self.imagePath.insert(dir)
    
    @pyqtSlot()
    def on_exportmatrix_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "./test.txt", "Text files (*.txt)")
        if filename:
            data = []
            data.append(self.mtx)
            data.append(self.dist)
            with open(filename, 'w') as f:
                f.write(str(data))
