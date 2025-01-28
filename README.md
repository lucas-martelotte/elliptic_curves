# Elliptic curve calculator

This repository implements some useful, elementary algorithms with respect to elliptic curves. Let $E(\mathbb{Q})$ be the group of rational points of an elliptic curve and $L(E, s)$ its $L$-function. Currently the following functionalities are available.

- Calculate the torsion subgroup of $E(\mathbb{Q})$,
- Calculate the rank of $E(\mathbb{Q})$,
- Calculate the value of $L(E, 1)$ for elliptic curves of the form $y^2 = x^3 - Dx$, where $D \in \mathbb{Z}$.

## Instalation

First, make sure you have Python 3 installed in your machine and the command pip3 working properly. Clone the repository and open a cmd inside of it. Simply run the following command and you're done.

`pip3 install requirements.txt`

## Basic usage

The repository's most fudamental object is an elliptic curve in Weierstrass form with integers coefficients, i.e.
$$E : y^2 = x^3 + Ax^2, Bx + C, \quad A,B,C \in \mathbb{Z}.$$
To create an elliptic curve, simply run the following.

```python
from src.elliptic_curves import EllipticCurve

A, B, C = 2, -4, 8 # Must be integers!
elliptic_curve = EllipticCurve(A, B, C)
```
If the curve you're trying to create is singular, the constructor will raise an exception. After creating an elliptic curve, there are many operations you can do with it. First, you can check if a rational point belong to the curve or not.

```python
from src.elliptic_curves import Point
from sympy import Rational

p = Point((2, 4)) # p = (2, 4)
e.is_on_the_curve(p)
# Output: True

p = Point((Rational(3, 2), 2)) # p = (3/2, 2)
e.is_on_the_curve(p)
# Output: False
```

You can also operate points and take inverses.

```python
from src.elliptic_curves import O # the neutral element

p1, p2 = Point((2, 4)), Point((-2, 4))

e.add(p1, p2)
# Output: (-2, -4)

e.inv(p1)
# Output: (2, -4)

e.add(p1, e.inv(p1))
# Output: O
```

And finally you can calculate the torsion subgroup. Thanks to Mazur's Theorem, we know there are only 15 possibilities for the torsion subgroup. They are

$$\mathbb{Z}/N\mathbb{Z}, \quad 1 \leq N \leq 10 \text{ or } N = 12,$$
$$\mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2N\mathbb{Z}, \quad 1 \leq N \leq 4.$$
The property "torsion_name" returns one of these 15 names in string format, and the property "torsion" returns all the elements of the torsion subgroup explicitly.

```python
e.torsion_name
# Output: Z5

e.torsion
# Output: {(2, 4), (-2, 4), (2, -4), O, (-2, -4)}
```
