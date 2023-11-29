import board
import time
import neopixel
from neopixel import NeoPixel

import numpy as np
from numpy import ndarray

import cv2


def displayAmogus(pixels: NeoPixel):
    amogus = cv2.imread("amogus.png")
    amogus_res = cv2.resize(amogus, dsize=(16, 16), interpolation=cv2.INTER_NEAREST  )
    amogus_res_cc = amogus_res[..., ::-1]

    # display has alternating indexing on the rows
    for row in range(0, len(amogus_res_cc), 2):
        amogus_res_cc[row] = amogus_res_cc[row][::-1]


    for row in range(len(amogus_res_cc)):
        for col in range(len(amogus_res_cc[row])):
            pixels[col + 16 * row] = (amogus_res_cc[row][col][0], amogus_res_cc[row][col][1], amogus_res_cc[row][col][2])
    pixels.show()


def videoStreamDemo(pixels: NeoPixel):
    vid = cv2.VideoCapture(0)

    while(True):
        ret, frame = vid.read()

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        if input() == 'q': 
            break

        vid_res = cv2.resize(frame, dsize=(16, 16), interpolation=cv2.INTER_NEAREST)
        vid_res_cc = vid_res[..., ::-1]

        for row in range(0, len(vid_res_cc), 2):
            vid_res_cc[row] = vid_res_cc[row][::-1]

        for row in range(len(vid_res_cc)):
            for col in range(len(vid_res_cc[row])):
                pixels[col + 16 * row] = (vid_res_cc[row][col][0], vid_res_cc[row][col][1], vid_res_cc[row][col][2])
        pixels.show()


    vid.release() 


if __name__ == "__main__":
    pixels = NeoPixel(  pin=board.D18, 
                        n=256,
                        brightness=0.05,
                        auto_write=False)
    
    displayAmogus(pixels)
    # videoStreamDemo(pixels)
