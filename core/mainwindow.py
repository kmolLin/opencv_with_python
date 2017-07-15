# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from collections import deque
from .webcam import Webcam
from .VideoWidget import VideoWidget

import numpy as np
import datetime
import cv2
import sys

from .ui.Ui_mainwindow import Ui_MainWindow

greenLower = (100, 43, 46)
greenUpper = (124, 255, 255)
pts = deque(maxlen=64)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.running = False
        self.binary_toggle = False
        self.video_stream = Webcam(src=0).start()

        self.timers = list()
        self.VidFrameGUI = self.VidFrame
        self.VidFrame = VideoWidget(self.VidFrame)

        self.startButton.clicked.connect(self.start_clicked)
        self.showBinaryButton.clicked.connect(self.binary_clicked)

        self.setup_timers()
        self.startButton.setFocus()
        
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
        self.running = not self.running
        if self.running:
            self.startButton.setText('Stop Video')
            self.VidFrame.show()
        else:
            self.startButton.setText('Start Video')
            self.VidFrame.hide()

    def binary_clicked(self):
        self.binary_toggle = not self.binary_toggle
        if self.binary_toggle:
            self.showBinaryButton.setText('Show Color')
        if not self.binary_toggle:
            self.showBinaryButton.setText('Show Binary')

    def update_frame(self):
        if self.running:
            frame = self.video_stream.read()
            if self.binary_toggle:
                #(grabbed, frame) = self.video_stream.read()
                self.trackObject(frame)

                #frame = self.clean_img(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

    def clear_timers(self):
        while self.timers:
            timer = self.timers.pop()
            timer.stop()

    def closeEvent(self, event):
        self.running = False
        self.clear_timers()
        self.video_stream.stop()
        self.close()
        sys.exit()
        
    def trackObject(self, frame1):
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
            print("{}\t{}".format(center[0],center[1] ))
            if radius > 10:
                cv2.circle(frame1, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame1, center, 5, (0, 0, 255), -1)
            
        pts.appendleft(center)
        #print(pts)
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(64/ float(i + 1)) * 2.5)
            cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)


'''
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
'''
