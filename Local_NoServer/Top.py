#Simple script used for debugging the feature matching functions.

import sys
import os
import cv2
import numpy as np
from django.conf import settings

#Go Root dir for the feature matching 
os.chdir('..\\WebProject')
sys.path.append('app\\')
import Alignment2D

#img1 = cv2.imread('media/testImages/fit01.jpg', cv2.CV_LOAD_IMAGE_COLOR)
#img2 = cv2.imread('media/testImages/Fit02.jpg', cv2.CV_LOAD_IMAGE_COLOR)

img1 = cv2.imread('media/testImages/IMG_5283_2.jpg', cv2.CV_LOAD_IMAGE_COLOR)
img2 = cv2.imread('media/testImages/IMG_5283_1.jpg', cv2.CV_LOAD_IMAGE_COLOR)


(kp1Matches, kp2Matches) = Alignment2D.ExtractFeatures(img1, img2)

Transform = Alignment2D.AlignImages ( kp1Matches, kp2Matches, 'levenberg', 'homography' ) 
#Transform = Alignment2D.AlignImages ( kp1Matches, kp2Matches, 'lls', 'homography' ) 

#Overlay the two images, showing the detected feature.
rows,cols,colours = img1.shape
Canvas1 = np.zeros( ( rows*2, cols*2, colours) , img1.dtype );
Canvas2 = np.copy(Canvas1)

finalRows, finalCols, colours = Canvas1.shape
M = np.float32([[1,0,0],[0,1,0], [0,0,1]])

img3 = cv2.drawKeypoints(img1, kp1Matches,color=(0,0,255) )
cv2.warpPerspective(img3, M,(finalCols, finalRows), Canvas1)

img2 = cv2.drawKeypoints(img2, kp2Matches,color=(255,0,0) )
cv2.warpPerspective(img2, Transform,(finalCols, finalRows), Canvas2, borderMode=cv2.BORDER_TRANSPARENT)

alpha = 0.5
beta = ( 1.0 - alpha )
cv2.addWeighted( Canvas1, alpha, Canvas2, beta, 0.0, Canvas1)
cv2.namedWindow('Features1', cv2.WINDOW_NORMAL) 
cv2.imshow('Features1', Canvas1)
cv2.waitKey(0)
cv2.destroyAllWindows()