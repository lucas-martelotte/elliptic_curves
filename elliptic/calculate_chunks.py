import csv

import cv2
import numpy as np
from tqdm import tqdm

from .elliptic_curve import EllipticCurve, SingularCurveError
from .torsion import calculate_torsion_subgroup

CHUNK_SIZE = 50
GROUP_TO_COLOR = {
    "*": (255, 255, 255),  # WHITE
    "0": (0, 0, 0),  # BLACK
    "Z2": (0, 0, 255),  # DARK BLUE
    "Z3": (0, 238, 255),  # LIGHT BLUE
    "Z4": (5, 237, 28),  # GREEN
    "Z5": (148, 5, 250),  # PURPLE
    "Z6": (216, 161, 255),  # LILAC
    "Z7": (0, 150, 136),  # teal
    "Z8": (103, 58, 183),  # deep purple
    "Z9": (200, 200, 200),  # gray
    "Z10": (232, 30, 99),  # pink
    "Z12": (244, 67, 54),  # red
    "Z2 x Z2": (139, 195, 74),  # light green
    "Z2 x Z4": (255, 235, 59),  # yellow
    "Z2 x Z6": (255, 152, 0),  # orange
    "Z2 x Z8": (255, 87, 34),  # deep orange
}


def calculate_chunk(chunk_y: int, chunk_x: int):
    """
    Iterates through a square of size CHUNK_SIZE in the coordinate
    (chunk_x, chunk_y). For each iteration (a, b) it calculates the
    torsion group of the ellptic curve y^2 = x^3 + ax + b and
    calculates its torsion group. Lastly, it saves all torsion
    groups in a csv file under the directory "chunks/".
    """
    initial_x, initial_y = chunk_x * CHUNK_SIZE, chunk_y * CHUNK_SIZE
    rows: list[list[str]] = []
    for y in tqdm(
        range(initial_y, initial_y + CHUNK_SIZE, 1),
        desc=f"Calculating chunk {(chunk_x, chunk_y)}",
    ):
        current_row: list[str] = []
        for x in range(initial_x, initial_x + CHUNK_SIZE, 1):
            torsion_group = "*"
            try:
                e = EllipticCurve(x, y)
                torsion_group = calculate_torsion_subgroup(e)
            except SingularCurveError:
                pass
            current_row.append(torsion_group)
        rows.append(current_row)
    with open(f"chunks/{chunk_y}_{chunk_x}_{CHUNK_SIZE}.csv", "w", newline="") as file:
        for row in rows:
            csv.writer(file).writerow(row)


def write_chunk_image(chunk_y: int, chunk_x: int):
    """
    Reads the chunk file (if there is any) and writes an image
    file corresponding to it in the directory "chunks/".
    """
    with open(f"chunks/{chunk_y}_{chunk_x}_{CHUNK_SIZE}.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",", quotechar="|")
        image = np.zeros((CHUNK_SIZE, CHUNK_SIZE, 3))
        x, y = 0, 0
        for row in reader:
            x = 0
            for group in row:
                color = GROUP_TO_COLOR[group]
                color = (color[2], color[1], color[0])
                image[y, x] = color
                x += 1
            y += 1
        cv2.imwrite(f"chunks/{chunk_y}_{chunk_x}_{CHUNK_SIZE}.png", image)
