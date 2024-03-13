import json
import os

import pygame
import sympy
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


class Chunk:
    def __init__(
        self, x: int, y: int, size: int, chunkdict: dict[str, list[tuple[int, int]]]
    ):
        self.x = x
        self.y = y
        self.size = size
        self.chunkdict = chunkdict
        self._sfc: Surface | None = None
        self._last_pixel_size: int | None = None

    def get_surface(self, pixel_size: int = 10) -> tuple[Surface, tuple[int, int]]:
        chunk_x = self.x * self.size * pixel_size
        chunk_y = self.y * self.size * pixel_size
        if self._last_pixel_size == pixel_size:
            assert self._sfc is not None
            return self._sfc, (chunk_x, chunk_y)
        sfc = Surface((self.size * pixel_size, self.size * pixel_size))
        sfc.fill((0, 0, 0))
        for group, points in self.chunkdict.items():
            for py, px in points:
                point_x, point_y = px * pixel_size, py * pixel_size
                pygame.draw.rect(
                    sfc,
                    GROUP_TO_COLOR[group] if group in ["Z6"] else (0, 0, 0),
                    (point_x, point_y, pixel_size, pixel_size),
                )
        self._sfc = sfc
        self._last_pixel_size = pixel_size
        return sfc, (chunk_x, chunk_y)

    def collide(self, pos: tuple[int, int], pixel_size: int = 10) -> str | None:
        """
        Returns None if doesn't collide, else returns the
        torsion group of the pixel which is colliding.
        Obs.: pos = (x, y) in pygame coordinates.
        """
        chunk_x = self.x * self.size
        chunk_y = self.y * self.size
        relative_x, relative_y = (
            pos[0] // pixel_size - chunk_x,
            pos[1] // pixel_size - chunk_y,
        )
        if (
            relative_x >= self.size
            or relative_y >= self.size
            or relative_x < 0
            or relative_y < 0
        ):
            return None
        for group, points in self.chunkdict.items():
            if [relative_y, relative_x] in points:
                return group
        return "0"


def get_chunks(pixel_size: int = 5) -> list[Chunk]:
    chunks: list[Chunk] = []
    for filename in os.listdir("./chunks/"):
        if not filename.endswith(".json"):
            continue
        coords = filename.split(".")[0].split("_")
        ry, rx, size = int(coords[0]), int(coords[1]), int(coords[2])
        with open("./chunks/" + filename, "r") as chunkfile:
            chunkdict = json.loads(chunkfile.read())
            chunks.append(Chunk(rx, ry, size, chunkdict))
    return chunks


pygame.mouse.set_visible(False)
font_small = pygame.font.SysFont("comicsans", 36)
font_big = pygame.font.SysFont("comicsans", 48)
pixel_size, offset, camera_vel = 10, (960, 540), 50
chunks = get_chunks(pixel_size=pixel_size)
running = True
while running:
    clock.tick(60)
    pygame.display.update()

    screen.fill((0, 0, 0))
    for chunk in chunks:
        sfc, pos = chunk.get_surface(pixel_size=pixel_size)
        pos = (pos[0] + offset[0], pos[1] + offset[1])
        screen.blit(sfc, pos)

    mouse_pos = pygame.mouse.get_pos()
    offseted_mouse_pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
    a, b = offseted_mouse_pos[0] // pixel_size, offseted_mouse_pos[1] // pixel_size
    x = sympy.symbols("x")
    eq = x**3 + a * x + b
    eq_str = "y² = " + str(eq).replace("**3", "³").replace("*", "")
    pygame.draw.rect(screen, (255, 255, 255), (mouse_pos[0] - 10, mouse_pos[1], 20, 1))
    pygame.draw.rect(screen, (255, 255, 255), (mouse_pos[0], mouse_pos[1] - 10, 1, 20))
    for chunk in chunks:
        if group := chunk.collide(offseted_mouse_pos, pixel_size=pixel_size):
            if group != "0":
                text = font_big.render(group, False, (255, 255, 255))
                screen.blit(text, (mouse_pos[0] + 24, mouse_pos[1] + 12))
                text = font_small.render(eq_str, False, (255, 255, 255))
                screen.blit(text, (mouse_pos[0] + 24, mouse_pos[1] + 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_LEFT:
                offset = offset[0] + camera_vel, offset[1]
            if event.key == pygame.K_RIGHT:
                offset = offset[0] - camera_vel, offset[1]
            if event.key == pygame.K_UP:
                offset = offset[0], offset[1] + camera_vel
            if event.key == pygame.K_DOWN:
                offset = offset[0], offset[1] - camera_vel
            if event.key in [61, pygame.K_PLUS, pygame.K_KP_PLUS]:
                pixel_size = min(20, pixel_size + 1)
            if event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                pixel_size = max(1, pixel_size - 1)
