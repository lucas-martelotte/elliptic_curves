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
    for x in range(min_x - 10, max_x + 11, 1)
    for y in range(min_y - 10, max_y + 11, 1)
    if (y, x) not in coords
]
target_chunks = sorted(target_chunks, key=lambda p: max(abs(p[0]), abs(p[1])))
print(target_chunks)


def process_chunk(chunk: tuple[int, int]):
    calculate_chunk(chunk[0], chunk[1])
    write_chunk_image(chunk[0], chunk[1])


from multiprocessing import Pool

if __name__ == "__main__":
    with Pool(4) as p:
        p.map(process_chunk, target_chunks)
    exit()
