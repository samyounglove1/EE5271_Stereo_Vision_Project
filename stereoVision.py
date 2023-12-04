import numpy as np
import cv2
from matplotlib import pyplot as plt

#internal utilities
import stereoUtils as utils


def interactiveDisparity():
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
    
    def f(x): return
    cv2.namedWindow('disp', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('disp', 800, 1200) 
    cv2.createTrackbar('numDisparities', 'disp', 1, 50, f)
    cv2.createTrackbar('blockSize', 'disp', 5, 50, f)
    cv2.createTrackbar('preFilterType', 'disp', 1, 1, f)
    cv2.createTrackbar('preFilterSize', 'disp', 2, 25, f)
    cv2.createTrackbar('preFilterCap', 'disp', 5, 62, f)
    cv2.createTrackbar('textureThreshold', 'disp', 10, 100, f)
    cv2.createTrackbar('uniquenessRatio', 'disp', 15, 100, f)
    cv2.createTrackbar('speckleRange', 'disp', 0, 100, f)
    cv2.createTrackbar('speckleWindowSize', 'disp', 3, 25, f)
    cv2.createTrackbar('disp12MaxDiff', 'disp', 0, 100, f)
    cv2.createTrackbar('minDisparity', 'disp', 0, 25, f)
    
    # iml = cv2.imread('./images/calibration/webcam_left_10.png', 0)
    # imr = cv2.imread('./images/calibration/webcam_right_10.png',0)
    
    
    # K = np.matrix([[1500, 0, 640],[0, 1500, 360],[0, 0, 1]])
    K = np.matrix([[717.22735137, 0, 320.22308769],[0, 717.22735137, 177.63512465],[0, 0, 1]])
    b = .075 # 75 mm baseline distance
    plt.ion()

    while True:
        iml = cam0.read()
        imr = cam1.read()
        uImr, uIml = utils.undistortRectify(imr, iml)
        cv2.imshow('rectified left', uIml)
        
        # Updating the parameters based on the trackbar positions
        numDisparities = cv2.getTrackbarPos('numDisparities', 'disp') * 16
        blockSize = cv2.getTrackbarPos('blockSize', 'disp') * 2 + 5
        preFilterType = cv2.getTrackbarPos('preFilterType', 'disp')
        preFilterSize = cv2.getTrackbarPos('preFilterSize', 'disp') * 2 + 5
        preFilterCap = cv2.getTrackbarPos('preFilterCap', 'disp')
        textureThreshold = cv2.getTrackbarPos('textureThreshold', 'disp')
        uniquenessRatio = cv2.getTrackbarPos('uniquenessRatio', 'disp')
        speckleRange = cv2.getTrackbarPos('speckleRange', 'disp')
        speckleWindowSize = cv2.getTrackbarPos('speckleWindowSize', 'disp') * 2
        disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff', 'disp')
        minDisparity = cv2.getTrackbarPos('minDisparity', 'disp')
        
        # Setting the updated parameters before computing disparity map
        stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
        stereo.setNumDisparities(numDisparities)
        stereo.setBlockSize(blockSize)
        stereo.setPreFilterType(preFilterType)
        stereo.setPreFilterSize(preFilterSize)
        stereo.setPreFilterCap(preFilterCap)
        stereo.setTextureThreshold(textureThreshold)
        stereo.setUniquenessRatio(uniquenessRatio)
        stereo.setSpeckleRange(speckleRange)
        stereo.setSpeckleWindowSize(speckleWindowSize)
        stereo.setDisp12MaxDiff(disp12MaxDiff)
        stereo.setMinDisparity(minDisparity)
        

        # Calculating disparity using the StereoBM algorithm
        disparity = stereo.compute(uIml, uImr)
        # NOTE: Code returns a 16bit signed single channel image,
        # CV_16S containing a disparity map scaled by 16. Hence it
        # is essential to convert it to CV_32F and scale it down 16 times.

        # Converting to float32
        disparity = disparity.astype(np.float32)

        # Scaling down the disparity values and normalizing them
        # disparity = (disparity / 16.0 - minDisparity) / numDisparities
        disparity[disparity==0] = 0.0000001
        # status = np.ones(disparity.shape)
        u0 = K[0, 2]/2
        v0 = K[1, 2]/2
        Z = (K[0,0]/2) * b / disparity
        Z[Z < 0] = 0
        Z[Z > 2] = 2
        
        
        

        # Displaying the disparity map
        cv2.imshow("disp", disparity)
        # Close window using esc key
        plt.imshow(Z, 'hot')
        if cv2.waitKey(50) == 27:
            break




if __name__ == "__main__":
    # interactiveDisparity()
    
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