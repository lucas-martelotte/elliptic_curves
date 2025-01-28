from math import floor, sqrt

import numpy as np
from sympy import factorint


def is_square(n: int) -> bool:
    """Checks if n is a square number"""
    if n < 0:
        return False
    return sqrt(n).is_integer()


def divisors_of(n: int) -> set[int]:
    """Returns all divisors of n"""
    n = abs(n)
    divisors: set[int] = {1, n}
    root = sqrt(n)
    if int(root) == root:
        divisors.add(int(root))
    for m in range(2, floor(sqrt(n)) + 1, 1):
        if n % m == 0:
            divisors.add(m)
            divisors.add(n // m)
    return divisors.union({-x for x in divisors})


def fourth_power_divisors_of(n: int) -> set[int]:
    """
    Returns all divisors d of n such
    that d^4 still divides n.
    """
    n = abs(n)
    divisors: set[int] = {1}
    root = sqrt(sqrt(n))
    if int(root) == root:
        divisors.add(int(root))
    for m in range(2, floor(root) + 1, 1):
        if n % m**4 == 0:
            divisors.add(m)
    return divisors.union({-x for x in divisors})


def square_divisors_of(n: int) -> set[int]:
    """
    Returns all divisors d of n such
    that d² still divides n.
    """
    n = abs(n)
    divisors: set[int] = {1}
    root = sqrt(n)
    if int(root) == root:
        divisors.add(int(root))
    for m in range(2, floor(root) + 1, 1):
        if n % m**2 == 0:
            divisors.add(m)
    return divisors.union({-x for x in divisors})


def is_square_free(n: int) -> bool:
    """Checks if n is a square-free integer"""
    return square_divisors_of(n) == {1, -1}


def is_fourth_power_free(n: int) -> bool:
    """Checks if n is a fourth-power-free integer"""
    return fourth_power_divisors_of(n) == {1, -1}


def square_free_divisors_of(n: int) -> set[int]:
    """Returns all square-free divisors of n"""
    divisors = divisors_of(n)
    return set(d for d in divisors if is_square_free(d))


def remove_square_factors_of(n: int) -> int:
    """Returns n without any square factors"""
    for d in range(2, abs(n), 1):
        while n % d**2 == 0:
            n = n // (d**2)
    return n


def roots_of(a: int, b: int, c: int, d: int) -> set[int]:
    """
    Returns all integer roots of ax³ + bx² + cx + d = 0
    Makes use of Gauss' Lemma to reduce the number of
    cases to check.
    """
    roots: set[int] = set()
    if d == 0:
        return roots_of(0, a, b, c).union({0})
    for x in divisors_of(abs(d)).union({0}):
        if a * x**3 + b * x**2 + c * x + d == 0:
            roots.add(x)
    return roots


def radical(a: int) -> int:
    """
    Returns the radical of a, i.e. the product of all
    primes dividing a.
    """
    prime_factors = list(factorint(a).keys())
    output = np.prod(prime_factors)
    assert output.is_integer()
    return int(output)
