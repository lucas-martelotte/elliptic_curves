from math import ceil, floor, sqrt

from sympy.ntheory import factorint


def gaussian_division(a: complex, b: complex) -> tuple[complex, complex]:
    """
    Returns gaussian integers q and r such that a = bq + r.
    """
    e = a / b
    q = complex(round(e.real), round(e.imag))
    # print(f"Divide: {(a, b)}")
    assert gaussian_norm(a - b * q) < gaussian_norm(b)
    return q, a - b * q


def divides(a: complex, b: complex) -> complex:
    """Returns True if a divides b"""
    return gaussian_division(b, a)[1] == 0


def mod(a: complex, b: complex) -> complex:
    """Reduces a mod b in the gaussian integers"""
    return gaussian_division(a, b)[1]


def euclidean_norm(a: complex) -> float:
    """Returns the euclidean norm of a"""
    norm = sqrt(a.real**2 + a.imag**2)
    return norm


def gaussian_norm(a: complex) -> int:
    """Returns the gaussian norm of a"""
    norm = a.real**2 + a.imag**2
    assert norm.is_integer()
    return int(norm)


def is_primary(a: complex) -> bool:
    return mod(a, 2 + 2j) == 1


def conjugate(a: complex) -> complex:
    return complex(a.real, -a.imag)


def is_unit(a: complex) -> bool:
    return a in {1, -1, 1j, -1j}


def get_representatives_mod(a: complex) -> list[complex]:
    """Returns a set of representatives mod a"""
    representatives: set[complex] = set()
    a_norm = ceil(euclidean_norm(a))
    for m in range(-a_norm, a_norm + 1, 1):
        max_norm = ceil(sqrt(a_norm**2 - m**2))
        for n in range(-max_norm, max_norm + 1, 1):
            candidate = complex(m, n)
            residue = mod(candidate, a)
            if any(divides(a, f - residue) for f in representatives):
                continue
            representatives.add(residue)
    return sorted(representatives, key=gaussian_norm)


def gaussian_gcd(a: complex, b: complex) -> complex:
    if b == 0:
        return a
    return gaussian_gcd(b, gaussian_division(a, b)[1])


def factor_primary_rational_prime(p: int) -> tuple[complex, complex]:
    """Factors a prime p = 4k+1 into a conjugate prime pair"""
    for n in range(2, p, 1):
        if (pow(n, (p - 1) // 2, p) + 1) % p == 0:  # Checking if n^((p-1)/2) = -1 mod p
            k = (n ** ((p - 1) // 4)) % p  # This k has k^2 = -1 mod p
            g_prime = gaussian_gcd(p, k + 1j)
            if is_unit(g_prime):
                g_prime = gaussian_gcd(p, k - 1j)
            return (g_prime, conjugate(g_prime))
    raise Exception("Unknown error.")


def factor_gaussian_integer(a: complex) -> dict[complex, int]:
    """
    Factors the integer a into a product of gaussian primes.
    Returns a list of tuples of the form (prime, power).
    """
    if is_unit(a):
        return {a: 1}
    norm_factors: dict[int, int] = factorint(gaussian_norm(a))
    a_factors: dict[complex, int] = {}
    for p, r in norm_factors.items():
        if p == 2:
            a_factors[1 + 1j] = r
            a, _ = gaussian_division(a, (1 + 1j) ** r)
        elif p % 4 == 3:
            assert r % 2 == 0
            a_factors[p + 0j] = r // 2
            a, _ = gaussian_division(a, p ** (r // 2))
        elif p % 4 == 1:
            pi, pi_bar = factor_primary_rational_prime(p)
            pi_power, pi_bar_power = 0, 0
            while divides(pi, a):
                a, _ = gaussian_division(a, pi)
                pi_power += 1
            while divides(pi_bar, a):
                a, _ = gaussian_division(a, pi_bar)
                pi_bar_power += 1
            if pi_power > 0:
                a_factors[pi] = pi_power
            if pi_bar_power > 0:
                a_factors[pi_bar] = pi_bar_power
    assert is_unit(a)
    if a != 1:
        a_factors[a] = 1
    return a_factors


def coprime(a: complex, b: complex) -> bool:
    return is_unit(gaussian_gcd(a, b))


def fast_modular_exp(a: complex, k: int, b: complex) -> complex:
    output = a
    exp_factors = factorint(k)
    for exp_factor, exp_factor_power in exp_factors.items():
        for _ in range(exp_factor_power):
            output = mod(output**exp_factor, b)
    return output
