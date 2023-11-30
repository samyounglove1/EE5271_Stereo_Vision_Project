import cv2
import numpy as np

AR_MARKER_DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
AR_MARKER_SIZE = 300
ORIGIN_MARKER_ID = 1


# Generate an AR marker with a given ID using the dictionary defined above
def generateARMarker(id):
    marker = np.zeros((AR_MARKER_SIZE, AR_MARKER_SIZE, 1), dtype="uint8")
    cv2.aruco.generateImageMarker(AR_MARKER_DICTIONARY, id, AR_MARKER_SIZE, marker, 1)
    cv2.imwrite("images/ar_markers/marker{}.png".format(id), marker)



def test():
    # This is a picture of a marker from DICT_4X4_50
    img1 = cv2.imread("../FinalProjectTemp/images/stereoLeft/imageL0.png")
    

    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(AR_MARKER_DICTIONARY, params)
    corners, ids, rejected = detector.detectMarkers(img1)
    cv2.aruco.drawDetectedMarkers(img1, corners, ids)
    cv2.imshow('Img 1', img1)

    # if you call poseEstimation() and then cv2.drawFrameAxes() it should
    # correctly show a set of axes on the image, I just haven't done calibration
    # with my camera yet so I can't test it

    print(corners)
    print(ids)

    print("Press any key to exit")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    



def poseEstimation(img, camera_matrix, dist_coeffs, marker_side_length):
    marker_corners_world_frame = np.array([(0, 0, 0),
                                  (marker_side_length, 0, 0),
                                  (marker_side_length, marker_side_length, 0),
                                  (0, marker_side_length, 0)])

    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(AR_MARKER_DICTIONARY, params)
    corners, ids, rejected = detector.detectMarkers(img)

    r_vec = None
    t_vec = None
    for i in range(len(ids)):
        if id[i][0] == ORIGIN_MARKER_ID:
            succ, r_vec, t_vec = cv2.solvePnP(marker_corners_world_frame, corners, camera_matrix, dist_coeffs)

    return r_vec, t_vec



if __name__ == "__main__":
    test()
