# Elliptic curve calculator

This repository implements some useful, elementary algorithms with respect to elliptic curves. Let $E(\mathbb{Q})$ be the group of rational points of an elliptic curve and $L(E, s)$ its $L$-function. Currently the following functionalities are available.

- Calculate the torsion subgroup of $E(\mathbb{Q})$,
- Calculate upper and lower bounds for the rank of $E(\mathbb{Q})$, provided the group has an element of order two,
- Calculate the value of $L(E, 1)$ for elliptic curves of the form $y^2 = x^3 - Dx$, where $D \in \mathbb{Z}$.

## Instalation

First, make sure you have Python 3 installed in your machine and the command pip3 working properly. Clone the repository and open a cmd inside of it. Simply run the following command and you're done.

`pip3 install requirements.txt`

## Basic usage

The repository's most fudamental object is an elliptic curve in Weierstrass form with integer coefficients, i.e.
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

It is possible to calculate the torsion subgroup. Thanks to Mazur's Theorem, we know there are only 15 possibilities for the torsion subgroup. They are

$$\mathbb{Z}/N\mathbb{Z}, \quad 1 \leq N \leq 10 \text{ or } N = 12,$$

$$\mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2N\mathbb{Z}, \quad 1 \leq N \leq 4.$$

The property "torsion_name" returns one of these 15 names in string format, and the property "torsion" returns all the elements of the torsion subgroup explicitly.

```python
e.torsion_name
# Output: Z5

e.torsion
# Output: {(2, 4), (-2, 4), (2, -4), O, (-2, -4)}
```

Lastly, one is able to calculate bounds for the rank. In this case, the elliptic curve must have the parameter $C$ equal to zero. This guarantees that $(0,0)$ is a point of order two in $E(\mathbb{Q})$. Let $r$ be the rank of this elliptic curve. By running "calculate_rank", the program returns a pair $(a,b)$ such that $a \leq r \leq b$. The rank can be pinpointed exactly when $a = b$. This algorithm was executed for more than 10.000 different elliptic curves and roughly 22% of them returned definitive answers for the rank.

```python
from src.elliptic_curves import calculate_rank

e = EllipticCurve(2, -4, 0)
calculate_rank(e)
# Output: (0,1)
```

## Torsion graph

A fun way to visualize how the torsion subgroup varies as $A, B$ and $C$ change was implemented and called the "torsion graph". It is essentially a 3d image constructed as follows: given a point $(A, B, C) \in \mathbb{Z}^3$, paint it a specific color based on the torsion subgroup of $E : y^2 = x^3 + Ax^2 + Bx + C$ (as we said earlier, there are only 15 possibilities and hence only 16 colors are needed, including the additional color for singular curves). This will generate a $\mathbb{Z}^3$ coloring, and the torsion graph application shows horizontal sections of it on the screen. It is interactive in the sense that the user can navigate back and forth and change cross sections, to get a full view of this coloring and get some intuition about the torsion subgroup. To run the torsion graph, do the following.


```python
from src.apps import TorsionGraph

axis = 0 # 0 means the axis of the cross section is the A-axis. Alternatively, axis=1 corresponds to B, and axis=2 to C.
torsion_graph = TorsionGraph(z_axis=axis)
torsion_graph.run()
```

All the torsion shown in the images are pre-calculated and stored in data/torsion. The regions not yet calculated are displayed in pure red. To calculate more torsion subgroups and expand the image, the user can run the following.


```python
from src.chunk_storage import TorsionStorage

storage = TorsionStorage()
n_processes = 12 # number of processes to run in parallel
storage.calculate_chunk(n_processes=n_processes)
```

This calculates a new chunk of the image and save it inside data/torsion.
