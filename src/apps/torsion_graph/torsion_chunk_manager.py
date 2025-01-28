from pygame.surface import Surface

from src.apps.essentials import Pos, Rect
from src.chunk_storage import TorsionStorage

from .camera import Camera
from .torsion_chunk import TorsionChunk


class TorsionChunkManager:
    def __init__(self, storage: TorsionStorage, z_axis: int):
        self.z_axis = z_axis
        self.storage = storage
        chunk_positions = self.storage.get_all_chunks()
        self.chunks = {
            TorsionChunk((c[0], c[1], c[2]), self.storage) for c in chunk_positions
        }

    def get_sfc(self, camera: Camera, screen_size: tuple[int, int]) -> Surface:
        cr = self.storage.chunk_range
        screen_rect = Rect(
            camera.x - screen_size[0] // 2,
            camera.y - screen_size[1] // 2,
            screen_size[0],
            screen_size[1],
        )
        screen_pos = screen_rect.pos()
        chunks_in_screen = {
            chunk
            for chunk in self.chunks
            if Rect.aabb_algorithm(screen_rect, chunk.get_rect(self.z_axis))
            and chunk.chunk_position[self.z_axis] * cr[self.z_axis] <= camera.z
            and (chunk.chunk_position[self.z_axis] + 1) * cr[self.z_axis] > camera.z
        }
        screen_sfc = Surface(screen_size)
        screen_sfc.fill((255, 0, 0))
        for chunk in chunks_in_screen:
            chunk_pos = chunk.get_pos(self.z_axis)
            chunk_sfc = chunk.get_sfc(self.z_axis, camera.z % cr[self.z_axis])
            chunk_relative_pos = chunk_pos - screen_pos
            screen_sfc.blit(chunk_sfc, chunk_relative_pos.to_tuple())
        return screen_sfc

    def get_torsion(self, point: tuple[int, int, int], z_axis: int) -> str | None:
        """
        Returns None if there is no chunk containing the point.
        Otherwise, returns the torsion.
        """
        for chunk in self.chunks:
            if torsion := chunk.get_torsion(point, z_axis):
                return torsion
        return None
