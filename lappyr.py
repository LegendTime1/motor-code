from __future__ import print_function
import sys
from PIL import Image
import imutils
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2 as cv

import video
from common import nothing, getsize

def build_lappyr(img, leveln=6, dtype=np.int16):
    img = dtype(img)
    levels = []
    for _i in xrange(leveln-1):
        next_img = cv.pyrDown(img)
        img1 = cv.pyrUp(next_img, dstsize=getsize(img))
        levels.append(img-img1)
        img = next_img
    levels.append(img)
    return levels

def merge_lappyr(levels):
    img = levels[-1]
    for lev_img in levels[-2::-1]:
        img = cv.pyrUp(img, dstsize=getsize(lev_img))
        img += lev_img
    return np.uint8(np.clip(img, 0, 255))


dist_coeffs = np.zeros((4,1)) #dummies, must be replaced by proper calibration
camera_matrix = np.array([[538.43377452, 0., 338.31871591], [  0., 538.4746563, 237.83438816], [  0., 0., 1.]])
  
cap = video.create_capture(0)
def left_or_right(cap):
    # import sys
    # try:
    #     fn = sys.argv[1]
    # except:
    #     fn = 0
    leveln = 6
    # trackbarptr = [43,38,44,10,25,10]
    trackbarptr = [43,38,44,10,25,10, 0.04, 0.01]
    cv.namedWindow('level control')
    for i in xrange(leveln):
        cv.createTrackbar('%d'%i, 'level control',trackbarptr[i], 50, nothing)
    cv.createTrackbar('%d'%6, 'level control',trackbarptr[i], 50, nothing)
    cv.createTrackbar('%d'%7, 'level control',trackbarptr[i], 50, nothing)
    # arrow_pts = np.array([[255.0,27.0],[364.0,143.0],[224.0,260.0],[225.0,172.0],[19.0,172.0],[19.0,114.0],[225.0,114.0]])
    arrow_pts = np.array([[330.0,166.0],[221.0,144.0],[220.0,100.0],[9.0,98.0],[9.0,64.0],[220.0,65.0],[221.0,20.0]])
    # image = cv.imread("Arrow.png")
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # thresh = cv.threshold(gray, 200, 255,
    #     cv.THRESH_BINARY_INV)[1]
    # cv.imshow("Thresh", thresh)
    # cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
    #     cv.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # c = max(cnts, key=cv.contourArea)
    # print(c)
    arrow_pts3d = np.append(arrow_pts, np.array([np.zeros(7, dtype = float)]).T, axis=1)
    # while True:
    if 1:
        ret = 0
        _ret, frame = cap.read()
        # frame = cv.imread("./frames/frame_0.png")
        frame2 = frame
        pyr = build_lappyr(frame, leveln)
        for i in xrange(leveln):
            v = int(cv.getTrackbarPos('%d'%i, 'level control') / 5)
            pyr[i] *= v
        const_arrpp_min = cv.getTrackbarPos('%d'%6, 'level control') / 5.
        # const_arrpp_max = cv.getTrackbarPos('%d'%7, 'level control') / 2.5
        # print("min ", const_arrpp_min)
        # print("max ", const_arrpp_max)
        res = merge_lappyr(pyr)
        # cv.imshow('laplacian pyramid filter', res)
        pil_image = Image.fromarray(res.astype(np.uint8))
        open_cv_image = np.array(pil_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        edged = cv.cvtColor(open_cv_image, cv.COLOR_BGR2GRAY)
        kernel = np.ones((3,3),np.uint8)
        for i in range(1):
            pass
        
        kernels = [np.ones((2*i+1,2*i+1),np.uint8) for i in range (5)]
        for i in range(1):
            edged = cv.morphologyEx(edged, cv.MORPH_OPEN,kernel=kernels[i])
        edged = cv.GaussianBlur(edged,(3,3),cv.BORDER_DEFAULT)
        edged = cv.GaussianBlur(edged,(5,5),cv.BORDER_DEFAULT)
        kernel2 = np.array([[-1,-1,-1], 
                       [-1, 9,-1],
                       [-1,-1,-1]])
        edged = cv.filter2D(edged, -1, kernel2) # applying the sharpening kernel to the input image & displaying it.
        _ , edged = cv.threshold(edged, 20,150,cv.THRESH_BINARY | cv.THRESH_OTSU)
        # downsample edged by ration 0.25
        # edged = cv.resize(edged, (0,0), fx=0.25, fy=0.25)
        cnts = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)
        screenCnt = []
        homograph = []
        Pnpout = [] 
        i = 0
        for c in cnts:
            i+=1
            peri = cv.arcLength(c, True)
            area = cv.contourArea(c)
            approx = cv.approxPolyDP(c, 0.02*peri, True)
            if (len(approx) == 7) and area/peri/peri < 0.08 and area/peri/peri > 0.005 and area < 11000 and area >500:
                if(cv.isContourConvex):
                    b = np.array([np.arctan2((approx[i%6-1][0][1]-approx[i%6][0][1]),(approx[i%6-1][0][0]-approx[i%6][0][0])) - np.arctan2((approx[i%6-2][0][1]-approx[i%6-1][0][1]),(approx[i%6-2][0][0]-approx[i%6-1][0][0])) for i in range(len(approx))])*180/np.pi
                    # print(b)
                    b = [i-360 if i>180  else i+360 if i<-180 else i for i in b]
                    # print("LLL ", b)
                    if  -b[3] < b[0] and -b[3] < b[1] and -b[3] < b[2] and -b[3] < b[4] and -b[3] < b[0]:
                        # if 1:
                        if (b[3] < 0 and b[0] > 0  and b[1] > 0  and b[2] > 0 and b[4] > 0 and b[5] > 0 and b[6] > 0) or (b[3] > 0 and b[0] < 0  and b[1] < 0  and b[2] < 0 and b[4] < 0 and b[5] < 0 and b[6] < 0):
                        
                            # print(approx)
                            screenCnt.append(approx)
                            r = np.reshape(approx[:,:,0], (-1))
                            # print(r)6
                            c = np.mean(r)
                            d = np.median(r)
                            # print(d, c)
                            if d>c:
                                ret = 1 # RIGHT
                            if d<c:
                                ret = -1 # LEFT
                        else:
                            pass
                            # print("OOOO ", approx)
                # h_mat, status = homograph.append(cv.findHomography(approx, arrow_pts,cv.RANSAC))
                # print(approx[:,0,:],'H', arrow_pts3d[[1,3,5,6]])
                # Pnpout.append(cv.solvePnP(arrow_pts3d, approx[:,0,:], camera_matrix, dist_coeffs))
                # Pnpout.append(cv.solvePnP(arrow_pts3d[1,3,5,6], approx[:,0,:], camera_matrix, dist_coeffs))
            else:
                if peri == 0:
                    continue
                # print ("LLL ", area/peri/peri, area, 0.03*peri)
                # print(area)
                # print(peri)
            # if(i>4):
            #     break
        # if screenCnt is not []:
        #     cv.drawContours(frame, screenCnt, -1, (0, 255, 0), 3)
            # cv.drawFrameAxes(frame, camera_matrix, dist_coeffs, Pnpout[1], Pnpout[2], 300, 3 )
            # cv.imshow("Arrow", frame)
            # save frame to a png file
            # cv.imwrite('frame.png', frame)
            # cv.imshow("edged", edged)
            # cv.waitKey()
        # Display Output
        # cv.imshow("Laplace of Image", res)
        k = cv.waitKey(30)
        print (ret)
        return ret#, frame
        # if k == 27:
        #     return
        # elif k==ord('y'):
        #     print(k)
        #     if trackbarptr[0] < 50:
        #         trackbarptr[0]+=1
        #         cv.setTrackbarPos('%d'%0,'level control', trackbarptr[0])
        # elif k==ord('Y'):
        #     print
        #     if trackbarptr[0] > 0:
        #         trackbarptr[0]-=1
        #         cv.setTrackbarPos('%d'%0,'level control', trackbarptr[0])
        # elif k==ord('u'):
        #     print(k)
        #     if trackbarptr[1] < 50:
        #         trackbarptr[1]+=1
        #         cv.setTrackbarPos('%d'%1,'level control', trackbarptr[1])
        # elif k==ord('U'):
        #     print
        #     if trackbarptr[1] > 0:
        #         trackbarptr[1]-=1
        #         cv.setTrackbarPos('%d'%1,'level control', trackbarptr[1])
        # elif k==ord('i'):
        #     print(k)
        #     if trackbarptr[2] < 50:
        #         trackbarptr[2]+=1
        #         cv.setTrackbarPos('%d'%2,'level control', trackbarptr[2])
        # elif k==ord('I'):
        #     print
        #     if trackbarptr[2] > 0:
        #         trackbarptr[2]-=1
        #         cv.setTrackbarPos('%d'%2,'level control', trackbarptr[2])
        # elif k==ord('o'):
        #     print(k)
        #     if trackbarptr[3] < 50:
        #         trackbarptr[3]+=1
        #         cv.setTrackbarPos('%d'%3,'level control', trackbarptr[3])
        # elif k==ord('O'):
        #     print
        #     if trackbarptr[3] > 0:
        #         trackbarptr[3]-=1
        #         cv.setTrackbarPos('%d'%3,'level control', trackbarptr[3])
        # elif k==ord('p'):
        #     print(k)
        #     if trackbarptr[4] < 50:
        #         trackbarptr[4]+=1
        #         cv.setTrackbarPos('%d'%4,'level control', trackbarptr[4])
        # elif k==ord('P'):
        #     print
        #     if trackbarptr[4] > 0:
        #         trackbarptr[4]-=1
        #         cv.setTrackbarPos('%d'%4,'level control', trackbarptr[4])
        # elif k==ord('['):
        #     print(k)
        #     if trackbarptr[5] < 50:
        #         trackbarptr[5]+=1
        #         cv.setTrackbarPos('%d'%5,'level control', trackbarptr[5])
        # elif k==ord('{'):
        #     print
        #     if trackbarptr[5] > 0:
        #         trackbarptr[5]-=1
        #         cv.setTrackbarPos('%d'%5,'level control', trackbarptr[5])
        # else:
        #     pass
        # if cv.waitKey(1) == 27:
        #     break
    # print('Done')
# if __name__ == '__main__':
#     print(__doc__)
#     main()
#     cv.destroyAllWindows()
# arrow pointing right of viewer
# top acute vertex: (255,27)
# front tip: (364,143)
# lower acute vertex: (224,260)
# lower join of rectangle with triangle: (225,172)
# lower vertex of tail: (19,172)
# upper vertex of tail: (19,114)
# lower join of rectangle with triangle: (225,114)
# All the vertices are in clockwise orientation
while 1:
    left_or_right(cap)