from math import floor

import numpy as np


def move_point_inside_fundamental_domain(
    w1: complex, w2: complex, p: complex
) -> complex:
    """
    Returns a complex number q inside the parallelogram spammed by w1, w2
    such that p-q is a point in the lattice <w1, w2>. Raises ValueError
    if w1, w2 fail to form a lattice.

    The calculation goes as follows, let

    [P1]
    [P2] = [w1 w2] p,    then return p -floor(P1)w1 -floor(P2)w2.
    """
    if (w2 / w1) == 0:
        raise ValueError("The point w1, w2 don't form a lattice.")
    if (w2 / w1).imag < 0:
        w1, w2 = w2, w1
    A = np.array([[w1.real, w2.real], [w1.imag, w2.imag]])
    A = np.linalg.inv(A)
    p_as_array = np.array([p.real, p.imag])
    p_changed_basis = A.dot(p_as_array)
    m, n = -floor(p_changed_basis[0]), -floor(p_changed_basis[1])
    return p + m * w1 + n * w2


def weierstrass_p_function_by_duplication_method(
    g2: complex, g3: complex, w1: complex, w2: complex, z: complex, iterations: int = 6
) -> tuple[complex, complex]:
    """
    Evaluates at z the Weierstrass p function (and its derivative)
    with invariants g2, g3 and periods w1, w2. The function uses the
    duplication method and the number of iterations is set to 6 by default.
    Returns a pair (X, Y) where X = weierstrass p function at z, and
    Y = derivative of weierstrass p function at z.
    """
    z_0 = move_point_inside_fundamental_domain(w1, w2, z) / 2**iterations
    X = 1 / z_0**2 + (g2 / 20) * z_0**2 + (g3 / 28) * z**4
    Y = -2 / z_0**3 + (g2 / 10) * z_0 + (g3 / 7) * z_0**3
    for iter in range(iterations):
        X2 = -2 * X + (6 * X**2 - g2 / 2) ** 2 / (4 * (4 * X**3 - g2 * X - g3))
        Y2 = ((12 * X**2 - g2) / (2 * Y)) * (X2 - X) + Y
        X, Y = X2, Y2
    return X, Y


def weierstrass_p_function_by_direct_calculation(
    w1: complex, w2: complex, z: complex, interval: int = 100
) -> complex:
    output = 1 / z**2
    for m in range(-interval // 2, interval // 2 + 1, 1):
        for n in range(-interval // 2, interval // 2 + 1, 1):
            if (m, n) == (0, 0):
                continue
            output += 1 / (z - m * w1 - n * w2) ** 2 - 1 / (m * w1 + n * w2) ** 2
    return output


def weierstrass_p_function_derivative_by_direct_calculation(
    w1: complex, w2: complex, z: complex, interval: int = 100
) -> complex:
    output: complex = 0
    for m in range(-interval // 2, interval // 2 + 1, 1):
        for n in range(-interval // 2, interval // 2 + 1, 1):
            output += -2 / (z - m * w1 - n * w2) ** 3
    return output
