from os.path import exists

import sympy

from elliptic.calculate_chunks import CHUNK_SIZE, calculate_chunk, write_chunk_image
from elliptic.elliptic_curve import EllipticCurve, SingularCurveError
from elliptic.rank import calculate_rank_of_elliptic_curve
from elliptic.torsion import calculate_torsion_subgroup

with open("ranks_filtered.txt", "r") as file:
    for line in file.readlines():
        parts = line.split(",")
        a = int(parts[0][1:])
        b = int(parts[1])
        rank = int(parts[2][:-2])
        # =====
        new_a = b - a**2
        new_b = a**2 - a**3 - a * b
        torsion = calculate_torsion_subgroup(EllipticCurve(new_a, new_b))
        result = f"{(a, b, rank)}\t{(new_a, new_b, torsion)}"
        with open("ranks_and_torsion.txt", "a") as a_file:
            a_file.write(f"{result}\n")
        if torsion != "0":
            with open("ranks_and_non_trivial_torsion.txt", "a") as a_file:
                a_file.write(f"{result}\n")

            x = sympy.symbols("x")
            exp_1 = str(x**3 + a * x**2 + b * x).replace("**", "^").replace("*", "")
            exp_2 = str(x**3 + new_a * x + new_b).replace("**", "^").replace("*", "")
            with open("ranks_and_non_trivial_torsion_parsed.txt", "a") as a_file:
                a_file.write(f"{exp_1}\t|\t{exp_2}\t|\t{rank}\t|\t{torsion}\n")

# class Spiral:
#     def __init__(self, o_x: int, o_y: int):
#         self.o_x, self.o_y = o_x, o_y
#         self.step_index = 0
#         self.step_direction = 1
#         self.step_size = 1

#     def next(self) -> tuple[int, int]:
#         point = (self.o_x, self.o_y)
#         if self.step_index == 2 * self.step_size:
#             self.step_index = 0
#             self.step_size += 1
#             self.step_direction *= -1
#         if self.step_index < self.step_size:
#             self.o_x += self.step_direction
#         else:
#             self.o_y += self.step_direction
#         self.step_index += 1
#         return point


# spiral = Spiral(0, 0)
# while True:
#     point = spiral.next()
#     try:
#         rank = calculate_rank_of_elliptic_curve(point[0], point[1])
#         print(f"Rank of {point} is {rank}.")
#         with open("ranks.txt", "a") as file:
#             file.write(f"{point}".ljust(20) + f"{rank}\n")
#     except Exception:
#         print(f"Unable to determine the rank of {point}.")
#         with open("ranks.txt", "a") as file:
#             file.write(f"{point}".ljust(20) + "--\n")

exit()


# y^2 = x^3 -6x + 4
# y -> y/2
# y^2 = 4x^3 -24x + 16
# y -> y/4, x -> x/4
# y^2 = x^3 -96x + 256
e = EllipticCurve(-6, 4)
print(calculate_torsion_subgroup(e))

e = EllipticCurve(-96, 256)
print(calculate_torsion_subgroup(e))

# y^2 = 4x^3 - 1
# y -> y/4, x -> x/4
# y^2 = x^3 - 16
e = EllipticCurve(0, -16)
print(calculate_torsion_subgroup(e))

# y^2 = 4x^3 + 168x - 622
# y -> y/4, x -> x/4
# y^2 = x^3 + 672x - 9952
e = EllipticCurve(672, -9952)
print(calculate_torsion_subgroup(e))

# for x in range(-3, 3, 1):
#     for y in range(-3, 3, 1):
#         if exists(f"chunks/{x}_{y}_{CHUNK_SIZE}.csv"):
#             continue
#         calculate_chunk(x, y)
#         write_chunk_image(x, y)
