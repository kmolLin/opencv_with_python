from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from PIL import Image
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

ap = argparse.ArgumentParser()
#原輸入的基準物寬，單位為inch
ap.add_argument("-w", "--width", type=float, required=True)
args = vars(ap.parse_args())
"""
imgC = Image.open("second.jpg")
cut = imgC.crop((400, 350, 700, 800))
cut.save("AA.png")
"""
#讀取圖檔→灰階→模糊
#cv2.GaussianBlur模糊程度可以用3x3, 5x5, 7x7
img = cv2.imread("second.jpg", 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# 輪廓描邊→補空&侵蝕 (用於size)
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cntsS = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cntsS = cntsS[0] if imutils.is_cv2() else cntsS[1]
 
# 'pixels Per Metric' = object_width / know_width (相機像素 / 已知物品的寬度)
(cntsS, _) = contours.sort_contours(cntsS)

 
pixelsPerMetric = None
 
for (a, d) in enumerate(cntsS):
 
    # 計算輪廓旋轉邊界
    Sbox = cv2.minAreaRect(d)
    Sbox = cv2.cv.BoxPoints(Sbox) if imutils.is_cv2() else cv2.boxPoints(Sbox)
    Sbox = np.array(Sbox, dtype="int")
 
    # 繪製輪廓旋轉邊界
    Sbox = perspective.order_points(Sbox)
    cv2.drawContours(img, [Sbox.astype("int")], -1, (0, 255, 0), 1)
 
    for (x, y) in Sbox:
        cv2.circle(img, (int(x), int(y)), 3, (0, 0, 230), -1)
 
    # 計算物品上下邊界之中點
    (Stl, Str, Sbr, Sbl) = Sbox
    (StltrX, StltrY) = midpoint(Stl, Str)
    (SblbrX, SblbrY) = midpoint(Sbl, Sbr)
 
    # 計算物品左右邊界之中點
    (StlblX, StlblY) = midpoint(Stl, Sbl)
    (StrbrX, StrbrY) = midpoint(Str, Sbr)
 
 
    # 利用歐式定理算中點之間的距離
    dA = dist.euclidean((StltrX, StltrY), (SblbrX, SblbrY))
    dB = dist.euclidean((StlblX, StlblY), (StrbrX, StrbrY))
 
    # 如果未知 'pixelsPerMetric', 則使用下一行之算式
    if pixelsPerMetric is None:
        pixelsPerMetric = dB / (args["width"] * 2.54)
 
    # 計算物品之最大長寬
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric
    print ("[{}]".format(a + 1),"width" , round(dimA , 2) , "length" , round(dimB , 2))
 
    # 顯示出畫面中物品的大小
    cv2.putText(img, "{:.1f}cm".format(dimA),
        (int(StrbrX + 10), int(StrbrY)), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 1)
    cv2.putText(img, "{:.1f}cm".format(dimB),
        (int(StltrX - 15), int(StltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 1)

 
