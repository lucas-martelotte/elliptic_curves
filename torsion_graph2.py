import json
import os

import pygame
from pygame.surface import Surface

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

pygame.init()
pygame.display.set_caption("Torsion Group Graph")

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()


def get_chunk_surfaces(
    pixel_size: int = 5, offset: tuple[int, int] = (960, 540)
) -> list[tuple[Surface, int, int]]:
    sfcs: list[tuple[Surface, int, int]] = []
    for filename in os.listdir("./chunks/"):
        if not filename.endswith(".json"):
            continue
        coords = filename.split(".")[0].split("_")
        ry, rx, size = int(coords[0]), int(coords[1]), int(coords[2])
        sfc = Surface((size * pixel_size, size * pixel_size))
        sfc.fill((0, 0, 0))
        chunk_x = offset[0] + rx * size * pixel_size
        chunk_y = offset[1] + ry * size * pixel_size
        with open("./chunks/" + filename, "r") as chunkfile:
            chunkdict = json.loads(chunkfile.read())
            for group, points in chunkdict.items():
                for py, px in points:
                    point_x, point_y = px * pixel_size, py * pixel_size
                    pygame.draw.rect(
                        sfc,
                        GROUP_TO_COLOR[group],
                        (point_x, point_y, pixel_size, pixel_size),
                    )
        sfcs.append((sfc, chunk_x, chunk_y))
    return sfcs


chunk_sfcs = get_chunk_surfaces()
running = True
while running:
    clock.tick(24)
    pygame.display.update()

    screen.fill((0, 0, 0))
    for sfc, x, y in chunk_sfcs:
        screen.blit(sfc, (x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
