import math
import cv2
import numpy as np
import rospkg
import os

##############################################################################
        # template preprocess 
_img = cv2.imread('example.jpg')
_draw_img = _img.copy()

        # Bilateral Filter smoothes images while preserving edges,
        # by means of a nonlinear combination of nearby image values.
        # cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace)
        # d - Diameter of each pixel neighborhood that is used during filtering.
_blur = cv2.bilateralFilter(_img, 19, 130, 30)
_blur = cv2.medianBlur(_blur, 9)

_img_gray = cv2.cvtColor(_blur, cv2.COLOR_BGR2GRAY)
_xgrd = cv2.Sobel(_img_gray, cv2.CV_16SC1, 1, 0)
_ygrd = cv2.Sobel(_img_gray, cv2.CV_16SC1, 0, 1)
_img = cv2.Canny(_xgrd, _ygrd, 30, 220)

        # Here we obtain the edge, then show using code below
        # cv2.imshow('1', img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        
_w, _h = _img.shape
_img_1 = _img[:, :_w]
_img_2 = _img[:, _w:]

        # cv2.findContours to find contour
        # variable _contours_1 stores all contours, each of which is composed of
        # a series of pixel point 
        # For example: len(contours) contours[0] 
        # rectangle
_img_1, _contours_1, hierarchy = cv2.findContours(_img_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # circle
_img_2, _contours_2, hierarchy = cv2.findContours(_img_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
##############################################################################







_img = cv2.imread('test9.bmp')
_draw_img = _img.copy()
#cv2.imshow('_img', _img)

_blur = cv2.bilateralFilter(_img, 19, 130, 30)
_blur = cv2.medianBlur(_blur, 9)
#cv2.imshow('_blur', _blur)


_img_gray = cv2.cvtColor(_blur, cv2.COLOR_BGR2GRAY)
_xgrd = cv2.Sobel(_img_gray, cv2.CV_16SC1, 1, 0)
_ygrd = cv2.Sobel(_img_gray, cv2.CV_16SC1, 0, 1)
_img = cv2.Canny(_xgrd, _ygrd, 3, 10)
cv2.imshow('_Canny', _img)

_img, contoursUnfiltered, hierarchy = cv2.findContours(_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = []
for i in range(len(contoursUnfiltered)):
	if cv2.contourArea(contoursUnfiltered[i]) > 1500:
		contours.append(contoursUnfiltered[i])	
_draw_img=cv2.drawContours(_draw_img,contours,-1,(0,255,0),3)
cv2.imshow('_draw_img', _draw_img)
cv2.waitKey()
cv2.destroyAllWindows()


center_value = []
tip_value = []
shape = [] # 0 represents rectangle while 1 represents circle or ellipse
theta = []
for i in range(len(contours) // 2):
    if i % 2 == 0: #is contour of the base
        N = cv2.moments(contours[i * 2])
        _center_x = int(N["m10"] / N["m00"])
        _center_y = int(N["m01"] / N["m00"])
        _draw_img=cv2.circle(_draw_img, (int(_center_x), int(_center_y)), 7, [255,0,0], -1) #center, blu
        center_value.append([_center_x,_center_y])

        _draw_img = cv2.putText(_draw_img,str(int(_center_x))+","+str(int(_center_y)),(int(_center_x+30), int(_center_y+30)),cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),3)

        rect = cv2.matchShapes(contours[i * 2], _contours_1[0], 1, 0.0)
        circ = cv2.matchShapes(contours[i * 2], _contours_2[0], 1, 0.0) 
        if rect > circ:
            shape.append(1) #is circle, GREEN
            ######
            _draw_img = cv2.drawContours(_draw_img,contours[i * 2],-1,(255,255,0),3) #is circle, GREEN
        else:
            shape.append(0)#is rect, RED
            ######
            _draw_img = cv2.drawContours(_draw_img,contours[i * 2],-1,(0,0,255),3)#is rect, RED
    else:  #is contour of the arrow
        arrow = contours[i * 2]
        block = contours[i * 2 -2]
        distprev=1000000
        for pointsInArrow in arrow:
            for pointsInBlock in block:
                dist = np.linalg.norm(pointsInArrow - pointsInBlock)
                if dist < distprev:
                    distprev = dist
                    arrowClosest = pointsInArrow
        ######
        _draw_img=cv2.circle(_draw_img, (arrowClosest[0][0],arrowClosest[0][1]), 7, [255,255,255], -1)# IS tip, white
        tip_value.append([arrowClosest[0][0],arrowClosest[0][1]]) 
for i in range(len(center_value)):
    angle = -math.atan2(tip_value[i][1]-center_value[i][1],tip_value[i][0]-center_value[i][0])/3.1415*180
    theta.append(angle)
    ######
    _draw_img = cv2.putText(_draw_img,str(int(angle)),(center_value[i][0],center_value[i][1]),cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),3)
		
#print(center_value)
print(shape)
cv2.imshow('_draw_img', _draw_img)            
cv2.waitKey()
cv2.destroyAllWindows()
