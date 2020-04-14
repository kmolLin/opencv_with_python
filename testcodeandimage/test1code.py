# 辨識物體將其標號，並標註長寬及抓取重心，以便算出各點到點之距離
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from PIL import Image
import numpy as np
import argparse
import imutils
import cv2


# 用於距離測量
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# 此定義用於物體標號時
def order_points_old(pts):
    # 設定物體輪廓之四個點位置,左上右上右下左下(順時針)
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


ap = argparse.ArgumentParser()
# 原輸入的基準物寬，單位為inch
ap.add_argument("-w", "--width", type=float, required=True)
args = vars(ap.parse_args())

###剪裁圖片→只留基準物 (用於重心距離量測)###

imgC = Image.open("first.png")
cut = imgC.crop((0, 0, 200, 200))
cut.save("AA.png")

# 讀取圖檔→灰階→模糊
# cv2.GaussianBlur模糊程度可以用3x3, 5x5, 7x7
imgC = cv2.imread("AA.png", 1)
grayC = cv2.cvtColor(imgC, cv2.COLOR_BGR2GRAY)
blurredC = cv2.GaussianBlur(grayC, (5, 5), 0)
threshC = cv2.threshold(blurredC, 60, 255, cv2.THRESH_BINARY)[1]

cntsC = cv2.findContours(threshC.copy(), cv2.RETR_EXTERNAL,
                         cv2.CHAIN_APPROX_SIMPLE)

cntsC = cntsC[0] if imutils.is_cv2() else cntsC[1]
(cntsC, _) = contours.sort_contours(cntsC)

for b in cntsC:
    # 辨識基準物重心
    M = cv2.moments(b)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

###處理未裁剪的圖片(原始圖)###

# 讀取圖檔→灰階→模糊
# cv2.GaussianBlur模糊程度可以用3x3, 5x5, 7x7
img = cv2.imread("first.png", 1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# 輪廓描邊→補空&侵蝕 (用於size)
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# 進行輪廓偵測  (用於重心測量&標號)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
(cnts, _) = contours.sort_contours(cnts)

# 進行輪廓偵測  (用於最大長寬測量)
cntsS = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                         cv2.CHAIN_APPROX_SIMPLE)
cntsS = cntsS[0] if imutils.is_cv2() else cntsS[1]

# 'pixels Per Metric' = object_width / know_width (相機像素 / 已知物品的寬度)
(cntsS, _) = contours.sort_contours(cntsS)

###物體標號###

for (i, n) in enumerate(cnts):

    if cv2.contourArea(n) < 100:
        continue

    box = cv2.minAreaRect(n)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    rect = order_points_old(box)

    cv2.putText(img, "[{}]".format(i + 1),
                (int(rect[0][0] - 10), int(rect[0][1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 100, 200), 1)

###最大長寬###

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
    print("[{}]".format(a + 1), "width", round(dimA, 2), "length", round(dimB, 2))

    # 顯示出畫面中物品的大小
    cv2.putText(img, "{:.1f}cm".format(dimA),
                (int(StrbrX + 10), int(StrbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1)
    cv2.putText(img, "{:.1f}cm".format(dimB),
                (int(StltrX - 15), int(StltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1)

###重心距離###

refObj = None

for c in cnts:

    cv2.drawContours(img, [c], -1, (220, 255, 250), 1)
    cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(img, "datum", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 220), 1)

    # 計算輪廓旋轉邊界
    gear7 = cv2.minAreaRect(c)
    gear7 = cv2.cv.BoxPoints(gear7) if imutils.is_cv2() else cv2.boxPoints(gear7)
    gear7 = np.array(gear7, dtype="int")

    # 計算輪廓旋轉邊界
    gear7C = cv2.minAreaRect(c)
    gear7C = cv2.cv.BoxPoints(gear7C) if imutils.is_cv2() else cv2.boxPoints(gear7C)
    gear7C = np.array(gear7C, dtype="int")

    gear7 = perspective.order_points(gear7)
    gear7C = perspective.order_points(gear7C)

    # 計算物體重心
    M = cv2.moments(c)
    PcX = int(M["m10"] / M["m00"])
    PcY = int(M["m01"] / M["m00"])
    print(PcX, PcY)

    # 以左邊邊界輪廓當基準, 當參考對象
    if refObj is None:
        # 計算基準物的中點(矩形中點=重心)
        (tl, tr, br, bl) = gear7C
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # 用座標法計算兩物體中心距離 (D為圖中物體座標距離)
        # 乘2.54換算單位inch→mm
        D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        refObj = (gear7C, (cX, cY), D / (args["width"] * 2.54))
        continue

    orig = img.copy()

    # 基準物&測量物的中心點及點到點的距離
    cv2.circle(orig, (int(PcX), int(PcY)), 5, (240, 250, 150), -1)
    cv2.circle(orig, (int(cX), int(cY)), 5, (240, 250, 150), -1)
    cv2.line(orig, (int(PcX), int(PcY)), (int(cX), int(cY)), (240, 250, 150), 2)

    # 用座標距離法算出圖中的座標距離，並和實際的距離做比值，求出待測實際距離
    D = dist.euclidean((PcX, PcY), (cX, cY)) / refObj[2]
    (mX, mY) = midpoint((PcX, PcY), (cX, cY))
    cv2.putText(orig, "{:.2f}cm".format(D), (int(mX), int(mY - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 200, 100), 2)
    # "{:.2f}in" 取到小數點第二位

    cv2.imshow("Image", orig)
    cv2.waitKey(0)
