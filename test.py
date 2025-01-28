import multiprocessing
from math import e, log, pi, sqrt
from pathlib import Path
from pprint import pprint
from time import time

import sympy
from sympy import Rational as R
from sympy import primerange
from sympy import sqrt as sp_sqrt
from sympy import symbols

from src.apps import TorsionGraph
from src.chunk_storage import ChunkStorage, TorsionStorage
from src.elliptic_curves import EllipticCurve, Point, calculate_rank
from src.elliptic_curves.counting_points_mod_p import (
    ModifiedBernoulliNumbers,
    count_points_mod_p,
    count_points_mod_p_naive,
)
from src.elliptic_curves.elliptic_curve import EllipticCurve
from src.utils.elliptic_functions import (
    move_point_inside_fundamental_domain,
    weierstrass_p_function_by_direct_calculation,
    weierstrass_p_function_by_duplication_method,
    weierstrass_p_function_derivative_by_direct_calculation,
)
from src.utils.gaussian_integers import (
    coprime,
    divides,
    euclidean_norm,
    factor_gaussian_integer,
    factor_primary_rational_prime,
    gaussian_division,
    gaussian_gcd,
    gaussian_norm,
    get_representatives_mod,
    is_primary,
    mod,
)
from src.utils.quartic_symbol import quartic_symbol

# from src.utils.elliptic_functions import weierstrass_p
from src.utils.rational_integers import (
    fourth_power_divisors_of,
    is_fourth_power_free,
    radical,
    remove_square_factors_of,
    square_free_divisors_of,
)

# A, B, C, x, y = symbols("A, B, C, x, y")
# P_0 = x**3 + A * x**2 + B * x + C
# P_1 = 3 * x**2 + 2 * A * x + B

# G = x**3 + B * x + C
# G_1 = 3 * x**3 - 5 * B * x - 27 * C
# F = x**4 - 2 * B * x**2 - 8 * C * x + B**2
# F_1 = 3 * x**2 + 4 * B


# exp_f = sympy.expand(F * F_1)
# exp_g = sympy.expand(G * G_1)
# res = sympy.expand(F * F_1 - G * G_1)
# print(exp_f)
# print(exp_g)
# print(res)
# print(f"Degree: x is {sympy.degree(res, gen=x)}, y is {sympy.degree(res, gen=y)}")


# exit()

if __name__ == "__main__":
    # storage = TorsionStorage()
    # storage.calculate_chunk(target_chunk=[0, 0, 0], n_processes=8)

    # for i in range(-120, -10):
    #     curve = EllipticCurve(2, i, 0)
    #     print(curve.torsion_name)
    # exit()

    torsion_graph = TorsionGraph(z_axis=0)
    torsion_graph.run()
exit()

# bn = ModifiedBernoulliNumbers()
# for i in range(2, 11, 1):
#     print(f"B{2*i}:\t{bn.find(2*i)}")


# max_prime = 300
# t2, t3 = 3, 5
# print(f"Curve E : y² = 4x³ -({t2})x -({t3})")

# start = time()

# count_fast = count_points_mod_p(t2, t3, max_prime)

# print(time() - start)
# start = time()

# count_naive = {
#     p: len(count_points_mod_p_naive(t2, t3, p)) for p in primerange(max_prime)
# }

# print(time() - start)


# def correction_factor(n_solutions: int) -> str:
#     real_part = R(p + 1 - n_solutions, 2)
#     imag_part = sp_sqrt(p - real_part**2)
#     return f"{real_part} + {imag_part}i"


# print(
#     ""
#     + f"p           | count fast  | count naive | correction term \n"
#     + f"------------|-------------|-------------|-------------------"
# )  # 11 spaces per column
# for p in primerange(19, max_prime):
#     print(
#         f"{p}".ljust(11)
#         + " | "
#         + f"{count_fast[p]}".ljust(11)
#         + " | "
#         + f"{count_naive[p]}".ljust(11)
#         + " | "
#         + f"{correction_factor(count_naive[p])}".ljust(11)
#     )

# exit()

# ====================================================================================#
# =========================== CALCULATING THE L-FUNCTION =============================#
# ====================================================================================#

# with open("values_of_LD.txt", "r") as f:
#     with open("values_of_LD_formatted.txt", "w") as g:
#         for line in f.readlines():
#             parts = [p.strip() for p in line.split("&")]
#             if parts[-2] == "-":
#                 print(parts[-2])
#                 continue
#             parts[-1] = parts[-1].replace("x", "\\times").replace("Z2", "\\Z_2")
#             parts[-2] = parts[-2].replace(">=", "\\geq ")
#             parts = [f"${p}$" for p in parts]
#             print(parts)
#             g.write(" & ".join(parts) + " \\\\ \n")
# exit()

