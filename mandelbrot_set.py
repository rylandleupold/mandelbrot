import math
import pygame

WINDOW_HEIGHT = 640
WINDOW_WIDTH = int(1.8*WINDOW_HEIGHT)
# px 100-700 for image width
# px 100-500 for image height
ORIGIN = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))

UP_SCALE = (WINDOW_HEIGHT / 2.5)
DOWN_SCALE = 1 / UP_SCALE

MAX_MAGNITUDE = 30
NUM_POINTS = 70
POINT_RADIUS = 4
CONTAINER_RADIUS = int(WINDOW_HEIGHT/2 - 100)
CLINE_RADIUS = 1

LIGHT_BLUE = (205, 255, 255)
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
RED = (255, 51, 51)
DARK_BLUE = (0, 0, 139)
WHITE = (255, 255, 255)


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
        return math.sqrt(self.real**2 + self.imaginary**2)

    @staticmethod
    def square(n):
        first = n.getReal()**2
        img_part = 2 * n.getReal() * n.getImg()
        last = (n.getImg()**2) * -1

        return Imaginary(first + last, img_part)

    @staticmethod
    def add(n1, n2):
        return Imaginary(n1.getReal() + n2.getReal(), n1.getImg() + n2.getImg())

    def to_string(self):
        if self.imaginary < 0:
            return str(self.real) + ' - ' + str(abs(self.imaginary)) + 'i'


def update_points(mouse_pos):
    mouse_pos = (DOWN_SCALE * (mouse_pos[0] - ORIGIN[0]), DOWN_SCALE * (ORIGIN[1] - mouse_pos[1]))

    points.clear()
    points.append(Imaginary(0, 0))
    c.setReal(mouse_pos[0])
    c.setImg(mouse_pos[1])
    points.append(c)

    for i in range(1, NUM_POINTS):
        if Imaginary.add(Imaginary.square(points[i]), c).magnitude() <= MAX_MAGNITUDE:
            points.append(Imaginary.add(Imaginary.square(points[i]), c))
        else:
            break


def is_bounded(point_lst):
    '''Takes in a list of Imaginary numbers and determines
    if the series is bounded or if it grows arbitrarily large'''
    if point_lst[-1].magnitude() < 2:
        return True
    else:
        return False


def draw_points(surface):
    pygame.draw.circle(surface, WHITE, ORIGIN, CONTAINER_RADIUS, 2)

    for i in range(len(points) - 1):
        pygame.draw.line(surface, GREY, points[i].getPosition(), points[i + 1].getPosition())

    if is_bounded(points):
        pygame.draw.circle(surface, DARK_BLUE, c.getPosition(), POINT_RADIUS)
        for circle in points:
            pygame.draw.circle(surface, DARK_BLUE, circle.getPosition(), POINT_RADIUS, CLINE_RADIUS)
    else:
        pygame.draw.circle(surface, RED, c.getPosition(), POINT_RADIUS)
        for circle in points:
            pygame.draw.circle(surface, RED, circle.getPosition(), POINT_RADIUS, CLINE_RADIUS)


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pygame.image.load("mandelbrot_plot.png")
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont('arial', 20)

done = False
points = []
c = Imaginary(0, 0)
cord_text = ""

while not done:
    screen.fill(LIGHT_BLUE)
    screen.blit(background, [0, 0])

    cursor_pos = pygame.mouse.get_pos()
    cord_text = font.render(str(round(DOWN_SCALE*(cursor_pos[0]-ORIGIN[0]), 4)) + " + " + str(round(DOWN_SCALE * (ORIGIN[1] - cursor_pos[1]), 4)) + "i",
                            True, WHITE)

    screen.blit(cord_text, (WINDOW_WIDTH//20, WINDOW_HEIGHT//20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    update_points(cursor_pos)
    draw_points(screen)
    pygame.display.flip()











