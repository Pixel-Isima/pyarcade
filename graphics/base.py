from __future__ import annotations

import pygame

from .metrics import Position, Size, Rect

class SurfaceBase:
    def get_subsurface(self, rect : Rect) -> SubSurface: raise NotImplementedError

    @property
    def size(self) -> Size: raise NotImplementedError

    @property
    def pos(self) -> Position: raise NotImplementedError

    @property
    def rect(self) -> Rect:
        return Rect(self.pos, self.size)

    def blit(self, other : SurfaceBase, rect: Rect):
        """
        Blit other into the Surface
        :param other: A Surface or SubSurface which is blitted into self
        :param rect: The position and the size of the blitted surface (for
        :return:
        """
        raise NotImplementedError

    def _get_pygame_surface(self) -> pygame.Surface:
        raise NotImplementedError


class Surface(SurfaceBase):
    _surface: pygame.Surface

    def __init__(self, size: Size):
        self._surface = pygame.Surface(size, pygame.SRCALPHA)

    def get_subsurface(self, rect: Rect) -> SubSurface:
        ret = SubSurface()
        ret._parent = self
        ret._inset_rect = rect

        return ret

    @property
    def size(self) -> Size:
        return Size.from_tuple(self._surface.get_size())

    @property
    def pos(self) -> Position:
        return Position(0, 0)

    def blit(self, other: SurfaceBase, rect: Rect):
        self._surface.blit(other._get_pygame_surface(), rect.tuple, other.rect.tuple)

    def _get_pygame_surface(self) -> pygame.Surface:
        return self._surface

class SubSurface(SurfaceBase):
    _parent: SurfaceBase
    _inset_rect: Rect

    def get_subsurface(self, rect: Rect) -> SubSurface:
        ret = SubSurface()
        ret._parent = self
        ret._inset_rect = rect

        return ret

    @property
    def size(self) -> Size:
        return self._inset_rect.size

    @property
    def pos(self) -> Position:
        return self._parent.pos + self._inset_rect.position

    @property
    def rect(self) -> Rect:
        return Rect(self.pos, self.size)

    def blit(self, other: SurfaceBase, rect: Rect):
        surface = self._get_pygame_surface()
        pass

    def _get_pygame_surface(self) -> pygame.Surface:
        return self._parent._get_pygame_surface()

class GraphicalBase:
    def add_to_surface(self, other: SurfaceBase, rect: Rect): raise NotImplementedError
