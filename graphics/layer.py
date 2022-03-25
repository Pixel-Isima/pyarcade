################################################################################
# Filename: graphics/layers.py                                                 #
# Created by: Venceslas Duet                                                   #
# Created at: 03-15-2018                                                       #
# Last update at: 03-16-2022                                                   #
# Description: High level class for manage layers and automatically update     #
# rendering of graphical elements                                              #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import pygame
import enum


class ClipPosition(enum.Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    TOP = 3
    MIDDLE = 4
    BOTTOM = 5


class LayerMember:
    def __init__(
            self,
            surface: pygame.Surface,
            pos: tuple[int, int],
            layer: int,
            clip: tuple[ClipPosition, ClipPosition],
            scale: float
    ):
        if scale <= 0:
            raise ValueError("scale needs to have a number strictly highest of 0")
        self.surface = surface
        self.layer = layer
        self.pos = pos
        self.clip = clip
        self.scale = scale

    def change_surface(self, surface: pygame.Surface):
        self.surface = surface

    def move(self, new_pos: tuple[int, int]):
        self.pos = new_pos

    def resize(self, scale: float):
        self.scale = scale

    def set_clip(self, clip: tuple[ClipPosition, ClipPosition]):
        self.clip = clip

    def get_position(self, canvas_size: tuple[int, int]):
        if canvas_size[0] <= 0 or canvas_size[1] <= 0:
            raise ValueError("canvas_size needs to have content upper to (0,0)")
        x = 0
        y = 0
        width = self.surface.get_width()
        height = self.surface.get_height()
        if self.scale != 1:
            width = width * self.scale
            height = height * self.scale
        if self.clip[0] == ClipPosition.LEFT:
            x = self.pos[0]
        elif self.clip[0] == ClipPosition.CENTER:
            x = (canvas_size[0] / 2 - width / 2) + self.pos[0]
        elif self.clip[0] == ClipPosition.RIGHT:
            x = (canvas_size[0] - width) - self.pos[0]
        if self.clip[1] == ClipPosition.TOP:
            y = self.pos[1]
        elif self.clip[1] == ClipPosition.MIDDLE:
            y = (canvas_size[1] / 2 - height / 2) + self.pos[1]
        elif self.clip[1] == ClipPosition.BOTTOM:
            y = (canvas_size[1] - height) - self.pos[1]
        return int(x), int(y)


class Layer(pygame.Surface):
    def __init__(
            self,
            canvas_size: tuple[int, int],
            layers: int,
            default_layer: int = 0
    ):
        if canvas_size[0] <= 0 or canvas_size[1] <= 0:
            raise ValueError("canvas_size needs to have content upper to (0,0)")
        if layers <= 0:
            raise ValueError("layers needs to be upper to 0")
        if default_layer not in range(layers):
            raise ValueError("default_layer needs to be between 0 and layers value")
        pygame.Surface.__init__(self, canvas_size, pygame.HWSURFACE |
                                pygame.SRCALPHA)
        self.surfaces = []
        self.layer_cnt = layers
        self.layer_show = []
        self.layer_modified = []
        self.layer = []
        for i in range(self.layer_cnt):
            self.layer_show.append(True)
            self.layer_modified.append(False)
            self.layer.append(pygame.Surface(canvas_size, pygame.HWSURFACE |
                                             pygame.SRCALPHA))

        self.default_layer = default_layer

    def add_surface(
            self,
            surface: pygame.Surface,
            position: tuple[int, int],
            layer: int = -1,
            clip: tuple[ClipPosition, ClipPosition] = (ClipPosition.LEFT, ClipPosition.TOP),
            zoom: float = 1.0
    ):
        if layer == -1:
            layer = self.default_layer
        if layer not in range(self.layer_cnt):
            raise ValueError("layer needs to be between 0 and layers value")
        self.surfaces.append(LayerMember(surface, position, layer, clip, zoom))
        self.layer_modified[layer] = True
        return len(self.surfaces) - 1

    def change_surface(self, index: int, surface: pygame.Surface):
        if index not in range(len(self.surfaces)):
            raise ValueError("index needs to be a surface list index")
        self.surfaces[index].change_surface(surface)
        self.layer_modified[self.surfaces[index].layer] = True

    def change_visibility(self, layer: int, visible: bool = True):
        if layer not in range(self.layer_cnt):
            raise ValueError("layer needs to be between 0 and layer count")
        self.layer_show[layer] = visible

    def refresh(self):
        self.fill(pygame.Color(0, 0, 0, 0))
        for i in range(self.layer_cnt):
            if self.layer_show[i]:
                self.update_layer(i)
                self.blit(self.layer[i], (0, 0))

    def update_layer(self, layer: int):
        if layer not in range(self.layer_cnt):
            raise ValueError("layer needs to be between 0 and layer count")
        if self.layer_modified[layer]:
            self.layer[layer].fill(pygame.Color(0, 0, 0, 0))
            for j in self.surfaces:
                if j.layer == layer:
                    pos = j.get_position(self.get_size())
                    surf = j.surface
                    if j.scale != 1:
                        surf = pygame.transform.scale(surf, (
                            int(surf.get_width() * j.scale), int(surf.get_height() * j.scale)))
                    self.layer[layer].blit(surf, pos)
            self.layer_modified[layer] = False

    def relative_move(self, index: int, pos: tuple[int, int]):
        if index not in range(len(self.surfaces)):
            raise ValueError("index needs to be between 0 and length of surfaces list")
        self.surfaces[index].pos = (self.surfaces[index].pos[0] + pos[0],
                                    self.surfaces[index].pos[1] + pos[1])
        self.layer_modified[self.surfaces[index].layer] = True

    def absolute_move(self, index: int, pos: tuple[int, int]):
        if index not in range(len(self.surfaces)):
            raise ValueError("index needs to be between 0 and length of surfaces list")
        self.surfaces[index].pos = pos
        self.layer_modified[self.surfaces[index].layer] = True

    def change_clip(self, index: int, clip: tuple[ClipPosition, ClipPosition]):
        self.surfaces[index].set_clip(clip)
        self.layer_modified[self.surfaces[index].layer] = True

    def resize(self, size: tuple[int, int]):
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("size needs to have content upper to (0,0)")
        pygame.Surface.__init__(self, size, pygame.HWSURFACE |
                                pygame.SRCALPHA)
        for i in range(self.layer_cnt):
            self.layer_modified[i] = True
            self.layer[i] = pygame.Surface(size, pygame.HWSURFACE | pygame.SRCALPHA)

    def get_rect(self, index: int):
        if index not in range(self.layer_cnt):
            raise ValueError("index needs to be between 0 and length of surfaces list")
        pos = self.surfaces[index].get_position(self.get_size())
        return (pos[0], pos[1], int(self.surfaces[index].surface.get_width() * self.surfaces[index].scale),
                int(self.surfaces[index].surface.get_height() * self.surfaces[index].scale))

    def relative_pos(self, index: int, pos: tuple[int, int]):
        # WTF?
        pos = self.surfaces[index].get_position(self.get_size())

    def focus_element(self, pos: tuple[int, int]):
        for i in range(self.layer_cnt):
            if self.layer_show[i]:
                for j in range(len(self.surfaces)):
                    if self.surfaces[j].layer == i:
                        layer_rect = self.get_rect(j)
                        if (layer_rect[0] >= pos[0] >= layer_rect[0] + layer_rect[2] and
                                layer_rect[1] >= pos[1] >= layer_rect[1] + layer_rect[3]):
                            return j
        return -1
