import numpy as np
from PIL import Image
import math

#WINDOW_HEIGHT = 512
#WINDOW_WIDTH = WINDOW_HEIGHT*2
WINDOW_HEIGHT = 3072
WINDOW_WIDTH = int(1.8*WINDOW_HEIGHT)

ORIGIN = (int(WINDOW_HEIGHT/2), int(WINDOW_WIDTH/2))

# Y range (-1, 1)
# X Range (-2, 2)
SCALE = 2.5/WINDOW_HEIGHT

MAX_MAGNITUDE = 5
POINT_RADIUS = 4

LIGHT_BLUE = (205, 255, 255)
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
RED = (255, 51, 51)
DARK_BLUE = (0, 0, 139)


class Imaginary:
    def __init__(self, a, b):
        self.real = a
        self.imaginary = b

    def getReal(self):
        return self.real

    def setReal(self, n):
        self.real = n

    def getImg(self):
        return self.imaginary

    def setImg(self, n):
        self.imaginary = n

    def getCords(self):
        return self.real, self.imaginary

    def getPosition(self):
        return int(ORIGIN[0] + (self.real * UP_SCALE)), int(ORIGIN[1] - (self.imaginary * UP_SCALE))

    def magnitude(self):
        # Distance = sqrt(real**2 + imaginary**2)
        return math.sqrt(self.real ** 2 + self.imaginary ** 2)

    @staticmethod
    def square(n):
        first = n.getReal() ** 2
        img_part = 2 * n.getReal() * n.getImg()
        last = (n.getImg() ** 2) * -1

        return Imaginary(first + last, img_part)

    @staticmethod
    def add(n1, n2):
        return Imaginary(n1.getReal() + n2.getReal(), n1.getImg() + n2.getImg())

    @staticmethod
    def px_to_scale(x, y):
        return

    def to_string(self):
        if self.imaginary < 0:
            return str(self.real) + ' - ' + str(abs(self.imaginary)) + 'i'


def is_bounded(point_lst):
    '''Takes in a list of Imaginary numbers and determines
    if the series is bounded or if it grows arbitrarily large'''
    if point_lst[-1].magnitude() < 2:
        return True
    else:
        return False


def to_cords(r, c):
    px_adjusted = (ORIGIN[0] - r, -1*(ORIGIN[1] - c))
    return px_adjusted[0]*SCALE, px_adjusted[1]*SCALE


points = []
constant = Imaginary(0, 0)
zero = Imaginary(0, 0)
current = Imaginary(0, 0)

# FORMAT: [y value, x value]
#         np.zeros(y range, x range, 3 for RGB)
data = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

counter = 0
unbounded = False
for y in range(WINDOW_HEIGHT):
    for x in range(WINDOW_WIDTH):
        counter = 0
        unbounded = False
        current.setImg(0)
        current.setReal(0)

        cords = to_cords(y, x)

        constant.setImg(cords[0])
        constant.setReal(cords[1])

        while counter < 30 and not unbounded:
            current = Imaginary.add(Imaginary.square(current), constant)
            if current.magnitude() >= MAX_MAGNITUDE:
                unbounded = True
            counter += 1

        if unbounded:
            if counter <= 7:
                data[y, x] = [0, 0, 0]
            elif counter <= 9:
                data[y, x] = [0, 0, 153]
            elif counter <= 11:
                data[y, x] = [0, 0, 200]
            else:
                data[y, x] = [0, 0, 255]
        else:
            data[y, x] = [205, 255, 255]

        print(cords)

image = Image.fromarray(data)
image.show()
image.save("mandelbrot_plot_3072.png")

