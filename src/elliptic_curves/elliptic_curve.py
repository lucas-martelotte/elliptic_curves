"""
This module implements the class EllipticCurve, which represents an elliptic
curve in weierstrass form E : y² = x³ + ax² + bx + c with a, b, c integers.
Amongst other things, it implements the group operation and a calculation
of the torsion subgroup based on Nagell-Lutz and Mazur's theorems.
"""

from sympy import Rational as R
from sympy import symbols

from .point import O, Point


class SingularCurveError(Exception):
    pass


class EllipticCurve:
    def __init__(self, a: int, b: int, c: int):
        """
        Creates an ellptic curve given by: y² = x³ + ax² + bx + c.
        The discriminant is -4a³c + a²b² + 18abc -4b³ -27c².
        """
        self.a, self.b, self.c = a, b, c
        self.discriminant = (
            -4 * a**3 * c + a**2 * b**2 + 18 * a * b * c - 4 * b**3 - 27 * c**2
        )
        if self.discriminant == 0:
            raise SingularCurveError("Invalid coefficients for the elliptic curve!")
        self._has_point_of_infinite_order: bool | None = None
        self._torsionpoint2order: dict[Point, int] | None = None
        self._torsion_name: str | None = None

    def is_on_the_curve(self, p: Point) -> bool:
        """Checks if a given point lies inside the curve"""
        if p.is_neutral_element():
            return True
        x, y, a, b, c = p.x, p.y, self.a, self.b, self.c
        return y**2 == x**3 + a * x**2 + b * x + c

    def inv(self, p: Point) -> Point:
        """Calculates the inverse of p"""
        if p.is_neutral_element():
            return O
        return Point((p.x, -p.y))

    def add(self, p_1: Point, p_2: Point) -> Point:
        """Operates the points p_1 and p_2"""
        assert self.is_on_the_curve(p_1)
        assert self.is_on_the_curve(p_2)
        if p_1.is_neutral_element():
            return p_2
        if p_2.is_neutral_element():
            return p_1
        if p_1 == self.inv(p_2):
            return O
        x1, y1, x2, y2 = p_1.x, p_1.y, p_2.x, p_2.y
        a, b, c = self.a, self.b, self.c
        slope = (
            (y2 - y1) / (x2 - x1)
            if p_1 != p_2
            else (3 * x1**2 + 2 * a * x1 + b) / (2 * p_1.y)
        )
        x3 = slope**2 - a - x1 - x2
        offset = y1 - slope * x1
        y3 = -(slope * x3 + offset)
        return Point((x3, y3))

    def __str__(self):
        x, y = symbols("x, y")
        exp = x**3 + self.a * x**2 + self.b * x + self.c
        exp_str = str(exp).replace("**2", "^2").replace("**3", "^3").replace("*", "")
        return f"E : y^2 = {exp_str}"

    def get_order_of(self, p: Point) -> int | None:
        """
        Returns the order of p. By Mazur's theorem, the
        greatest possible (finite) order is 12.
        It assumes p is a point in the curve.
        If the point has infinite order, returns None.
        """
        assert self.is_on_the_curve(p)
        current_point, order = p, 1
        while not current_point.is_neutral_element():
            if order > 12 or not current_point.is_integer():
                # Found infinite order point
                self._has_point_of_infinite_order = True
                return None
            current_point = self.add(current_point, p)
            order += 1
        return order

    def _calculate_torsionpoint2order(self) -> dict[Point, int]:
        """
        Implements the algorithm induced by the Nagell-Lutz
        theorem. Computes all finite order elements and returns
        a dictionary {element: order}.
        """
        from ..utils import roots_of, square_divisors_of

        point2order: dict[Point, int] = {O: 1}
        a, b, c = self.a, self.b, self.c
        for y in sorted([0] + list(square_divisors_of(self.discriminant))):
            for x in roots_of(1, a, b, c - y**2):
                candidate = Point((R(x), R(y)))
                if order := self.get_order_of(candidate):
                    point2order[candidate] = order
                    continue
        return point2order

    def _calculate_torsion_name(self) -> str:
        """
        Receives the full list of orders of the group as input
        and determines which group it is among the 15 possibilies
        of torsion subgroup in Mazur's classification Theorem.
        """
        orders = sorted(list(self.torsionpoint2order.values()))
        if orders == [1]:
            return "0"
        if orders == [1, 2]:
            return "Z2"
        if orders == [1, 2, 2, 2]:
            return "Z2xZ2"
        for k in [9, 10, 12]:
            if k in orders:
                return f"Z{k}"
        for k in reversed(list(range(3, 9, 1))):
            if k in orders:
                if len(orders) == k:
                    return f"Z{k}"
                elif len(orders) == 2 * k:
                    return f"Z2xZ{k}"
        raise Exception()

    @property
    def torsionpoint2order(self) -> dict[Point, int]:
        if self._torsionpoint2order is None:
            self._torsionpoint2order = self._calculate_torsionpoint2order()
        return self._torsionpoint2order

    @property
    def torsion(self) -> set[Point]:
        return set(self.torsionpoint2order.keys())

    @property
    def torsion_name(self) -> str:
        if not self._torsion_name:
            self._torsion_name = self._calculate_torsion_name()
        return self._torsion_name

    def has_non_zero_rank(self) -> bool | None:
        """
        Returns True if a point of infinite order was found,
        otherwise returns None for inconclusive.
        """
        return self._has_point_of_infinite_order

    def all_points_of_order(self, order: int) -> set[Point]:
        """Returns all points whose order is exactly the input"""
        return {p for p, o in self.torsionpoint2order.items() if o == order}

    def has_point_of_order(self, order: int) -> bool:
        """Returns if there exists a point of a given finite order"""
        return order in self.torsionpoint2order.values()
