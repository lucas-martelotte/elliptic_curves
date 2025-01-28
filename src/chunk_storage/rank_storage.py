from pathlib import Path
from typing import Any

from sympy import isprime

from src.elliptic_curves.elliptic_curve import EllipticCurve, SingularCurveError
from src.elliptic_curves.rank_calculator import calculate_rank

from ..chunk_storage import ChunkStorage


class RankStorage(ChunkStorage):
    def __init__(self):
        super().__init__(
            path=Path("./data/rank"),
            chunk_range=[20, 20],
            ignore_values=["0"],
        )

    def _calculate(self, variables: list[int]) -> Any:
        a, b = variables[0], variables[1]
        try:
            e = EllipticCurve(a, b, 0)
            lower, upper = calculate_rank(e)
            return str(lower) if lower == upper else f"{lower}_{upper}"
        except SingularCurveError:
            return "-"
