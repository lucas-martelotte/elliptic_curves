from math import gcd, log

from utils.number_theory import remove_square_factors_of, square_free_divisors_of
from utils.primes import FIRST_1000_PRIMES

from .elliptic_curve import SingularCurveError


def exists_solution_mod_p_to(p: int, a: int, b_1: int, b_2: int) -> bool:
    """
    Tries to check if there exists an integer
    solution (M, N, e) to the diophantine equation
        N^2 = b_1 M^4 + a M^2 e^2 + b_2 e^4
    in the field Z/pZ.
    """
    for M in range(p):
        for N in range(p):
            for e in range(p):
                if (N**2) % p == (b_1 * M**4 + a * M**2 * e**2 + b_2 * e**4) % p:
                    return True
    return False


def exists_valid_solution_to(a: int, b_1: int, b_2: int) -> bool:
    """
    Tries to check if there exists an integer
    solution (M, N, e) to the diophantine equation
        N^2 = b_1 M^4 + a M^2 e^2 + b_2 e^4
    such that the following relations hold
        gcd(M, e) = gcd(N, e) = gcd(M, N) =
           gcd(b_1, e) = gcd(b_2, M) = 1
    """
    print(f"Checking for b_1 = {b_1} and b_2 = {b_2}")
    if b_1 <= 0 and a <= 0 and b_2 <= 0:
        print("No solutions in the reals!")
        return False
    # Checking if solution exists
    for M in range(-100, 100, 1):
        for N in range(-100, 100, 1):
            for e in range(-100, 100, 1):
                if (
                    N**2 == b_1 * M**4 + a * M**2 * e**2 + b_2 * e**4
                    and gcd(M, e) == 1
                    and gcd(N, e) == 1
                    and gcd(M, N) == 1
                    and gcd(b_1, e) == 1
                    and gcd(b_2, M) == 1
                ):
                    print(f"Solution: (M, N, e) = {(M, N, e)}.")
                    return True
    # Checking if solution DOESN'T exist mod p
    for p in FIRST_1000_PRIMES:
        if not exists_solution_mod_p_to(p, a, b_1, b_2):
            print(f"There is no solution mod {p}.")
            return False
    raise TimeoutError("Unable to determine if solution exists... :(")


def image_of_alpha(a: int, b: int) -> set[int]:
    """
    Calculates all elements in the image of the map
    alpha, whose domain are the point on the elliptic
    curve E : y^2 = x^3 + ax^2 + bx.
    """
    points_on_image = {1, b}
    candidates_for_image = {
        remove_square_factors_of(d) for d in square_free_divisors_of(b)
    }
    for b_1 in candidates_for_image:
        b_2 = b // b_1
        if exists_valid_solution_to(a, b_1, b_2):
            points_on_image.add(b_1)
    return points_on_image


def calculate_rank_of_elliptic_curve(a: int, b: int) -> int:
    """
    Tries to calculate the rank of the
    elliptic curve E : y^2 = x^3 + ax^2 + bx.
    """
    if b**2 * a**2 - 4 * b**3 == 0:
        raise SingularCurveError()
    image_1 = image_of_alpha(a, b)
    image_2 = image_of_alpha(-2 * a, a**2 - 4 * b)
    return int(log(len(image_1), 2) + log(len(image_2), 2) - 2)
