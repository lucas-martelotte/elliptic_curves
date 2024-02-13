import sympy

from utils.number_theory import roots_of, square_divisors_of

from .elliptic_curve import EllipticCurve, Point


def get_order_of(e: EllipticCurve, p: Point) -> int | None:
    """
    Returns the order of p. It assumes p is a point in the curve.
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


def determine_group_based_on_orders(orders: list[int]) -> str:
    """
    Receives the full list of orders of the group as input
    and determines which group it is among the 15 possibilies
    of torsion subgroup in Mazur's classification Theorem.
    """
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


def calculate_torsion_subgroup(e: EllipticCurve) -> str:
    """Calculates the torsion subgroup of the elliptic curve e"""
    orders: list[int] = [1]  # Starts with O
    for y in sorted(list(square_divisors_of(e.discriminant).union({0}))):
        # print(y)
        for x in roots_of(1, 0, e.a, e.b - y**2):
            if order := get_order_of(e, Point((sympy.Rational(x), sympy.Rational(y)))):
                orders.append(order)
                continue
    # print(sorted(orders))
    return determine_group_based_on_orders(orders)
