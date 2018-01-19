# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\opencv_with_python\core\calibation.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(457, 449)
        Dialog.setSizeGripEnabled(True)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.chessew = QtWidgets.QSpinBox(Dialog)
        self.chessew.setObjectName("chessew")
        self.horizontalLayout.addWidget(self.chessew)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.chessel = QtWidgets.QSpinBox(Dialog)
        self.chessel.setObjectName("chessel")
        self.horizontalLayout_2.addWidget(self.chessel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.chessboard_dis = QtWidgets.QDoubleSpinBox(Dialog)
        self.chessboard_dis.setObjectName("chessboard_dis")
        self.horizontalLayout_3.addWidget(self.chessboard_dis)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.imagePbtn = QtWidgets.QPushButton(Dialog)
        self.imagePbtn.setObjectName("imagePbtn")
        self.horizontalLayout_4.addWidget(self.imagePbtn)
        self.imagePath = QtWidgets.QLineEdit(Dialog)
        self.imagePath.setObjectName("imagePath")
        self.horizontalLayout_4.addWidget(self.imagePath)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.calibation = QtWidgets.QPushButton(Dialog)
        self.calibation.setObjectName("calibation")
        self.verticalLayout.addWidget(self.calibation)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.undistort = QtWidgets.QPushButton(Dialog)
        self.undistort.setObjectName("undistort")
        self.horizontalLayout_5.addWidget(self.undistort)
        self.initundistort = QtWidgets.QPushButton(Dialog)
        self.initundistort.setObjectName("initundistort")
        self.horizontalLayout_5.addWidget(self.initundistort)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "chessboard_w"))
        self.label_2.setText(_translate("Dialog", "chessboard_L"))
        self.label_3.setText(_translate("Dialog", "Distance"))
        self.imagePbtn.setText(_translate("Dialog", "Image path"))
        self.calibation.setText(_translate("Dialog", "Calibation"))
        self.undistort.setText(_translate("Dialog", "undistort"))
        self.initundistort.setText(_translate("Dialog", "initundistort"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

