"""
Given an elliptic curve E : y² = x³ + ax² + bx + c, with a, b, c integers and
a good prime p, we call E_p the reduction modulo of E modulo p. Hasse's Theorem
on Elliptic Curves tells us that the number of points in E_p is given by
    #E_p = p + 1 - pi - conjugate(pi),
where pi is a complex number which depends on E and p and satisfies N(pi) = p.
Thanks to the last condition, pi is unique up to complex conjugation and we 
can calculate it simply by knowing #E_p.

------------------------------------------------------------------------------
Theorem: Given pi, chosen so that it lies on the upper-half plane, there are
integers p, q such that one of the following hold.

1. pi = p + sqrt(q)i,
2. pi = (p + sqrt(q)i)/2, with p odd and q = 4k+3.
------------------------------------------------------------------------------

This application calculates pi, p and q for a large amount of good primes in 
ascending order and draws on the screen a path passing through all the points pi.
"""

from math import sqrt
from pprint import pprint

import pygame
from sympy import primerange

from src.elliptic_curves import EllipticCurve
from src.elliptic_curves.counting_points_mod_p import (
    count_points_mod_p_naive_weierstrass_form,
)

# ==================== APP CONFIG ======================= #

pygame.init()
zoom = 50
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
pygame.font.init()

# ======================================================= #

e = EllipticCurve(0, -1, -112)
max_prime = 500

good_primes = [p for p in primerange(max_prime) if e.discriminant % p != 0 and p > 5]
n_solutions = {  # number of solutions of good prime reduction
    p: len(count_points_mod_p_naive_weierstrass_form(e, p)) for p in good_primes
}
correction_terms: dict[int, tuple[float, float]] = {}
for p, solutions_mod_p in n_solutions.items():
    real_part = (p + 1 - solutions_mod_p) / 2
    imag_part = sqrt(p - real_part**2)
    correction_terms[p] = (real_part, imag_part)

lattice_points: dict[int, tuple[float, float, str]] = {}
for p, term in correction_terms.items():
    if term[0].is_integer():
        assert round(term[1] ** 2, 2).is_integer()
        lattice_points[p] = (int(term[0]), int(term[1] ** 2), "not")
    else:
        assert round((2 * term[1]) ** 2, 2).is_integer()
        assert round(2 * term[0], 2).is_integer()
        lattice_points[p] = (int(2 * term[0]), int((2 * term[1]) ** 2), "divided")

# print(len([t for t in lattice_points.values() if t[2] == "not"]) / len(lattice_points))
# pprint(lattice_points)
# exit()

# Drawing the tree
screen.fill((255, 255, 255))
font = pygame.font.SysFont("Verdana", 32)
text = str(e).replace("^3", "³").replace("^2", "²")
text_sfc = font.render(text, True, (0, 0, 0))
screen.blit(text_sfc, (10, 10))

for i in range(len(good_primes) - 1):
    term_start = correction_terms[good_primes[i]]
    term_end = correction_terms[good_primes[i + 1]]
    line_start = (width // 2 + term_start[0] * zoom, height - term_start[1] * zoom)
    line_end = (width // 2 + term_end[0] * zoom, height - term_end[1] * zoom)
    pygame.draw.line(
        screen,
        (int(255 - i * 255 / (len(good_primes) - 2)), 0, 0),
        line_start,
        line_end,
        width=2,
    )

pygame.display.update()

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            prev_mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            drag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pass
