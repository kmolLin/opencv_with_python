import cv2
from threading import Thread

class Webcam:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.staus = False

    def start(self):
        self.staus = True
        self.stream.set(3, 720)# CV_CAP_PROP_FRAME_WIDTH
        self.stream.set(4,1280)#CV_CAP_PROP_FRAME_WIDTH
        t = Thread(target=self.update)
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame
        
    def saveimage(self):
        a= self.frame
        return a

    def stop(self):
        self.stream.release()
        self.staus = False
        self.stopped = True
    def callbackStaus(self):
        return self.staus
