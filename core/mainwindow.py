# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from collections import deque
from .webcam import Webcam
from .VideoWidget import VideoWidget

from .calibation import Dialog

import platform
import numpy as np
import datetime
import cv2
import sys

from .Ui_mainwindow import Ui_MainWindow
from .parseimage import parseImage
from .image_class import CommandStack, ImageProcess
from .imagedlg import CannyDlg, DilateDlg, ErodeDlg, ThresholdDlg, MorphologyDlg

greenLower = (100, 43, 46)
greenUpper = (124, 255, 255)
pts = deque(maxlen=64)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        loadUi("core/mainwindow.ui", self)
        self.show()
        self.running = False
        self.binary_toggle = False

        self.video_stream = None
        self.timers = list()
        self.VidFrameGUI = self.VidFrame
        self.VidFrame = VideoWidget(self.VidFrame)

        parseImage(self)
        self.startButton.clicked.connect(self.start_clicked)
        self.showBinaryButton.clicked.connect(self.binary_clicked)

        self.setup_timers()
        self.startButton.setFocus()
        toolbox = ["threshold", "Canny", "Houghline", "morphologyEx", "crop image", "dilate", "findContours"]
        self.image_box.addItems(toolbox)
        self.listWidget.itemDoubleClicked.connect(self.get_widget)
        self.model = []
        self.lenpos = 0
        self.image = None
        self.processing_img = None

    def update_time(self):
        self.currTimeLabel.setText(datetime.datetime.now().strftime('%I:%M:%S %p'))
        self.currDateLabel.setText(datetime.datetime.now().strftime('%d-%b-%Y'))

    def setup_timers(self):
        timer1 = QTimer(self)
        timer1.timeout.connect(self.update_time)
        timer1.start(250)

        timer2 = QTimer(self)
        timer2.timeout.connect(self.update_frame)
        timer2.start(1000.0 / 30)

        self.timers.append(timer1)
        self.timers.append(timer2)

    def start_clicked(self):
        """ Use the class inherit the opencv named Webcam() and init it to open camera
        """
        self.video_stream = Webcam(src=self.cameraNumber.value()).start()
        self.running = not self.running
        if self.running:
            self.startButton.setText('Stop Video')
            self.VidFrame.show()
        else:
            self.startButton.setText('Start Video')
            self.VidFrame.hide()

    def binary_clicked(self):
        """ clicked and start for tradding object
        """
        self.binary_toggle = not self.binary_toggle
        if self.binary_toggle:
            self.showBinaryButton.setText('Show Color')
        if not self.binary_toggle:
            self.showBinaryButton.setText('Show Binary')

    def __openDlg__(self):
        dlg2 = Dialog()
        dlg2.show()
        if dlg2.exec_(): pass

    @pyqtSlot()
    def on_load_image_btn_clicked(self):
        # choose a image from dlg
        self.VidFrame.show()
        file_url, _ = QFileDialog.getOpenFileName(self, 'choose image', ".", "*.png *.jpg")
        if not file_url:
            return

        self.image = cv2.imread(file_url, 0)
        self.processing_img = self.image.copy()
        frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        frame = self.resizeimage(frame, 1)
        frame_height, frame_width, _ = frame.shape
        frame = QImage(frame.data,
                       frame_width,
                       frame_height,
                       frame.strides[0],
                       QImage.Format_RGB888)

        self.VidFrame.setImage(frame)

    @pyqtSlot()
    def on_add_list_view_clicked(self):
        name = self.image_box.currentText()
        self.listWidget.addItem(QListWidgetItem(name))
        self.lenpos = self.lenpos + 1

        self.model.append(ImageProcess(name, (), {}))

    @pyqtSlot()
    def on_apply_select_clicked(self):
        print(self.lenpos)
        commandstack = CommandStack()
        commandstack.insertlist(self.model)
        print(commandstack.script())

    @pyqtSlot()
    def on_delete_list_view_clicked(self):
        if self.listWidget.currentRow() != -1:
            index = self.listWidget.currentRow()
            self.listWidget.takeItem(index)
            del self.model[index]
        else:
            self.listWidget.takeItem(self.listWidget.count() - 1)
            del self.model[self.listWidget.count() - 1]
        self.lenpos = self.lenpos - 1

    # TODO: this two function for move up or down the model list  4/14
    @pyqtSlot()
    def on_move_up_btn_clicked(self):
        index = self.listWidget.currentRow()
        self.listWidget.insertItem(index - 1, self.listWidget.takeItem(index))
        self.listWidget.setCurrentRow(index - 1)
        self.model[index], self.model[index - 1] = self.model[index - 1], self.model[index]

    @ pyqtSlot()
    def on_move_down_btn_clicked(self):
        index = self.listWidget.currentRow()
        self.listWidget.insertItem(index + 1, self.listWidget.takeItem(index))
        self.listWidget.setCurrentRow(index + 1)

    def get_widget(self, qitem):
        # TODO: if user not double click dlg, the value is None need to add default value in function
        index = self.listWidget.row(qitem)
        # print(index)
        if not self.model[index].args:
            init_tuple, init_dict = (), {}
        else:
            init_tuple, init_dict = self.model[index].args, self.model[index].kwd

        if qitem.text() == 'threshold':
            dlg = ThresholdDlg(self, init_tuple, init_dict)
            dlg.exec_()
            # cv2.imwrite('test.jpg', dlg.finish_image)
        elif qitem.text() == 'Canny':
            dlg = CannyDlg(self, init_tuple, init_dict)
            dlg.exec_()
        elif qitem.text() == 'morphologyEx':
            dlg = MorphologyDlg(self, init_tuple, init_dict)
            dlg.exec_()
        elif qitem.text() == 'dilate':
            dlg = DilateDlg(self, init_tuple, init_dict)
            dlg.exec_()
        elif qitem.text() == 'erode':
            dlg = ErodeDlg(self, init_tuple, init_dict)
            dlg.exec_()
        else:
            pass
        self.processing_img = dlg.finish_image
        self.model[index] = dlg.command

    def resizeimage(self, image, scale):
        frame_height, frame_width, _ = image.shape
        reimage = cv2.resize(image, (int(frame_width / scale), int(frame_height / scale)))
        return reimage

    def update_frame(self):
        if self.running:
            frame = self.video_stream.read()

            if self.binary_toggle:
                # (grabbed, frame) = self.video_stream.read()
                frame = frame

                self.trackObject(frame)

                # frame = self.clean_img(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.resizeimage(frame, 2)
            frame_height, frame_width, _ = frame.shape
            frame = QImage(frame.data,
                           frame_width,
                           frame_height,
                           frame.strides[0],
                           QImage.Format_RGB888)
            self.VidFrame.setImage(frame)

    def clean_img(self, img):
        height, width, channels = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 127, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        kernel = np.ones((5, 5), np.uint8)
        clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        clean = cv2.merge((clean, clean, clean))
        return clean

    def calctrackobject(self, image):
        """tracking max rect object
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print("{}\t{}".format(center[0], center[1]))

    def clear_timers(self):
        while self.timers:
            timer = self.timers.pop()
            timer.stop()

    def closeEvent(self, event):
        self.running = False
        self.clear_timers()
        if self.video_stream != None:
            self.video_stream.stop()
        self.close()
        sys.exit()

    def catchimage(self):
        """ Save capcture image
        """
        im = self.video_stream.read()
        camera_capture = im
        file = "buffer.png"
        cv2.imwrite(file, camera_capture)
        self.loadimage()

    def trackObject(self, frame1):
        """ tracking object function
        """
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]

        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # print("{}\t{}".format(center[0],center[1] ))
            # self.trackX.setText(str(center[0]))
            # self.trackY.setText(str(center[1]))
            if radius > 10:
                cv2.circle(frame1, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
            cv2.circle(frame1, center, 5, (0, 0, 255), -1)

        pts.appendleft(center)
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
            cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)

    @pyqtSlot()
    def on_saveImage_clicked(self):
        """
        dir = QFileDialog.getExistingDirectory(self, "Save File", ".calibation_data/data.jpg", QFileDialog.ShowDirsOnly)
        print(dir)
        """
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", ".calibation_data/data.jpg", "Text files (*.jpg)")
        if filename:
            camera_capture = self.video_stream.saveimage()
            cv2.imwrite(filename, camera_capture)

    @pyqtSlot()
    def on_actioncalibation_triggered(self):
        self.__openDlg__()
