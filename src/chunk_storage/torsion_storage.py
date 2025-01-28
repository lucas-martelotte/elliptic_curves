from pathlib import Path
from typing import Any

from sympy import isprime

from src.elliptic_curves.elliptic_curve import EllipticCurve, SingularCurveError

from ..chunk_storage import ChunkStorage


class TorsionStorage(ChunkStorage):
    def __init__(self):
        super().__init__(
            path=Path("./data/torsion"),
            chunk_range=[100, 100, 100],
            ignore_values=["0"],
        )

    def _calculate(self, variables: list[int]) -> Any:
        a, b, c = variables[0], variables[1], variables[2]
        try:
            return EllipticCurve(a, b, c).torsion_name
        except SingularCurveError:
            return "-"
