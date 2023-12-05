import cv2
import numpy as np

AR_MARKER_DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
AR_MARKER_SIZE = 300
ORIGIN_MARKER_ID = 0


# Generate an AR marker with a given ID using the dictionary defined above
def generateARMarker(id):
    marker = np.zeros((AR_MARKER_SIZE, AR_MARKER_SIZE, 1), dtype="uint8")
    cv2.aruco.generateImageMarker(AR_MARKER_DICTIONARY, id, AR_MARKER_SIZE, marker, 1)
    cv2.imwrite("images/ar_markers/marker{}.png".format(id), marker)



# Get the outer corners of the four AR markers.
# Returns None if all markers are not detected. If this happens, get a new image and try again.
# Only need to get the corners once at the beginning of the program.
def getBoundaryCorners(image):
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(AR_MARKER_DICTIONARY, params)
    corners, ids, rejected = detector.detectMarkers(image)

    num_ids = len(ids)
    if ids is None or not (num_ids == 3 or num_ids == 4):
        return None
    
    outer_corners = []
    for i in range(num_ids):
        id = ids[i][0]
        outer_corners.append(corners[i][0][id])

    return outer_corners



# Crops the depth map to fit the boundaries defined by the AR markers
def cropDepthMap(depth_map, corners):
    corners_x = []
    corners_y = []
    for i in range(len(corners)):
        corners_x.append(corners[i][0])
        corners_y.append(corners[i][1])

    x_min = int(np.min(corners_x))
    x_max = int(np.max(corners_x))
    y_min = int(np.min(corners_y))
    y_max = int(np.max(corners_y))
    return depth_map[y_min:y_max, x_min:x_max]



def test():
    # This is a picture of a marker from DICT_4X4_50
    img = cv2.imread("../FinalProjectTemp/images/stereoLeft/imageL0.png")
    

    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(AR_MARKER_DICTIONARY, params)
    corners, ids, rejected = detector.detectMarkers(img)
    cv2.aruco.drawDetectedMarkers(img, corners, ids)
    cv2.imshow('Img 1', img)

    # if you call poseEstimation() and then cv2.drawFrameAxes() it should
    # correctly show a set of axes on the image, I just haven't done calibration
    # with my camera yet so I can't test it

    print(corners)
    print(ids)
    print(corners[0][0][0][0])

    corners_u = []
    corners_v = []
    for i in range(4):
        id = ids[i][0]
        corners_u.append(corners[i][0][id][0])
        corners_v.append(corners[i][0][id][1])

    print(corners_u)
    print(corners_v)

    u_min = int(np.min(corners_u))
    u_max = int(np.max(corners_u))
    v_min = int(np.min(corners_v))
    v_max = int(np.max(corners_v))

    print(img.shape)
    print(u_min, u_max, v_min, v_max)
    print()

    cropped_img = img[v_min:v_max, u_min:u_max]
    cv2.imshow("Cropped image", cropped_img)

    # id_index = [-1, -1, -1, -1]
    # img_corners = []
    # for i in range(4):
    #     id = ids[i][0]
    #     id_index[id] = i
    #     print(id)
    #     print(corners[i][0][id])
    #     img_corners.append(corners[i][0][id])
    # print(img_corners)

    # pts = np.array([[img_corners[id_index[0]], img_corners[id_index[1]], img_corners[id_index[2]], img_corners[id_index[3]]]], dtype=np.int32)
    
    # removePixelsOutsideBoundary(img, pts)


    print("Press any key to exit")
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# This is what you need to do between the depth map and displaying it on the matrix
def test2():
    img = cv2.imread("../FinalProjectTemp/images/stereoLeft/imageL0.png")
    cv2.imshow("Image", img)

    corners = getBoundaryCorners(img)
    cropped_img = cropDepthMap(img, corners)
    cv2.imshow("Cropped Image", cropped_img)

    print("Press any key to exit")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def findArZone(img, depth_map) :
    corners = getBoundaryCorners(img)
    if corners == None:
        return depth_map, False
    return cropDepthMap(depth_map, corners), True
    



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
    generateARMarker(3)
