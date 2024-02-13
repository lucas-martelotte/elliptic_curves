from math import floor, sqrt


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


def square_divisors_of(n: int) -> set[int]:
    """
    Returns all divisors d of n such
    that d^2 still divides n.
    """
    n = abs(n)
    divisors: set[int] = {1}
    root = sqrt(n)
    if int(root) == root:
        divisors.add(int(root))
    for m in range(2, floor(sqrt(n)) + 1, 1):
        if n % m**2 == 0:
            divisors.add(m)
    return divisors.union({-x for x in divisors})


def is_square_free(n: int) -> bool:
    """Checks if n is a square-free integer"""
    return square_divisors_of(n) == {1, -1}


def square_free_divisors_of(n: int) -> set[int]:
    """Returns all square-free divisors of n"""
    divisors = divisors_of(n)
    return set(d for d in divisors if is_square_free(d))


def remove_square_factors_of(n: int) -> int:
    for d in range(2, abs(n), 1):
        while n % d**2 == 0:
            n = n // (d**2)
    return n


def roots_of(a: int, b: int, c: int, d: int) -> set[int]:
    """
    Returns all integer roots of ax^3 + bx^2 + cx + d = 0
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
