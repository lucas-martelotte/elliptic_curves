import itertools
import json
import multiprocessing
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from tqdm import tqdm


class ChunkStorage(ABC):
    def __init__(
        self, path: Path, chunk_range: list[int], ignore_values: list[Any]
    ) -> None:
        super().__init__()
        self.path = path
        self.chunk_range = chunk_range
        self.ignore_values = ignore_values

    @abstractmethod
    def _calculate(self, variables: list[int]) -> Any:
        pass

    def _iterate(self, args) -> Any:
        """
        Calculates one coordinate of the chunk and stores its value in the
        dictionary if it is not one of the values to ignore.
        """
        result = self._calculate(args)
        if result in self.ignore_values:
            return None
        return (args, result)

    def _get_next_chunk(self) -> list[int]:
        """Returns next non-calculated chunk."""
        if not self.path.is_dir():
            self.path.mkdir()
        n_variables = len(self.chunk_range)
        chunks = self.get_all_chunks()
        if len(chunks) == 0:
            return [0 for _ in range(n_variables)]
        min_xs = [min(c[i] for c in chunks) for i in range(n_variables)]
        max_xs = [max(c[i] for c in chunks) for i in range(n_variables)]
        range_xs = [range(min_xs[i], max_xs[i] + 1) for i in range(n_variables)]
        for chunk in itertools.product(*range_xs):
            if list(chunk) not in chunks:
                return list(chunk)
        return [min_xs[i] - 1 for i in range(n_variables)]

    def calculate_chunk(
        self, target_chunk: list[int] | None = None, n_processes: int = 1
    ) -> None:
        """Calculates a new chunk and saves it to storage."""
        nc, cr = target_chunk or self._get_next_chunk(), self.chunk_range
        assert len(nc) == len(cr)
        n_variables = len(cr)
        ranges = [range(nc[i] * cr[i], (nc[i] + 1) * cr[i]) for i in range(n_variables)]
        combinations = list(itertools.product(*ranges))
        results: dict[str, list[int]] = {}
        with multiprocessing.Pool(n_processes) as pool:
            for output in tqdm(
                pool.imap_unordered(self._iterate, combinations),
                total=len(combinations),
                mininterval=1.0,
            ):
                if output is not None:
                    args, result = output
                    if result not in results:
                        results[result] = []
                    results[result].append(args)
        with open(self.get_chunk_path(nc), "w") as f:
            json.dump(dict(results), f)

    def get_chunk_data(self, target_chunk: list[int]) -> dict:
        chunk_path = self.get_chunk_path(target_chunk)
        assert chunk_path.exists()
        with open(self.get_chunk_path(target_chunk), "r") as f:
            return json.load(f)

    def get_all_chunk_data(self) -> dict[tuple, dict]:
        chunks = self.get_all_chunks()
        return {tuple(c): self.get_chunk_data(c) for c in chunks}

    def get_all_chunks(self) -> list[list[int]]:
        stems = self.path.glob("*.json")
        return [[int(s) for s in c.stem.split("_")] for c in stems]

    def get_chunk_path(self, target_chunk: list[int]) -> Path:
        return self.path / ("_".join(map(str, target_chunk)) + ".json")
