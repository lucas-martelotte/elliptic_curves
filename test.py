import os
from os.path import exists

import sympy

from elliptic.calculate_chunks import CHUNK_SIZE, calculate_chunk, write_chunk_image
from elliptic.elliptic_curve import EllipticCurve, SingularCurveError
from elliptic.rank import calculate_rank_of_elliptic_curve
from elliptic.torsion import calculate_torsion_subgroup

fs = [d for d in os.listdir("./chunks/") if d.endswith(".json")]  # All chunk files
# List of the coordinates (x, y) (in pygame coordinates) of all calculated chunks
coords = [(int(c[0]), int(c[1])) for c in map(lambda x: x.split(".")[0].split("_"), fs)]
min_y, max_y = min(c[0] for c in coords), max(c[0] for c in coords)
min_x, max_x = min(c[1] for c in coords), max(c[1] for c in coords)
target_chunks = [
    (y, x)
    for x in range(min_x - 1, max_x + 2, 1)
    for y in range(min_y - 1, max_y + 2, 1)
    if (y, x) not in coords
]
target_chunks = sorted(target_chunks, key=lambda p: max(abs(p[0]), abs(p[1])))
print(target_chunks)

for chunk in target_chunks:
    calculate_chunk(chunk[0], chunk[1])
    write_chunk_image(chunk[0], chunk[1])

exit()

print(f"Rank is: {calculate_rank_of_elliptic_curve(0, -5)}.")
# for a in range(-100, 100, 1):
#     for b in range(-100, 100, 1):
#         try:
#             rank = calculate_rank_of_elliptic_curve(-1, 0)
#             print(f"Rank of E : y^2 = x^3 + ax^2 + bx is:\t{rank}.")
#         except TimeoutError:
#             pass
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
