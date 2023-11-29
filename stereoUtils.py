import cv2
import numpy as np

paramsFile = cv2.FileStorage()
paramsFile.open('webcamStereoMap.xml', cv2.FileStorage_READ)

stMapLX = paramsFile.getNode('webcamStereoMapLX').mat()
stMapLY = paramsFile.getNode('webcamStereoMapLY').mat()
stMapRX = paramsFile.getNode('webcamStereoMapRX').mat()
stMapRY = paramsFile.getNode('webcamStereoMapRY').mat()

def undistortRectify(r, l):
    uL = cv2.remap(l, stMapLX, stMapLY, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    uR = cv2.remap(r, stMapRX, stMapRY, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    return uR, uL

