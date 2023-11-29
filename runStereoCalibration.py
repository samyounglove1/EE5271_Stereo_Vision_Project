import cv2
import numpy as np
from tqdm import tqdm

def stereoWebcamCalibrate():
    pathL = "./images/calibration/webcam_left_"
    pathR = "./images/calibration/webcam_right_"

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((10*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:10,0:7].T.reshape(-1,2)
    
    img_ptsL = []
    img_ptsR = []
    obj_pts = []
    
    cv2.namedWindow('cornersR', cv2.WINDOW_NORMAL)
    cv2.namedWindow('cornersL', cv2.WINDOW_NORMAL)
    
    # first calibrate cams individually
    for i in tqdm(range(0, 20)):
        imgL = cv2.imread(pathL+"%d.png"%i)
        imgR = cv2.imread(pathR+"%d.png"%i)
        imgL_g = cv2.imread(pathL+"%d.png"%i,0)
        imgR_g = cv2.imread(pathR+"%d.png"%i,0)
        
        outputL = imgL.copy()
        outputR = imgR.copy()
        
        retR, cornersR =  cv2.findChessboardCorners(outputR,(10,7),None)
        retL, cornersL = cv2.findChessboardCorners(outputL,(10,7),None)
        
        if retR and retL:
            obj_pts.append(objp)
            cv2.cornerSubPix(imgR_g, cornersR,(11, 11), (-1, -1), criteria)
            cv2.cornerSubPix(imgL_g, cornersL,(11, 11), (-1, -1), criteria)
            cv2.drawChessboardCorners(outputR,(10,7),cornersR,retR)
            cv2.drawChessboardCorners(outputL,(10,7),cornersL,retL)    
            cv2.imshow('cornersR',outputR)
            cv2.imshow('cornersL',outputL)
            cv2.waitKey(250)
            
            img_ptsL.append(cornersL)
            img_ptsR.append(cornersR)
    # Calibrating left camera
    retL, mL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_g.shape[::-1],None,None)
    hL,wL= imgL_g.shape[:2]
    new_mL, roiL= cv2.getOptimalNewCameraMatrix(mL,distL,(wL,hL),1,(wL,hL))
    
    # Calibrating right camera
    # \/ returns ?, cam matrix, distortion coefficients, rotation and translation vectors
    retR, mR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_g.shape[::-1],None,None)
    hR,wR= imgR_g.shape[:2]
    new_mR, roiR= cv2.getOptimalNewCameraMatrix(mR,distR,(wR,hR),1,(wR,hR))
    cv2.destroyAllWindows()
    
    #now we do stereo calibration with our newly found parameters
    flags = cv2.CALIB_FIX_INTRINSIC #fixed intrinsic paramters
    #done because we only want rotation, translation, and F,E matrices
    
    criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    retS, new_mL, distL, new_mR, distR, rot, trans, Em, Fm = cv2.stereoCalibrate(
        obj_pts, img_ptsL, img_ptsR, new_mL, distL, new_mR, distR, imgL_g.shape[::-1], criteria_stereo, flags)
    
    # now we rectify the images
    rectify_scale = 1
    rectL, rectR, projectL, projectR, Q, roiL, roiR = cv2.stereoRectify(new_mL, distL, new_mR, distR, imgL_g.shape[::-1], rot, trans, rectify_scale, (0, 0))

    stereoMapL = cv2.initUndistortRectifyMap(new_mL, distL, rectL, projectL, imgL_g.shape[::-1], cv2.CV_16SC2)       
    stereoMapR = cv2.initUndistortRectifyMap(new_mR, distR, rectR, projectR, imgR_g.shape[::-1], cv2.CV_16SC2)       
    
    print('Done! Saving found stereo maps!')
    file = cv2.FileStorage('webcamStereoMap.xml', cv2.FileStorage_WRITE)
    
    file.write('webcamStereoMapLX', stereoMapL[0])
    file.write('webcamStereoMapLY', stereoMapL[1])
    file.write('webcamStereoMapRX', stereoMapR[0])
    file.write('webcamStereoMapRY', stereoMapR[1])
    
    file.release()
            
if __name__ == "__main__":
    stereoWebcamCalibrate()