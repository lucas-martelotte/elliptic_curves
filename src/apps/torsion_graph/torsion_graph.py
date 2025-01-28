from typing import Any

import pygame
from pygame.event import Event
from pygame.surface import Surface
from sympy import symbols

from src.chunk_storage import TorsionStorage

from ..essentials import Pos, Rect
from .camera import Camera
from .coords import get_abc_axis, get_abc_axis_and_plane_name
from .torsion_chunk_manager import TorsionChunkManager


class TorsionGraph:
    def __init__(self, z_axis: int):
        self.z_axis = z_axis
        self.storage = TorsionStorage()
        self.axis_to_chunk_manager = {
            z: TorsionChunkManager(self.storage, z) for z in range(3)
        }
        self.screen_width, self.screen_height = 1920, 1080
        self.running = False
        self.pixel_size = 6
        self.camera = Camera(0, 0, 0, 10)

    def run(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.__class__.__name__)
        self.font_small = pygame.font.SysFont("comicsans", 36)
        self.font_big = pygame.font.SysFont("comicsans", 48)
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            clock.tick(30)
            self._loop(screen)

    def _loop(self, screen: Surface):
        sw, sh, ps = self.screen_width, self.screen_height, self.pixel_size
        screen.fill((0, 0, 0))
        # ================================ #
        # ================================ #
        scaled_screen_size = Pos(sw // ps, sh // ps)
        sfc = self.axis_to_chunk_manager[self.z_axis].get_sfc(
            self.camera, scaled_screen_size.to_tuple()
        )
        sfc = pygame.transform.flip(sfc, False, True)
        sfc = pygame.transform.scale(sfc, (sw, sh))
        screen.blit(sfc, (0, 0))
        # ================================ #
        # ================================ #
        mouse_pos = pygame.mouse.get_pos()
        scaled_global_pos_tuple = (
            self.camera.x + (mouse_pos[0] - sw // 2) // ps,
            self.camera.y + -(mouse_pos[1] - sh // 2) // ps,
            self.camera.z,
        )
        a_axis, b_axis, c_axis = get_abc_axis(self.z_axis)
        axis_name, plane_name = get_abc_axis_and_plane_name(self.z_axis)
        axis_depth = scaled_global_pos_tuple[2]
        a, b, c = (
            scaled_global_pos_tuple[a_axis],
            scaled_global_pos_tuple[b_axis],
            scaled_global_pos_tuple[c_axis],
        )
        torsion = self.axis_to_chunk_manager[self.z_axis].get_torsion(
            scaled_global_pos_tuple, self.z_axis
        )

        text_sfc = self.font_small.render(
            "E : y² = x³ + Ax² + Bx + C", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 10))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render(
            f"{plane_name}-plane ({axis_name} = {axis_depth})", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 40))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render("CONTROLS", True, (255, 255, 0))
        text_rect = text_sfc.get_rect(topright=(sw - 10, 100))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render(
            "Use arrow keys to move around", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 130))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render(
            "Use z/x keys to change depth", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 160))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render(
            "Hold shift to change depth faster", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 190))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render(
            "Use a/s keys to change axis", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 220))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render(
            "Use +/- keys to zoom in/out", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 250))
        screen.blit(text_sfc, text_rect)

        text_sfc = self.font_small.render(
            "Use f key to reset camera", True, (255, 255, 255)
        )
        text_rect = text_sfc.get_rect(topright=(sw - 10, 280))
        screen.blit(text_sfc, text_rect)

        # text_sfc = self.font_small.render(
        #    f"Mouse position: {scaled_global_pos_tuple}.", False, (255, 255, 255)
        # )
        # screen.blit(text_sfc, (10, 50))
        # text_sfc = self.font_small.render(
        #    f"Curve coefficients: {(a, b, c)}.", False, (255, 255, 255)
        # )
        # screen.blit(text_sfc, (10, 90))
        # text_sfc = self.font_small.render(
        #    f"Torsion: {torsion}.", False, (255, 255, 255)
        # )
        # screen.blit(text_sfc, (10, 130))
        # text_sfc = self.font_small.render(
        #    f"Camera position: {self.camera.position}.", False, (255, 255, 255)
        # )
        # screen.blit(text_sfc, (10, 10))

        x = symbols("x")
        eq = x**3 + a * x**2 + b * x + c
        eq_str = "y² = "
        eq_str += str(eq).replace("**3", "³").replace("**2", "²").replace("*", "")
        if torsion != "0":
            text = self.font_big.render(torsion, False, (255, 255, 255))
            screen.blit(text, (mouse_pos[0] + 24, mouse_pos[1] + 12))
            text = self.font_small.render(eq_str, False, (255, 255, 255))
            screen.blit(text, (mouse_pos[0] + 24, mouse_pos[1] + 80))
        # ================================ #
        # ================================ #
        pygame.display.update()
        self.camera.update()
        for event in pygame.event.get():
            self.camera.handle_event(event)
            self._handle_event(event)

    def _handle_event(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.z_axis = (self.z_axis + 1) % 3
            if event.key == pygame.K_s:
                self.z_axis = (self.z_axis - 1) % 3
            if event.key in [pygame.K_EQUALS, pygame.K_KP_PLUS]:
                self.pixel_size = min(self.pixel_size + 1, 20)
            if event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                self.pixel_size = max(self.pixel_size - 1, 1)
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
