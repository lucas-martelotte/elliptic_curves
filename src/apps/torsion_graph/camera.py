import pygame
from pygame.event import Event


class Camera:
    def __init__(self, x: int, y: int, z: int, step_size: int):
        self.x, self.y, self.z = x, y, z
        self.step_size = step_size
        self.x_key_pressed = False
        self.z_key_pressed = False
        self.shift_key_pressed = False

    def handle_event(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.x -= self.step_size
            if event.key == pygame.K_RIGHT:
                self.x += self.step_size
            if event.key == pygame.K_UP:
                self.y += self.step_size
            if event.key == pygame.K_DOWN:
                self.y -= self.step_size
            if event.key == pygame.K_z:
                self.z_key_pressed = True
            if event.key == pygame.K_x:
                self.x_key_pressed = True
            if event.key == pygame.K_f:
                self.set_pos(0, 0, 0)
            if event.key == pygame.K_LSHIFT:
                self.shift_key_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                self.z_key_pressed = False
            if event.key == pygame.K_x:
                self.x_key_pressed = False
            if event.key == pygame.K_LSHIFT:
                self.shift_key_pressed = False

    def update(self):
        if self.z_key_pressed:
            self.z -= 1
            if not self.shift_key_pressed:
                self.z_key_pressed = False
        if self.x_key_pressed:
            self.z += 1
            if not self.shift_key_pressed:
                self.x_key_pressed = False

    @property
    def position(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z

    def set_pos(self, x: int, y: int, z: int) -> None:
        self.x, self.y, self.z = x, y, z
