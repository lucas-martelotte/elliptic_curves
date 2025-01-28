import pygame
from pygame.surface import Surface

from src.chunk_storage import TorsionStorage

from ..essentials import Pos, Rect
from .color_dict import GROUP_TO_COLOR
from .coords import get_abc_axis, get_xyz_axis


class TorsionChunk:
    def __init__(
        self,
        chunk_position: tuple[int, int, int],
        storage: TorsionStorage,
    ):
        self.storage = storage
        self.chunk_position = chunk_position
        self.pos2torsion = self._get_pos2torsion()
        self._surfaces: dict[tuple[int, int], Surface] = {}  # {(axis, index): sfc}

    def _get_pos2torsion(self) -> dict[tuple[int, int, int], str]:
        """Receives a point coordinate as input and returns its torsion"""
        data = self.storage.get_chunk_data(list(self.chunk_position))
        pos2torsion: dict[tuple[int, int, int], str] = {}
        for torsion, points in data.items():
            for point in points:
                pos2torsion[tuple(point)] = torsion
        return pos2torsion

    def get_sfc(self, z_axis: int, index: int) -> Surface:
        """
        Returns a cross section of the chunk as a surface.
        The axis of the cross section is "z_axis" and the
        depth of the cross section is "index".
        """
        cr = self.storage.chunk_range
        x_axis, y_axis, _ = get_xyz_axis(z_axis)
        width, height, depth = cr[x_axis], cr[y_axis], cr[z_axis]
        if (z_axis, index) in self._surfaces:
            return self._surfaces[(z_axis, index)]
        sfc = Surface((cr[x_axis], cr[y_axis]))
        for abc_coord, group in self.pos2torsion.items():
            color = GROUP_TO_COLOR[group]
            x, y, z = abc_coord[x_axis], abc_coord[y_axis], abc_coord[z_axis]
            if (z % depth) != index:
                continue  # only points in the correct z-level
            sfc.set_at((x % width, y % height), color)
        self._surfaces[(z_axis, index)] = sfc
        return sfc

    def get_rect(self, z_axis: int) -> Rect:
        cr = self.storage.chunk_range
        x_axis, y_axis, _ = get_xyz_axis(z_axis)
        return Rect(
            self.chunk_position[x_axis] * cr[x_axis],
            self.chunk_position[y_axis] * cr[y_axis],
            cr[x_axis],
            cr[y_axis],
        )

    def get_pos(self, z_axis: int) -> Pos:
        rect = self.get_rect(z_axis)
        return rect.pos()

    def get_torsion(self, point: tuple[int, int, int], z_axis: int) -> str | None:
        """
        Returns None if point does not belong to chunk, otherwise
        returns the torsion name.
        """
        cr = self.storage.chunk_range
        x_axis, y_axis, _ = get_xyz_axis(z_axis)
        # ============================= #
        # = inverting the permutation = #
        new_point = [0, 0, 0]
        new_point[z_axis] = point[2]
        new_point[y_axis] = point[1]
        new_point[x_axis] = point[0]
        point = (new_point[0], new_point[1], new_point[2])
        # ============================= #
        # ============================= #
        chunk = (
            point[0] // cr[x_axis],
            point[1] // cr[y_axis],
            point[2] // cr[z_axis],
        )
        if chunk == self.chunk_position:
            return self.pos2torsion.get(point) or "0"
        return None
