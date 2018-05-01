# function of  parser image

def parseImage(self):
    pass
    """
    def InConvertImage(self, frame1):
        h,  w = frame1.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        # this is second method in the conver Image.
        #dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)  method 1
        mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        dst = cv2.remap(frame1,mapx,mapy,cv2.INTER_LINEAR)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        return dst
        
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
        # for testing code 
        #self.testpoint()
        self.checkpoint()
    """
