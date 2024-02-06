from typing import Tuple, Union, Literal, Optional, List, Set
from .elliptic_curve import EllipticCurve, Point
from math import sqrt, floor
import sympy


def divisors_of(n: int) -> Set[int]:
    """Returns all divisors of n"""
    n = abs(n)
    divisors: Set[int] = {1, n}
    root = sqrt(n)
    if int(root) == root:
        divisors.add(int(root))
    for m in range(2, floor(sqrt(n)) + 1, 1):
        if n % m == 0:
            divisors.add(m)
            divisors.add(n // m)
    return divisors.union({-x for x in divisors})


def roots_of(a: int, b: int, c: int, d: int) -> Set[int]:
    """Returns all integer roots of ax^3 + bx^2 + cx + d = 0
    Makes use of Gauss' Lemma to reduce the number of
    cases to check.
    """
    roots: Set[int] = set()
    if d == 0:
        return roots_of(0, a, b, c).union({0})
    for x in divisors_of(abs(d)).union({0}):
        if a * x**3 + b * x**2 + c * x + d == 0:
            roots.add(x)
    return roots


def get_order_of(e: EllipticCurve, p: Point) -> Optional[int]:
    """Returns the order of p. It assumes p is a point in the curve.
    If the point has infinite order, returns None.
    """
    current_point, order = p, 1
    while not current_point.is_neutral_element():
        # print(f"\t{current_point}")
        if order > 12 or not current_point.is_integer():
            # print("Infinit order.")
            return None
        current_point = e.sum(current_point, p)
        order += 1
    # print(f"Order: {order}")
    return order


def determine_group_based_on_orders(orders: List[int]) -> str:
    orders = sorted(orders)
    if orders == [1]:
        return "0"
    if orders == [1, 2]:
        return "Z2"
    if orders == [1, 2, 2, 2]:
        return "Z2 x Z2"
    for k in [9, 10, 12]:
        if k in orders:
            return f"Z{k}"
    for k in reversed(list(range(3, 9, 1))):
        if k in orders:
            if len(orders) == k:
                return f"Z{k}"
            elif len(orders) == 2 * k:
                return f"Z2 x Z{k}"
    raise Exception("???")


def calculate_torsion_group(e: EllipticCurve):
    orders: List[int] = [1]  # Starts with O
    for y in sorted(list(divisors_of(e.discriminant).union({0}))):
        # print(y)
        for x in roots_of(1, 0, e.a, e.b - y**2):
            if order := get_order_of(e, Point((sympy.Rational(x), sympy.Rational(y)))):
                orders.append(order)
                continue
    # print(sorted(orders))
    return determine_group_based_on_orders(orders)
