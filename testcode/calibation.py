import numpy as np
import cv2
import glob
#14 9
# termination criteria

chessw_point = 6
chessL_point = 9
distance = 25.4

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessw_point*chessL_point,3), np.float32)
objp[:,:2] = np.mgrid[0:chessL_point,0:chessw_point].T.reshape(-1,2)*distance
print(objp)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('data4/*.png')


capture = cv2.VideoCapture( 0 );
if capture == None:
    print("Couldn't open the camera");
    


for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret = False
    ret, corners = cv2.findChessboardCorners(gray, (chessL_point,chessw_point),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)
        

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (chessL_point,chessw_point), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)


# mtx = cameraMatrix   相機內部參數矩陣 
# dist = distCoeffs  distortion coefficients, (k1, k2, p1, p2[, k3[, k4, k5, k6]])
# rvecs = 所預估的旋轉矩陣 (rotation)
# rvecs = 所預估的位移矩陣 (translation) 
ret, mtx, dist, rvecs, tvecs= cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
print('*'*8)
print(ret)
print('*'*8)
print(mtx) 
print('*'*8)
print(dist)
print('*'*8)
'''
print(rvecs)
print('*'*8)
print(tvecs)
'''

img = cv2.imread('test_image1.png')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

#a = np.dot(mtx, dist)
#print(a)

dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
print(type(dst))
cv2.imwrite('calibresult.jpg',dst)

mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresul1t.jpg',dst)
