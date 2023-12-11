import board
from neopixel import NeoPixel
import cv2


class LedMatrix:
    def __init__(   self,
                    led_data,
                    dim: tuple[int, int] = (16, 16),
                    brightness = 0.025,
                    colorCorrect=True):
        self.pixels = NeoPixel( pin=board.D18, 
                                n=dim[0] * dim[1],
                                brightness=brightness,
                                auto_write=False)
        self.led_data = led_data
        self.colorCorrect = colorCorrect


    def display(self):
        # display is BGR
        if self.colorCorrect:
            self.led_data = self.__doColorCorrect()

        # display has alternating indexing on the rows
        for row in range(0, len(self.led_data), 2):
            self.led_data[row] = self.led_data[row][::-1]

        # write each pixel
        for row in range(len(self.led_data)):
            for col in range(len(self.led_data[row])):
                self.pixels[col + len(self.led_data[row]) * row] = tuple(self.led_data[row][col][colorVal] for colorVal in range(3))
        self.pixels.show()


    def __doColorCorrect(self):
        return self.led_data[..., ::-1]


if __name__ == "__main__":
    amogus = cv2.imread("./images/led_matrix_hardware_demo/crewmate_2.png")
    amogus_res = cv2.resize(amogus, dsize=(16, 16), interpolation=cv2.INTER_NEAREST  )
    
    LedMatrix(amogus_res, colorCorrect=False).display()
