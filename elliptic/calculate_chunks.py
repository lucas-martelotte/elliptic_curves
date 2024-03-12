import csv

import cv2
import numpy as np
from tqdm import tqdm
import json

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
    Iterates through a square of size CHUNK_SIZE in the
    coordinate (chunk_x, chunk_y).

    For each iteration (a, b) it calculates the
    torsion group of the ellptic curve y^2 = x^3 + ax + b.

    Lastly, it saves all torsion groups in a json file under
    the directory "chunks/".
    """
    chunk_dict: dict[str, list[tuple[int, int]]] = {}
    initial_x, initial_y = chunk_x * CHUNK_SIZE, chunk_y * CHUNK_SIZE
    for relative_y in tqdm(
        range(CHUNK_SIZE),
        desc=f"Calculating chunk {(chunk_x, chunk_y)}",
    ):
        y = initial_y + relative_y
        for relative_x in range(CHUNK_SIZE):
            x = initial_x + relative_x
            torsion_group = "*"
            try:
                e = EllipticCurve(x, y)
                torsion_group = calculate_torsion_subgroup(e)
            except SingularCurveError:
                pass
            if torsion_group != "0":
                if torsion_group not in chunk_dict:
                    chunk_dict[torsion_group] = []
                chunk_dict[torsion_group].append((relative_y, relative_x))
    for key, value in chunk_dict.items():
        chunk_dict[key] = sorted(value)
    with open(f"chunks/{chunk_y}_{chunk_x}_{CHUNK_SIZE}.json", "w") as file:
        json.dump(chunk_dict, file)


def write_chunk_image(chunk_y: int, chunk_x: int):
    """
    Reads the chunk file (if there is any) and writes an image
    file corresponding to it in the directory "chunks/".
    """
    with open(f"chunks/{chunk_y}_{chunk_x}_{CHUNK_SIZE}.json", "r") as file:
        chunk_dict = json.loads(file.read())
        image = np.zeros((CHUNK_SIZE, CHUNK_SIZE, 3))
        for group, points in chunk_dict.items():
            for py, px in points:
                image[py, px] = GROUP_TO_COLOR[group][::-1]
        cv2.imwrite(f"chunks/{chunk_y}_{chunk_x}_{CHUNK_SIZE}_NEW.png", image)
