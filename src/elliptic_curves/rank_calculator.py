from math import ceil, floor, gcd, log

from sympy import Rational as R
from sympy import primerange

from ..utils.rational_integers import (remove_square_factors_of,
                                       square_free_divisors_of)
from .elliptic_curve import EllipticCurve, SingularCurveError
from .point import O, Point


def exists_solution_mod_p_to(p: int, a: int, b_1: int, b_2: int) -> bool:
    """
    Tries to check if there exists an integer solution (M, N, e) to the
    diophantine equation N^2 = b_1 M^4 + a M^2 e^2 + b_2 e^4 in the field Z/pZ.
    The corresponding solutions in the integers (if they exist) must be such that
    (M, N, e) are pairwise coprime. This means, in Z/pZ, that only one of these
    three can be zero at the same time.
    """
    # We may assume M, N, e coprime in Z, so at most one can be zero
    for M in range(p):
        for N in range(p):
            if M == 0 and N == 0:
                continue
            for e in range(p):
                if e == 0 and (M == 0 or N == 0):
                    continue
                if (N**2) % p == (b_1 * M**4 + a * M**2 * e**2 + b_2 * e**4) % p:
                    return True
    return False


def exists_valid_solution_to(a: int, b_1: int, b_2: int) -> tuple[int, int, int] | None:
    """
    Tries to check if there exists an integer solution (M, N, e) to the
    diophantine equation N^2 = b_1 M^4 + a M^2 e^2 + b_2 e^4 such that
    the following relations hold:
    - gcd(M, e) = gcd(N, e) = gcd(M, N) = gcd(b_1, e) = gcd(b_2, M) = 1

    If it exists, returns the solution. If it doesn't exist, returns
    None. If it's inconclusive, raises TimeoutError.
    """
    # print(f"Checking for b_1 = {b_1} and b_2 = {b_2}")
    if b_1 <= 0 and a <= 0 and b_2 <= 0:
        # No solutions in the reals!
        return None
    for e in range(-100, 100, 1):
        if e == 0:
            continue
        for M in range(-100, 100, 1):
            for N in range(-100, 100, 1):
                if N**2 == b_1 * M**4 + a * M**2 * e**2 + b_2 * e**4:
                    return (M, N, e)
    # Checking if solution DOESN'T exist mod p
    for p in primerange(0, 1000):
        if not exists_solution_mod_p_to(p, a, b_1, b_2):
            # There is no solution mod p!
            return None
    raise TimeoutError(
        f":( Unable to determine if solution exists to equation N^2 = {b_1}M^4 + {a}M^2e^2 + {b_2}e^4."
    )


def image_of_alpha(a: int, b: int) -> tuple[dict[Point, int], int]:
    """
    Tries to calculate all elements in the image of the map
    alpha, whose domain are the points on the elliptic
    curve E : y^2 = x^3 + ax^2 + bx.

    Returns a tuple (D, s). D is a dictionary of pairs
    {point: value} where alpha(point) = value. The value
    s is an upper bound for the size of the image (based
    on the number of equations whose solution was not found).
    """
    points_on_image: dict[Point, int] = {O: 1}
    missed_points = 0
    b_no_squares = remove_square_factors_of(b)
    if b_no_squares not in points_on_image.values():
        points_on_image[Point((R(0), R(0)))] = b_no_squares
    candidates_for_image = square_free_divisors_of(b)
    for b_1 in candidates_for_image:
        b_2 = b // b_1
        try:
            if solution := exists_valid_solution_to(a, b_1, b_2):
                M, N, e = solution
                point = Point((R(b_1 * M**2, e**2), R(b_1 * M * N, e**3)))
                if b_1 not in points_on_image.values():
                    points_on_image[point] = b_1
        except:
            missed_points += 1
    return points_on_image, len(points_on_image) + missed_points


def calculate_rank(curve: EllipticCurve) -> tuple[int, int]:
    """
    Tries to calculate the rank of the
    elliptic curve E : y² = x³ + ax² + bx.

    Returns (R, S) where R is a lower-bound for
    the rank and S is an upper-bound.
    """
    assert curve.c == 0
    a, b = curve.a, curve.b
    image_1, bound_1 = image_of_alpha(a, b)
    image_2, bound_2 = image_of_alpha(-2 * a, a**2 - 4 * b)
    print(f"Image of alpha ({f"found {len(image_1)}, max {bound_1}"}):\t{image_1}")
    print(f"Image of alpha bar ({f"found {len(image_2)}, max {bound_2}"}):\t{image_2}")
    lower_bound = log(len(image_1), 2) + log(len(image_2), 2) - 2
    upper_bound = log(bound_1, 2) + log(bound_2, 2) - 2
    print(f"Rank is in [{round(lower_bound, 2)}, {round(upper_bound, 2)}].")
    return ceil(lower_bound), floor(upper_bound)
