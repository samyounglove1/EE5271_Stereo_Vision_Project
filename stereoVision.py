import numpy as np
import cv2

#internal utilities
import stereoUtils as utils





if __name__ == "__main__":
    print('something')
    iml = cv2.imread('./images/calibration/webcam_left_0.png')
    imr = cv2.imread('./images/calibration/webcam_right_0.png')
    
    uImr, uIml = utils.undistortRectify(iml, imr)
    cv2.imshow('left', iml)
    cv2.imshow('right', imr)
    cv2.imshow('ur left', uIml)
    cv2.imshow('ur right', uImr)
    #WIP
    
    cv2.waitKey(0)