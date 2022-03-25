################################################################################
# Filename: graphics/frame.py                                                  #
# Created by: Venceslas Duet                                                   #
# Created at: 04-07-2018                                                       #
# Last update at: 03-16-2022                                                   #
# Description: base UI system for create zoom framed image                     #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

from __future__ import annotations

import pygame
import enum
import internal
from deprecated.sphinx import deprecated, versionadded
from graphics.metrics import Size, Position, Rect


class Side(enum.Enum):
    TOP = 0
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3

class Margin:
    top: int
    bottom: int
    left: int
    right: int

    def __init__(self, top: int, left: int, bottom: int, right: int):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    @staticmethod
    def from_tuple(e: tuple[int, int, int, int]) -> Margin:
        return Margin(
            e[0],
            e[1],
            e[2],
            e[3]
        )

    def from_index(self, idx : int) -> int:
        match idx:
            case 0: return self.top
            case 1: return self.left
            case 2: return self.bottom
            case 3: return self.right

    def to_index(self, idx: int, val: int):
        match idx:
            case 0: self.top = val
            case 1: self.left = val
            case 2: self.bottom = val
            case 3: self.right = val

    @staticmethod
    def empty() -> Margin:
        return Margin(0, 0, 0, 0)

class Frame(pygame.Surface):
    _margin: Margin
    _min_size: Size
    _elements: list[list[pygame.Surface]]

    def __init__(self, image: pygame.Surface, margin: Margin = Margin.empty()):
        if (((margin.top + margin.bottom) >= image.get_height()) or
            ((margin.left + margin.right) >= image.get_width())):
            raise ValueError("margin may not overlap")

        self._margin = margin

        pos_x = [
            0,
            margin.left,
            image.get_width() - margin.right,
            image.get_width()
        ]
        pos_y = [
            0,
            margin.top,
            image.get_height() - margin.bottom,
            image.get_height()
        ]

        self._min_size = Size(
            margin.left + margin.right,
            margin.top + margin.bottom
        )

        self._elements = []
        for i in range(3):
            line = []
            for j in range(3):
                element = pygame.Surface((pos_x[j + 1] - pos_x[j], pos_y[i + 1] - pos_y[i]),
                                         pygame.HWSURFACE | pygame.SRCALPHA)
                element.blit(image, (0, 0), (pos_x[j], pos_y[i], element.get_width(), element.get_height()))
                line.append(element)
            self._elements.append(line)

        # Todo: Remove the pygame.Surface inheritance
        pygame.Surface.__init__(self, image.get_size(), pygame.HWSURFACE | pygame.SRCALPHA)
        self.blit(image, (0, 0))

    @deprecated(version='0.5', reason="Direct surface resize in deprecated, pleas use generate instead")
    def resize(self, size: tuple[int, int]):
        if not internal.correct_tuple(size, int, 2):
            raise TypeError("size need to be a (int width, int height)")

        size = (max(size[0], self.min_size.width), max(size[1], self.min_size.height))
        pygame.Surface.__init__(self, size, pygame.HWSURFACE | pygame.SRCALPHA)
        pos_y = [
            0,
            self._margin.top,
            size[1] - self._margin.bottom
        ]
        pos_x = [
            0,
            self._margin.left,
            size[0] - self._margin.right
        ]
        for i in range(3):
            for j in range(3):
                to_blit = self._elements[j][i]
                if i == 1:
                    to_blit = pygame.transform.scale(to_blit, (pos_x[2] - pos_x[1], to_blit.get_height()))
                if j == 1:
                    to_blit = pygame.transform.scale(to_blit, (to_blit.get_width(), pos_y[2] - pos_y[1]))
                self.blit(to_blit, (pos_x[i], pos_y[j]))

    @versionadded(version='0.5', reason="Replace resize to reduce the use of similar surfaces in the memory")
    def generate(
            self,
            dest: pygame.Surface,
            rect: Rect,
            with_top: bool = True,
            with_left: bool = True,
            with_bottom: bool = True,
            with_right: bool = True
    ):
        margin = Margin(
            self._margin.top if with_top else 0,
            self._margin.left if with_left else 0,
            self._margin.bottom if with_bottom else 0,
            self._margin.right if with_right else 0
        )
        size = Size(max(rect.size.width, self.min_size.width), max(rect.size.height, self.min_size.height))
        pos_y = [
            0,
            margin.top,
            size.height - margin.bottom
        ]
        pos_x = [
            0,
            margin.left,
            size.width - margin.right
        ]

        x = rect.position.x + pos_x[1]
        y = rect.position.y + pos_y[1]
        width = pos_x[2] - pos_x[1]
        height = pos_y[2] - pos_y[1]
        # Nodes blit
        for i in [0, 2]:
            for j in [0, 2]:
                if margin.from_index(i+1) and margin.from_index(j):
                    dest.blit(self._elements[j][i], (rect.position.x + pos_x[i], rect.position.y + pos_y[j]))
        # Edges blit
        for i in [0, 2]:
            dest.blit(
                pygame.transform.scale(self._elements[i][1], (width, self._elements[i][1].get_height())),
                (x, rect.position.y + pos_y[i])
            )
            dest.blit(
                pygame.transform.scale(self._elements[1][i], (self._elements[1][i].get_width(), height)),
                (rect.position.x + pos_x[i], y)
            )
        # Center surface
        dest.blit(
            pygame.transform.scale(self._elements[1][1], (width, height)),
            (x, y)
        )

    @deprecated
    def get_min_size(self):
        return self._min_size

    @property
    def min_size(self) -> Size:
        return self._min_size

    @property
    def margin(self) -> Margin:
        return self._margin


if __name__ == "__main__":
    frame = Frame(pygame.image.load("../resource/MainPack/Images/card_bg.png"), Margin(2, 2, 2, 2))

    pygame.init()

    win = pygame.display.set_mode((300, 300))
    surf = pygame.Surface((100, 100))
    surf.fill((255, 255, 255))

    frame.generate(
        surf,
        Rect(Position(0, 0), Size(80, 80)),
        with_top=False, with_left=False
    )

    pygame.transform.scale(surf, (300, 300), win)

    pygame.display.flip()

    pygame.time.wait(3000)

    pygame.quit()
