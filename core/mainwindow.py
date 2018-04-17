# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from collections import deque
from .webcam import Webcam
from .VideoWidget import VideoWidget

from .calibation import Dialog

import numpy as np
import datetime
import cv2
import sys

from .Ui_mainwindow import Ui_MainWindow

greenLower = (100, 43, 46)
greenUpper = (124, 255, 255)
pts = deque(maxlen=64)

#640*480 pixel
"""
mtx  = np.array(([732.50285172, 0.00000000e+00,309.35704871], 
                      [0.00000000e+00,732.30666799, 242.63511951],
                     [0.00000000e+00, 0.00000000e+00, 1.00000000e+00] ))

dist = np.array(([3.78048858e-02, -3.67592030e-01 , -2.47147159e-03  ,-4.17964146e-04,  4.24613110e-01]))
  
"""
#800*600 pixel
mtx  = np.array(([915.87877768, 0.00000000e+00,380.14276358], 
                      [0.00000000e+00,915.88537288, 314.01035384],
                     [0.00000000e+00, 0.00000000e+00, 1.00000000e+00] ))


dist = np.array(([0.02764797, -0.33807616 , 0.00095279  ,-0.0024703,  0.57549135]))
  

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.running = False
        self.binary_toggle = False
        
        self.video_stream = None
        self.timers = list()
        self.VidFrameGUI = self.VidFrame
        self.VidFrame = VideoWidget(self.VidFrame)
        

        self.startButton.clicked.connect(self.start_clicked)
        self.showBinaryButton.clicked.connect(self.binary_clicked)
        self.generate.clicked.connect(self.generatearray)
        
        #self.generteMatrix =0

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
        self.video_stream = Webcam(src=self.cameraNumber.value()).start()
        
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
            
            
    # TODO: add method to calibation
    def __openDlg__(self):
        dlg2 = Dialog()
        dlg2.show()
        if dlg2.exec_(): pass

    def InConvertImage(self, frame1):
        # the convert will convert inner matrix to the frame.
        
        h,  w = frame1.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        # this is second method in the conver Image.
        #dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)  method 1
        
        mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        dst = cv2.remap(frame1,mapx,mapy,cv2.INTER_LINEAR)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        return dst

    def update_frame(self):
        if self.running:
            frame = self.video_stream.read()
            
            if self.binary_toggle:
                #(grabbed, frame) = self.video_stream.read()
                frame = self.InConvertImage(frame)
                
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
        
    def loadimage(self, name='buffer.png'):
        self.generatearray()
        
    
    def generatearray(self):
        
        world = np.mat([[self.gp1x.value(),self.gp1y.value(), 1, 1 ], 
                                  [self.gp2x.value(),self.gp2y.value(), 1, 1 ], 
                                  [self.gp3x.value(),self.gp3y.value(), 1, 1 ], 
                                  [self.gp4x.value(),self.gp4y.value(), 1, 1 ]])
                                  
        pixmat = np.mat([[self.pp1x.value(),self.pp1y.value(), 1, 1 ], 
                                  [self.pp2x.value(),self.pp2y.value(), 1, 1 ], 
                                  [self.pp3x.value(),self.pp3y.value(), 1, 1 ], 
                                  [self.pp4x.value(),self.pp4y.value(), 1, 1 ]])
        
        newmtx = np.array(([915.87877768/Zc, 0.00000000e+00, 0,380.14276358], 
                      [0.00000000e+00,915.88537288/Zc, 0, 314.01035384],
                     [0.00000000e+00, 0.00000000e+00, 1.0/Zc, 0], 
                    [0.00000000e+00, 0.00000000e+00, 0, 1.0] ))
        #np.linalg.inv
        outerMat = np.dot(np.dot(np.linalg.inv(world), np.linalg.inv(newmtx)), pixmat)  
        #X = np.linalg.inv(np.dot( Aplane.transpose(), Aplane))*np.dot( Aplane.transpose(), yplane)
        self.xtranslate = X
        #self.outputGenerte(X)  
        #TODO: not yet to convert to txt to read

        
    def checkpoint(self):
        pixelx, pixely = self.inputpixelX.value(), self.inputpixelY.value()
        endpoint =  [pixelx, pixely, 1]*self.xtranslate
        print(endpoint)
    
    
    def calctrackobject(self, image):
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
            print("{}\t{}".format(center[0],center[1] ))
        

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
        
    
    """TODO build catch image"""
    def catchimage(self):
        im = self.video_stream.read()
        camera_capture = im
        file = "buffer.png"
        cv2.imwrite(file, camera_capture)
        self.loadimage()
        
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
            #print("{}\t{}".format(center[0],center[1] ))
            self.trackX.setText(str(center[0]))
            self.trackY.setText(str(center[1]))
            if radius > 10:
                cv2.circle(frame1, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame1, center, 5, (0, 0, 255), -1)
            
        pts.appendleft(center)
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(64/ float(i + 1)) * 2.5)
            cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)


    def outputGenerte(self, matrix):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "./test.txt", "Text files (*.txt)")
        listdata = matrix.tolist()
        if filename:
            data = []
            data1 = []
            data2 = []
            for e in range(0, 3):
                data.append(str(listdata[0][e]))
                data1.append(str(listdata[1][e]))
                data2.append(str(listdata[2][e]))
            print(data2)
            with open(filename, 'w') as f:
                f.write(str(data+'\n'))
                f.write(str(data1+'\n'))
                f.write(str(data2+'\n'))

        
    @pyqtSlot()
    def on_load_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "Text files (*.txt)")
        if filename:
            with open(filename, 'r') as f:
                read_list = eval(f.read())
            for (x, y), (spinbox_x, spinbox_y) in zip(read_list, (
                (self.gp1x, self.gp1y),
                (self.gp2x, self.gp2y),
                (self.gp3x, self.gp3y),
                (self.gp4x, self.gp4y),
                (self.pp1x, self.pp1y),
                (self.pp2x, self.pp2y),
                (self.pp3x, self.pp3y),
                (self.pp4x, self.pp4y)
            )):
                spinbox_x.setValue(x)
                spinbox_y.setValue(y)
    
    @pyqtSlot()
    def on_output_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "./test.txt", "Text files (*.txt)")
        if filename:
            data = []
            for spinbox_x, spinbox_y in (
                (self.gp1x, self.gp1y),
                (self.gp2x, self.gp2y),
                (self.gp3x, self.gp3y),
                (self.gp4x, self.gp4y),
                (self.pp1x, self.pp1y),
                (self.pp2x, self.pp2y),
                (self.pp3x, self.pp3y),
                (self.pp4x, self.pp4y)
            ):
                data.append((spinbox_x.value(), spinbox_y.value()))
            with open(filename, 'w') as f:
                f.write(str(data))
    
    @pyqtSlot()
    def on_getpixel_clicked(self):
        self.checkpoint()
    
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
        #filename, _ = QFileDialog.getOpenFileUrl(self, "Save File", ".calibation_data/data.jpg", "Text files (*.jpg)")
        #print(filename)
