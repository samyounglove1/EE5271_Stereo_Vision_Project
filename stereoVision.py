import numpy as np
import cv2
from matplotlib import pyplot as plt

#internal utilities
import stereoUtils as utils

if __name__ == "__main__":    
    K = np.matrix([[1500, 0, 640],[0, 1500, 360],[0, 0, 1]])
    # K = np.matrix([[717.22735137, 0, 320.22308769],[0, 717.22735137, 177.63512465],[0, 0, 1]])
    b = .075 # 75 mm baseline distance
    # print('something')
    
    
    # OpenCV webcam test
    print('opening cam 1')
    cam0 = cv2.VideoCapture(0, cv2.CAP_DSHOW) #left
    print('cam 1 opened')
    cam0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam0.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cam0.set(cv2.CAP_PROP_FPS, 10)
    print('cam 1 configured')
    
    print('opening cam 2')
    cam1 = cv2.VideoCapture(1, cv2.CAP_DSHOW) #right
    print('cam 2 opened')
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cam1.set(cv2.CAP_PROP_FPS, 10)
    print('cam 2 configured')
    
    iml = cv2.imread('./images/calibration/webcam_left_10.png', 0)
    imr = cv2.imread('./images/calibration/webcam_right_10.png',0)
    
    maxDisparity = 128
    stereo = cv2.StereoSGBM_create(0, maxDisparity, 21)
    
    
    # plt.ion()
    while True:
        check0, iml = cam0.read()
        imlg = cv2.cvtColor(iml, cv2.COLOR_BGR2GRAY)
        check1, imr = cam1.read()
        imrg = cv2.cvtColor(imr, cv2.COLOR_BGR2GRAY)
        uimr,uiml = utils.undistortRectify(imrg,imlg)
        
        disparity = stereo.compute(uiml, uimr)
        cv2.filterSpeckles(disparity, 0, 40, maxDisparity)
        _, disparity = cv2.threshold(disparity, 0, maxDisparity * 16, cv2.THRESH_TOZERO)
        disparity_scaled = (disparity / 16.).astype(np.uint8)
        disparity_colour_mapped = cv2.applyColorMap(
            (disparity_scaled * (256. / maxDisparity)).astype(np.uint8),
            cv2.COLORMAP_HOT)
        cv2.imshow('disparity map', disparity_colour_mapped)
        
        u0 = K[0, 2]/2
        v0 = K[1, 2]/2
        Z = (K[0,0]/2) * b / disparity_scaled
        Z[Z < 0] = 0
        Z[Z > 5] = 5
        depth = Z
        
        depth_colour_mapped = cv2.applyColorMap(
            (depth * (256. / 5)).astype(np.uint8),
            cv2.COLORMAP_HOT)
        # plt.imshow(Z, 'hot')
        # cv2.imshow('depth estimate', Z)
        cv2.imshow('depth estimate', depth_colour_mapped)
        cv2.imshow('uleft', uiml)
        
        
        
        
        key = cv2.waitKey(50)
        if key == 27:
            break
    
    
    #     # Scaling down the disparity values and normalizing them
    #     disparity2 = (disparity / 16.0 - minDisparity) / numDisparities
    #     # disparity[disparity==0] = 0.0000001
    #     # status = np.ones(disparity.shape)
    #     u0 = K[0, 2]/2
    #     v0 = K[1, 2]/2
    #     Z = (K[0,0]/2) * b / disparity
    #     # Z[Z < 0] = 0
    #     # Z[Z > 2] = 2
    
    
    # plt.imshow(disparity, 'gray')
    # plt.show()
    # #WIP
    # disparity[disparity==0] = 0.0000001
    # # status = np.ones(disparity.shape)
    # u0 = K[0, 2]/2
    # v0 = K[1, 2]/2
    # Z = (K[0,0]/2) * b / disparity
    # Z[Z < 0] = 0
    # Z[Z > 2] = 2
    
    # cv2.imshow('ur left', uIml)
    # # cv2.imshow('disparity', )
    # cv2.imshow('ur right', uImr)
    # plt.imshow(Z, 'hot')
    # plt.show()
    # cv2.waitKey(0)