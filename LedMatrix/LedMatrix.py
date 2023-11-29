import board
import time
import neopixel
from neopixel import NeoPixel

import numpy as np
from numpy import ndarray

import cv2
# print(cv2.__version__)

amogus = cv2.imread("amogus2.png")
amogus_res = cv2.resize(amogus, dsize=(16, 16), interpolation=cv2.INTER_NEAREST  )
amogus_res_cc = amogus_res[...,::-1]
# cv2.imshow("amogus", amogus)
# cv2.waitKey(0)
# cv2.imshow("amogus_res", amogus_res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(np.asarray(amogus))

pixels = NeoPixel(  pin=board.D18, 
                    n=256,
                    brightness=0.05,
                    auto_write=False)

# print(len(amogus[0][1]))

# testMatrix = [
#     # black
#     [0, 0, 0],
#     # white
#     [255, 255, 255],
#     # purple 
#     [255, 0, 255], 
#     # red
#     [255, 0, 0], 
#     # green
#     [0, 255, 0], 
#     # blue
#     [0, 0, 255],
#     # yellow
#     [255, 255, 0],
#     # teal
#     [0, 255, 255]
    
# ]

#  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1   0
#  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31

for row in range(0, len(amogus_res_cc), 2):
    # print(f"\n{amogus[row]}", end="")
    amogus_res_cc[row] = amogus_res_cc[row][::-1]
    # print(f"\n{amogus[row]}")
    # print()

# row = 2
# for col in range(len(testMatrix)):
#     pixels[col + 16 * row] = (testMatrix[col][0], testMatrix[col][1], testMatrix[col][2])

for row in range(len(amogus_res_cc)):
    for col in range(len(amogus_res_cc[row])):
#         print(row + col * row
        # print(f"{amogus_res[row][col][0]:3d}{amogus_res[row][col][1]:3d}{amogus_res[row][col][2]:3d} ", end="")
    
        pixels[col + 16 * row] = (amogus_res_cc[row][col][0], amogus_res_cc[row][col][1], amogus_res_cc[row][col][2])
        # print(f"{col + 16 * row:3d} ", end="")
    # print("\n")
pixels.show()
# # pixels[0] = (0, 255, 0)
# # pixels[16] = (255, 0, 0)

# # # set all LEDs to green
# # pixels.fill((0,255,0))



# def colorMatrix(colorMatrix: NeoPixel):
#     testMatrix = np.array([[]])
#     pass



# pixel_pin = board.D18

# # The number of NeoPixels
# num_pixels = 256

# # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
# ORDER = neopixel.GRB

# pixels = neopixel.NeoPixel(
#     pixel_pin, num_pixels, brightness=0.05, auto_write=False, pixel_order=ORDER
# )


# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 0 or pos > 255:
#         r = g = b = 0
#     elif pos < 85:
#         r = int(pos * 3)
#         g = int(255 - pos * 3)
#         b = 0
#     elif pos < 170:
#         pos -= 85
#         r = int(255 - pos * 3)
#         g = 0
#         b = int(pos * 3)
#     else:
#         pos -= 170
#         r = 0
#         g = int(pos * 3)
#         b = int(255 - pos * 3)
#     return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


# def rainbow_cycle(wait):
#     for j in range(255):
#         for i in range(num_pixels):
#             pixel_index = (i * 256 // num_pixels) + j
#             pixels[i] = wheel(pixel_index & 255)
#         pixels.show()
#         time.sleep(wait)


# while True:
#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((255, 0, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((255, 0, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 255, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 255, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 0, 255))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 0, 255, 0))
#     pixels.show()
#     time.sleep(1)

#     rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step