# # w = 2.6220575
# w = sqrt(2) * pi * e ** (-pi / 6)
# for n in range(1, 1000, 1):
#     w *= (1 - e ** (-2 * pi * n)) ** 2


# w1, w2 = w, 1j * w
# g2, g3 = 4, 0
# weierstrass = lambda z: weierstrass_p_function_by_duplication_method(g2, g3, w1, w2, z)

# for D in range(3, 10000, 1):
#     if not is_fourth_power_free(D) or D in {2, 4, 8}:
#         continue

#     curve = EllipticCurve(0, -D, 0)
#     torsion = curve.torsion_name
#     rank: int | str = ">0" if curve.has_non_zero_rank() else "-"
#     rank_lower_bound, rank_upper_bound = calculate_rank(EllipticCurve(0, -D, 0))
#     if rank_lower_bound == rank_upper_bound:
#         rank = rank_lower_bound
#     elif rank_lower_bound > 0:
#         rank = f">={rank_lower_bound}"

#     # === Calculating L_D(1) ===#
#     E, F = D, 1
#     while E % 2 == 0:
#         E, F = E // 2, F * 2
#     if not is_primary(E):
#         E, F = -E, -F
#     K = 4 if F in {1, -1} else 8
#     Rad = radical(E)
#     if not is_primary(Rad):
#         Rad = -Rad
#     print(f"D = {D} = ({E})*({F}) \t:\t E = {E}, F = {F}, K = {K}, R = {Rad}")

#     K_primary_reps = [r for r in get_representatives_mod(K) if is_primary(r)]
#     Rad_reps_prime_to_Rad = [r for r in get_representatives_mod(Rad) if coprime(r, Rad)]

#     L: complex = 0
#     for a in Rad_reps_prime_to_Rad:
#         for b in K_primary_reps:
#             wp_b, dwp_b = weierstrass(b * w / K)
#             wp_a, _ = weierstrass(a * w / Rad)
#             lam = K * a + b * Rad
#             L += quartic_symbol(D, lam) * (dwp_b / (wp_b - wp_a))
#     L *= w / (2 * K * Rad)

#     L_int: complex = (D ** (1 / 4) * L / w) if D > 0 else ((-4 * D) ** (1 / 4) * L / w)
#     L_int_rounded = round(L_int.real)
#     print(
#         f"{D}: {L_int_rounded} \t Err: {round(euclidean_norm(L_int_rounded-L_int), 2)} \t {L}\n"
#     )

#     with open("values_of_LD.txt", "a") as f:
#         f.write(
#             f"{D} & {E} & {F} & {K} & {Rad} & {L_int_rounded} & {rank} & {torsion}\n"
#         )

# ==========================================================================#
# ==========================================================================#
# ==========================================================================#

# curve = EllipticCurve(0, 0, 17)
# P1, P2 = Point((R(-1), R(4))), Point((R(2), R(5)))
# print(curve)
# print(f"Torsion: {curve.torsion}")
# print(f"\n{curve.add(P1, P2)}")

# curve = EllipticCurve(0, -1, 0)
# print(curve)
# print(f"Torsion: {curve.torsion}")

# curve = EllipticCurve(0, 93, 94)
# print(curve)
# print(f"Torsion: {curve.torsion}")

# curve = EllipticCurve(1, -4, 0)
# print(curve)
# print(f"Torsion: {curve.torsion}")
# print(f"Rank: {calculate_rank(curve)}")

# curve = EllipticCurve(1, 2, 3)
# curve_bar = EllipticCurve(-2 * curve.a, curve.a**2 - 4 * curve.b, 0)
# print(f"{curve} | Bar{curve_bar}")
# print(f"Torsion ({curve.torsion_name}): {curve.torsion}")
# print(f"Rank: {calculate_rank(curve)}")


# curve = EllipticCurve(1, -4, 0)
# curve_bar = EllipticCurve(-2 * curve.a, curve.a**2 - 4 * curve.b, 0)
# print(f"{curve} | Bar{curve_bar}")
# print(f"Torsion ({curve.torsion_name}): {curve.torsion}")

# point = Point((R(18), R(-78)))
# assert curve.is_on_the_curve(point)

# curr_point = point
# for i in range(4):
#     value = curr_point.value
#     assert value != "O"
#     x_num, x_dem = int(value[0].p), int(value[0].q)
#     x_num_free = remove_square_factors_of(x_num)
#     print(str(curr_point) + ": " + str(x_num_free))
#     curr_point = curve.add(curr_point, point)
