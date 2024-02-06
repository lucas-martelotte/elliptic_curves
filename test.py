from elliptic.elliptic_curve import EllipticCurve, SingularCurveError
from elliptic.torsion import calculate_torsion_group
from elliptic.calculate_chunks import calculate_chunk, write_chunk_image, CHUNK_SIZE
from os.path import exists

# e = EllipticCurve(4, 0)
# print(calculate_torsion_group(e))

for x in range(-3, 3, 1):
    for y in range(-3, 3, 1):
        if exists(f"chunks/{x}_{y}_{CHUNK_SIZE}.csv"):
            continue
        calculate_chunk(x, y)
        write_chunk_image(x, y)
