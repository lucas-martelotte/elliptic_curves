from math import cos, sin, sqrt
from typing import Tuple

import pygame
from sympy import symbols

from src.elliptic_curves import EllipticCurve, SingularCurveError
from src.utils.rational_integers import divisors_of, square_free_divisors_of

pygame.init()
pygame.display.set_caption("Torsion Group Graph")

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

GROUP_TO_COLOR = {
    "0": (0, 0, 0),  # BLACK
    "Z2": (0, 0, 255),  # DARK BLUE
    "Z3": (0, 238, 255),  # LIGHT BLUE
    "Z4": (5, 237, 28),  # GREEN
    "Z5": (148, 5, 250),  # PURPLE
    "Z6": (216, 161, 255),  # LILAC
    "Z7": (0, 150, 136),  # teal
    "Z8": (103, 58, 183),  # deep purple
    "Z9": (200, 200, 200),  # gray
    "Z10": (232, 30, 99),  # pink
    "Z12": (244, 67, 54),  # red
    "Z2 x Z2": (139, 195, 74),  # light green
    "Z2 x Z4": (255, 235, 59),  # yellow
    "Z2 x Z6": (255, 152, 0),  # orange
    "Z2 x Z8": (255, 87, 34),  # deep orange
}


class Spiral:
    def __init__(self, o_x: int, o_y: int):
        self.o_x, self.o_y = o_x, o_y
        self.step_index = 0
        self.step_direction = 1
        self.step_size = 1

    def next(self) -> Tuple[int, int]:
        point = (self.o_x, self.o_y)
        if self.step_index == 2 * self.step_size:
            self.step_index = 0
            self.step_size += 1
            self.step_direction *= -1
        if self.step_index < self.step_size:
            self.o_x += self.step_direction
        else:
            self.o_y += self.step_direction
        self.step_index += 1
        return point


spiral = Spiral(0, 0)

screen.fill((255, 255, 255))

PIXEL_SIZE = 6

running = True
while running:
    # clock.tick(120)

    pygame.display.update()

    point = spiral.next()
    color = None
    try:
        x, y = point[0], -point[1]
        a, b, c = x, y, 0
        e = EllipticCurve(a, b, c)
        color = GROUP_TO_COLOR[e.torsion_name]
    except Exception:
        color = (255, 255, 255)
    pygame.draw.rect(
        screen,
        color,
        (
            950 + point[0] * PIXEL_SIZE,
            540 + point[1] * PIXEL_SIZE,
            PIXEL_SIZE,
            PIXEL_SIZE,
        ),
    )

    mouse_pos = pygame.mouse.get_pos()
    pixel_pos = (
        (mouse_pos[0] - 950) // PIXEL_SIZE,
        -(mouse_pos[1] - 540) // PIXEL_SIZE,
    )
    font = pygame.font.SysFont("comicsans", 24)
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 300, 100))
    # x, a, b = symbols("x"), pixel_pos[0], pixel_pos[1]
    # eq = x**3 + a * x**2 + b * x + c
    # eq_str = "y² = " + str(eq).replace("**3", "³").replace("**2", "²").replace("*", "")
    text_sfc = font.render(str(pixel_pos), False, (0, 0, 0))
    screen.blit(text_sfc, (5, 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
