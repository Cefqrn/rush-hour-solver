from __future__ import annotations

from typing import NamedTuple


class Vector2(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> Vector2:
        return Vector2(self.x * other, self.y * other)
