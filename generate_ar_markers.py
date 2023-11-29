import cv2
import numpy as np

AR_MARKER_DICTIONARY = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
AR_MARKER_SIZE = 300



def generateARMarker(id):
    dictionary = AR_MARKER_DICTIONARY
    marker0 = np.zeros((AR_MARKER_SIZE, AR_MARKER_SIZE, 1), dtype="uint8")
    cv2.aruco.generateImageMarker(dictionary, id, AR_MARKER_SIZE, marker0, 1)
    cv2.imwrite("images/ar_markers/marker{}.png".format(id), marker0)


def getRelativePoseCameraToWorld():
    pass


if __name__ == "__main__":
    generateARMarker(0)
    generateARMarker(1)
    generateARMarker(2)
