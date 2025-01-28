from typing import Literal

from sympy import Rational as R
from sympy import fraction, primerange

from .elliptic_curve import EllipticCurve


class RecursiveNumbers:
    def __init__(self, index_4: R, index_6: R) -> None:
        self.found_numbers: dict[int, R] = {4: index_4, 6: index_6}

    def find(self, index: int) -> R:
        if index % 2 != 0:  # Odd index is always zero
            return R(0, 1)
        if index in self.found_numbers:
            return self.found_numbers[index]
        sum = R(0, 1)
        # print(f"index = {index}")
        for i in range(4, index - 4 + 1, 2):
            # print((i, index - i))
            sum += self.find(i) * self.find(index - i)
        curr_number = 12 * sum / ((index + 5) * (index - 2))
        self.found_numbers[index] = curr_number
        return curr_number


class FNumbers(RecursiveNumbers):
    def __init__(self, t2: int, t3: int):
        super().__init__(index_4=R(t2, 40), index_6=R(t3, 56))


class ModifiedBernoulliNumbers(RecursiveNumbers):
    def __init__(self):
        super().__init__(index_4=R(1, 240 * 2), index_6=-R(1, 504 * 24))


def count_points_mod_p(t2: int, t3: int, max_prime: int) -> dict[int, int]:
    """
    Returns a dictionary where the key is a prime and
    the value is the number of points in the elliptic curve
                    E : y² = 4x³ -t2x -t3
    reduced modulo p. The function checks primes up to n_primes.
    """
    bn, fn = ModifiedBernoulliNumbers(), FNumbers(t2, t3)
    count: dict[int, int] = {}
    for p in primerange(19, max_prime):
        num, den = fraction(fn.find(p - 1) / bn.find(p - 1))
        # print((num, den))
        num, den = num % p, den % p
        # print((num, den))
        a_p = (num * pow(den, -1, p)) % p
        if a_p > (p - 1) // 2:
            a_p -= p
        count[p] = p + 1 - a_p
    return count


def count_points_mod_p_naive(t2: int, t3: int, p: int) -> set[tuple[int, int]]:
    """
    Finds all solutions mod p to
    the equation E : y² = 4x³ -t2x -t3.
    """
    solutions: set[tuple[int, int]] = set()
    for x in range(p):
        for y in range(p):
            if (4 * pow(x, 3, p) - t2 * x - t3 - pow(y, 2, p)) % p == 0:
                solutions.add((x, y))
    return solutions


def count_points_mod_p_naive_weierstrass_form(
    e: EllipticCurve, p: int
) -> set[tuple[int, int] | Literal["O"]]:
    """
    Finds all solutions mod p to the equation E : y² = x³ + ax² + bx + c
    including the point at infinity.
    """
    solutions: set[tuple[int, int] | Literal["O"]] = {"O"}
    for x in range(p):
        for y in range(p):
            if (
                pow(x, 3, p) + e.a * pow(x, 2, p) + e.b * x + e.c - pow(y, 2, p)
            ) % p == 0:
                solutions.add((x, y))
    return solutions
