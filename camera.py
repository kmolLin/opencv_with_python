from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
import cv2
import numpy as np
from collections import deque
import argparse
import imutils
import threading

blueLower = (100, 43, 46)
blueUpper = (124, 255, 255)

ap = argparse.ArgumentParser()
args = vars(ap.parse_args())


class CameraDevice(QObject):

    frame_ready = pyqtSignal(QImage)

    def __init__(self, device_id=0):
        super().__init__()
        self.capture = cv2.VideoCapture(device_id)
        print(type(self.capture))
        self.timer = QTimer()

        if not self.capture.isOpened():
            raise ValueError("Device not found")

        self.timer.timeout.connect(self.read_frame)
        self.timer.setInterval(1000 / (self.fps or 30))
        self.timer.start()

    def __del__(self):
        self.timer.stop()
        self.capture.release()

    @property
    def fps(self):
        """Frames per second."""
        return int(self.capture.get(cv2.CAP_PROP_FPS))

    @property
    def size(self):
        """Returns the size of the video frames: (width, height)."""
        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)

    def read_frame(self):
        """Read frame into QImage and emit it."""
        success, frame = self.capture.read()
        if success:
            img = _convert_array_to_qimage(frame)
            self.frame_ready.emit(img)
        else:
            raise ValueError("Failed to read frame")
            
    def start(self):
        threading.Thread(target = self.trackingBlueObject, args = ())
        
    def stop(self):
        threading.Thread(target = self.stoptracking, args = ())
        
    def stoptracking(self):
        print('stop')
    
    def trackingBlueObject(self):
        grabbed, frame= self.capture.read()
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, blueLower, blueUpper)
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
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            '''    
            pts.appendleft(center)
            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                    
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            '''


def _convert_array_to_qimage(a):
    height, width, channels = a.shape
    bytes_per_line = channels * width
    cv2.cvtColor(a, cv2.COLOR_BGR2RGB, a)
    return QImage(a.data, width, height, bytes_per_line, QImage.Format_RGB888)
