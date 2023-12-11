import numpy as np
import cv2
from matplotlib import pyplot as plt

#internal utilities
import stereoUtils as utils
import ARMarkers as ar

if __name__ == "__main__":    
    K = np.matrix([[1500, 0, 640],[0, 1500, 360],[0, 0, 1]])
    # K = np.matrix([[717.22735137, 0, 320.22308769],[0, 717.22735137, 177.63512465],[0, 0, 1]])
    b = .075 # 75 mm baseline distance
    # print('something')
    
    
    # OpenCV webcam test
    print('opening cam 1')
    # cam0 = cv2.VideoCapture(0, cv2.CAP_DSHOW) #left
    cam0 = cv2.VideoCapture(0, cv2.CAP_V4L2) #left
    print('cam 1 opened')
    cam0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam0.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cam0.set(cv2.CAP_PROP_FPS, 10)
    print('cam 1 configured')
    
    print('opening cam 2')
    # cam1 = cv2.VideoCapture(2, cv2.CAP_DSHOW) #right
    cam1 = cv2.VideoCapture(2, cv2.CAP_V4L2) #right
    print('cam 2 opened')
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cam1.set(cv2.CAP_PROP_FPS, 10)
    print('cam 2 configured')

    
    maxDisparity = 128
    stereo = cv2.StereoSGBM_create(0, maxDisparity, 21)
    # stereo.setMode(cv2.StereoSGBM_MODE_HH)
    
    # fig, axs = plt.subplots(2, 3)
    # plt.ion()
    # fig.show()
    # axs[0, 0].set_title('Image')
    # axs[0, 1].set_title('Disparity Map')
    # axs[0, 2].set_title('Depth Map')
    # axs[1, 0].setTitle('Image')
    
    plt.ion()
    cv2.namedWindow('led matrix', cv2.WINDOW_NORMAL)
    
    check0, iml = cam0.read()
    check1, imr = cam1.read()
    
    
    # key = cv2.waitKey()
    
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
        disparity_scaled[disparity_scaled == 0] = 0.0001
        
        u0 = K[0, 2]/2
        v0 = K[1, 2]/2
        Z = (K[0,0]/2) * b / disparity_scaled
        Z[Z < 0] = 0
        
        limit = 3
        Z[Z > limit] = limit
        depth = Z
        
        # depth_colour_mapped = cv2.applyColorMap(
        #     (depth * (256. / limit)).astype(np.uint8),
        #     cv2.COLORMAP_HOT)
        depth_colour_mapped = cv2.applyColorMap(
            (depth * (256. / limit)).astype(np.uint8),
            cv2.COLORMAP_HOT)
        # plt.imshow(Z, 'hot')
        # cv2.imshow('depth estimate', Z)
        # cv2.imshow('disparity map', disparity_colour_mapped)
        # cv2.imshow('depth estimate', depth_colour_mapped)
        # plt.imshow(depth, 'hot')
        cv2.imshow('undistorted rectified left image', uiml)
        
        # find region of interest
        roi, found = ar.findArZone(uiml, depth)
        
        #need to potentially crop more of the image to the left
        # h, w = depth.shape
        if not found:
            roi = roi[:,127:]
            
        roi_inv = limit - roi[:]
        
        roi_colormap = cv2.applyColorMap(
            (roi * (256. / limit)).astype(np.uint8),
            cv2.COLORMAP_HOT)
        cv2.imshow('region of interest depth', roi_colormap)

        
        led_matrix = cv2.resize(roi_colormap, (32, 32))
        cv2.imshow('led matrix', led_matrix)
        # cv2.imshow('maskedZoneU', maskeduIml)
        
        # axs[0, 0].imshow(uiml)
        # axs[0, 1].imshow(disparity_scaled)
        # axs[0, 2].imshow(Z, 'hot')
        
        key = cv2.waitKey(50)
        if key == 27:
            break
        
    cv2.destroyAllWindows()
