import sys
import cv2
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QScrollArea, QDesktopWidget, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QPalette
 
 
class Example(QMainWindow):
    
    def __init__(self, parent = None):
        # 繼承的 parent 初始化 fucntion
        super().__init__(parent)
        
        self.initUI()
        
        
    def initUI(self):    
        # 建立 QLabel 元件
        imgLabel = QLabel()
        
        # openCV 讀檔
        cvImage = cv2.imread("test.jpg")
        # 得到 大小 與 幾個 byte 組成一個顏色
        height, width, byteValue = cvImage.shape
        # 得到寬有多少 byte
        byteValue = byteValue * width
        
        # openCV 預設顏色排列為 BGR 故需再轉換為 RGB
        temp = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        # 設定 imgLabel 圖片
        # 因 setPixmap 輸入需為 QPixmap，所以還得多做一層轉換
        imgLabel.setPixmap(QPixmap().fromImage(QImage(temp, width, height, byteValue, QImage.Format_RGB888)))        
        
        # 建立 QScrollArea for 滾動圖片
        scrollArea = QScrollArea()
        # 設定背景顏色
        scrollArea.setBackgroundRole(QPalette.Dark)
        # 將 imgLabel 設定為 child
        scrollArea.setWidget(imgLabel)
        
        # 設定主要 widget
        self.setCentralWidget(scrollArea)         
        # 設定尺寸
        self.resize(500, 500)
        # 視窗置中
        self.center()        
        # 設定標題
        self.setWindowTitle('Simple')
        # 顯示，因圖形元件被創造時都是 hidden 狀態
        self.show()
    
    def center(self):    
        # 得到 frameGeometry 的 QRect
        qr = self.frameGeometry()
        
        # QDesktopWidget 可得到和桌面相關的資訊
        # 得到桌面可用的 geometry 的中心點 
        cp = QDesktopWidget().availableGeometry().center()
        
        # 將 qr 的中心點移至此中心點
        qr.moveCenter(cp)
        
        # 將視窗的左上角移至 qr 的左上角座標
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    # Qt GUI 需要唯一一個 QApplication 負責管理，可傳入 sys.argv 參數
    app = QApplication(sys.argv)
    # 建立 Exxample instance
    ex = Example()
    # app.exec_() 讓 QApplication 進入 event loop
    # exec 是 Python keyword，所以會多出底線
    sys.exit(app.exec_())   
