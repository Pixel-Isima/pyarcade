from __future__ import annotations

class Position:
    """Position of an object. Can have negative coordinates."""

    _x: int
    _y: int

    def __init__(self, x: int, y: int):
        """Create a Position element"""
        self._x = int(x)
        self._y = int(y)

    def __add__(self, other : Position):
        return Position(
            self._x + other._x,
            self._y + other._y
        )

    def __sub__(self, other : Position):
        return Position(
            self._x - other._x,
            self._y - other._y
        )

    @staticmethod
    def from_tuple(t: tuple[int, int]) -> Position:
        return Position(t[0], t[1])

    def min(self, other : Position) -> Position:
        """Create a point with its minimum coordinates"""
        return Position(
            min(self._x, other._x),
            min(self._y, other._y)
        )

    def max(self, other : Position) -> Position:
        """Create a point with its maximal coordinates"""
        return Position(
            max(self._x, other._x),
            max(self._y, other._y)
        )

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def tuple(self) -> tuple[int, int]:
        return self._x, self._y



class Size:
    """Size of an object. Must have positive values."""

    _width: int
    _height: int

    def __init__(self, width: int, height: int):
        if int(width) < 0:
            raise ValueError("width must be positive")
        if int(height) < 0:
            raise ValueError("height must be positive")

        self._width = int(width)
        self._height = int(height)

    @staticmethod
    def from_tuple(t: tuple[int, int]) -> Size:
        return Size(t[0], t[1])

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def tuple(self) -> tuple[int, int]:
        return (
            self._width,
            self._height
        )

class Rect:
    """A collection of a size and position.

    The position determines the position of the object in the draw area and
    the size determines the size of the object"""

    _position: Position
    _size: Size

    def __init__(self, position: Position, size: Size):
        self._position = position
        self._size = size

    @staticmethod
    def from_tuple(t: tuple[int, int, int, int]) -> Rect:
        return Rect(
            Position(t[0], t[1]),
            Size(t[2], t[3])
        )

    @staticmethod
    def from_coordinates(x: int, y: int, width: int, height: int) -> Rect:
        return Rect(
            Position(x, y),
            Size(width, height)
        )

    @staticmethod
    def from_points(p1: Position, p2: Position) -> Rect:
        min_x = min(p1.x, p2.x)
        max_x = max(p1.x, p2.x)

        min_y = min(p1.y, p2.y)
        max_y = max(p1.y, p2.y)

        return Rect(
            Position(min_x, min_y),
            Size(max_x - min_x, max_y - max_x)
        )

    def cut(self, by: Rect) -> Rect:
        p1min, p1max = self.points
        p2min, p2max = by.points

        return Rect.from_points(p1min.max(p2min), p1max.min(p2max))

    @property
    def x(self) -> int:
        return self._position.x

    @property
    def y(self) -> int:
        return self._position.y

    @property
    def width(self) -> int:
        return self._size.width

    @property
    def height(self) -> int:
        return self._size.height

    @property
    def position(self) -> Position:
        return self._position

    @property
    def size(self) -> Size:
        return self._size

    @property
    def tuple(self) -> tuple[int, int, int, int]:
        return (
            self._position.x,
            self._position.y,
            self._size.width,
            self._size.height
        )

    @property
    def points(self) -> (Position, Position):
        return (
            self._position,
            Position(
                self.position.x + self.size.width,
                self.position.y + self.size.height
            )
        )
