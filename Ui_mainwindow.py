# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\kmol\opencv_with_python\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(845, 499)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 811, 461))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.startButton = QtWidgets.QPushButton(self.layoutWidget)
        self.startButton.setAutoDefault(False)
        self.startButton.setDefault(False)
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 0, 2, 1, 1)
        self.currTimeLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.currTimeLabel.setFont(font)
        self.currTimeLabel.setObjectName("currTimeLabel")
        self.gridLayout.addWidget(self.currTimeLabel, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(24, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.currDateLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.currDateLabel.setFont(font)
        self.currDateLabel.setObjectName("currDateLabel")
        self.gridLayout.addWidget(self.currDateLabel, 0, 5, 1, 1)
        self.showBinaryButton = QtWidgets.QPushButton(self.layoutWidget)
        self.showBinaryButton.setObjectName("showBinaryButton")
        self.gridLayout.addWidget(self.showBinaryButton, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.VidFrame = QtWidgets.QWidget(self.layoutWidget)
        self.VidFrame.setMinimumSize(QtCore.QSize(640, 360))
        self.VidFrame.setObjectName("VidFrame")
        self.gridLayout_2.addWidget(self.VidFrame, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "opencv_pyqt5"))
        self.startButton.setText(_translate("MainWindow", "Start Video"))
        self.currTimeLabel.setText(_translate("MainWindow", "HH:MM:SS PM"))
        self.currDateLabel.setText(_translate("MainWindow", "DD-MMM-YYYY"))
        self.showBinaryButton.setText(_translate("MainWindow", "tracking"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

