import numpy as np
import cv2
from matplotlib import pyplot as plt

#internal utilities
import stereoUtils as utils

if __name__ == "__main__":
    K = np.matrix([[1500, 0, 640],[0, 1500, 360],[0, 0, 1]])
    b = .075 # 75 mm baseline distance
    print('something')
    iml = cv2.imread('./images/calibration/webcam_left_10.png', 0)
    imr = cv2.imread('./images/calibration/webcam_right_10.png',0)
    
    uImr, uIml = utils.undistortRectify(iml, imr)
    
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
    stereo.setMinDisparity(0)
    # stereo.setSpeckleRange(200)
    # stereo.setSpeckleWindowSize(12)
    # stereo.setTextureThreshold(5)
    disparity = stereo.compute(uIml,uImr)
    # disparity = stereo.compute(uImr,uIml)
    
    
    plt.imshow(disparity, 'gray')
    plt.show()
    #WIP
    disparity[disparity==0] = 0.0000001
    # status = np.ones(disparity.shape)
    u0 = K[0, 2]/2
    v0 = K[1, 2]/2
    Z = (K[0,0]/2) * b / disparity
    Z[Z < 0] = 0
    Z[Z > 2] = 2
    
    cv2.imshow('ur left', uIml)
    # cv2.imshow('disparity', )
    cv2.imshow('ur right', uImr)
    plt.imshow(Z, 'hot')
    plt.show()
    cv2.waitKey(0)