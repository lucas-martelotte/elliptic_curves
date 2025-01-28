from math import cos, sin, sqrt
from typing import Tuple

import pygame
from sympy import symbols

from src.elliptic_curves import EllipticCurve, SingularCurveError
from src.elliptic_curves.counting_points_mod_p import (
    count_points_mod_p_naive_weierstrass_form,
)
from src.utils.rational_integers import divisors_of, square_free_divisors_of

pygame.init()
pygame.display.set_caption("Torsion Group Graph")

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()


def correction_term_is_of_first_type(e: EllipticCurve, p: int) -> bool:
    solutions = count_points_mod_p_naive_weierstrass_form(e, p)
    return (p + 1 - len(solutions)) % 2 == 0


class Square:
    def __init__(self, size: int, o_x: int, o_y: int):
        self.o_x, self.o_y = o_x - size // 2, o_y - size // 2
        self.size = size
        self.step_index = 0
        self.step_size = 1

    def next(self) -> Tuple[int, int]:
        if self.step_index >= self.size**2:
            raise Exception()
        point = (self.o_x, self.o_y)
        self.step_index += 1
        if self.step_index % self.size == 0:
            self.o_y += 1
            self.o_x -= self.size - 1
        else:
            self.o_x += 1
        return point


screen.fill((0, 0, 0))
PIXEL_SIZE = 6
PRIME = 91
square = Square(PRIME, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # clock.tick(120)
    pygame.display.update()
    try:
        point = square.next()
    except:
        continue
    color = None
    try:
        x, y = point[0], -point[1]
        a, b, c = x, y, x + y
        e = EllipticCurve(a, b, c)
        if e.discriminant % PRIME == 0:
            color = (255, 0, 0)  # Red
        else:
            color = (
                (0, 0, 255)  # Blue
                if correction_term_is_of_first_type(e, PRIME)
                else (0, 0, 0)  # Green
            )
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
