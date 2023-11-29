import cv2
from machinevisiontoolbox import Image
from machinevisiontoolbox import WebCam
# from machinevisiontoolbox import CentralCamera
# import machinevisiontoolbox as mvtb
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    K = np.matrix([[1500, 0, 640],[0, 1500, 360],[0, 0, 1]])
    b = .075 # 75 mm baseline distance
    # cam = StereoCam(K, K, b)
        
    # OpenCV webcam test
    cam0 = cv2.VideoCapture(0) #left
    cam0.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam0.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
    cam0.set(cv2.CAP_PROP_FPS, 5)
    cam1 = cv2.VideoCapture(1) #right
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
    cam1.set(cv2.CAP_PROP_FPS, 5)
    
    # cv2.namedWindow('cam left', cv2.WINDOW_NORMAL)
    # cv2.namedWindow('cam right', cv2.WINDOW_NORMAL)
    plt.ion()
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    
    while True:
        check0, i0 = cam0.read()
        assert(check0)
        # cv2.imshow('cam0', frame0)
        i0 = cv2.cvtColor(i0, cv2.COLOR_BGR2GRAY)
        
        check1, i1 = cam1.read()
        assert(check0)
        i1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('cam1', frame1)
        
        # # convert from opencv matrix to mvtb image
        # il = Image(image=i0)
        # ir = Image(image=i1)
        # # run stereo block match
        # di = il.stereo_BM(ir, hw=3, drange=[150, 260], speckle=(200, 2))

        # u, v = il.meshgrid()
        # status = np.ones(di.shape)
        # u0 = K[0, 2]/4
        # v0 = K[1, 2]/4
        # Z = (K[0,0]/4) * b / di.image
        
        # max = 5
        
        # Z[Z > 5] = 0 # can use to clamp max range
        # # im = Image(image=Z)
        
        # normalize = (Z[:,:] / np.max(Z)) * 255 #normalize to 0 - 255 range to look better
        
        # # cast back to opencv matrix
        # depth_map = np.asarray(normalize, dtype=np.uint8)
        # cv2.imshow('Depth Map', depth_map)
        
        stereo = cv2.StereoBM_create(numDisparities=64, blockSize=11)
        disparity = stereo.compute(i0, i1)
        # plt.imshow(disparity, cmap='hot')
        # plt.ion()
        # plt.show()
        cv2.imshow('cam left', i0)
        cv2.imshow('disparity', disparity)
        cv2.imshow('cam right', i1)

        key = cv2.waitKey(20)
        if key == 27:
            break
    
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()
