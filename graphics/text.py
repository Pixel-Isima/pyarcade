################################################################################
# Filename: graphics/text.py                                                   #
# Created by: Venceslas Duet                                                   #
# Created at: 03-27-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: High level class for create surface from string                 #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import pygame

from graphics.metrics import Size


class Text:
    _font: pygame.Surface
    _letter_size: Size
    _ascender_height: int
    _baseline: int

    _cols : int
    _rows : int

    def __init__(self, font : pygame.Surface, letter_size : Size, ascender_height : int, baseline : int):
        if baseline > letter_size.height or baseline < 0:
            raise ValueError("baseline must be between 0 and {}".format(letter_size.height))
        if ascender_height > letter_size.height - baseline or ascender_height < 1:
            raise ValueError("ascender_height must be between 1 and {}".format(letter_size.height - baseline))

        self._font = font
        self._letter_size = letter_size
        self._ascender_height = ascender_height
        self._baseline = baseline
        self._cols = font.get_width() // letter_size.width
        self._rows = font.get_height() // letter_size.height

    def gen_text(self, text : str, color: pygame.Color | None = None):
        bts = []
        nl = 0
        actual = 0
        maximum = 0

        top_offset = self._letter_size.height - self._ascender_height - self._baseline

        line_height = self._ascender_height + 2 * self._baseline
        letter_offset = self._baseline - top_offset

        if top_offset > self._baseline:
            line_height = self._ascender_height + 2 * top_offset
            letter_offset = 0

        for i in text:
            if i == "\n":
                nl = nl + 1
                maximum = max(maximum, actual)
                actual = 0
            else:
                actual = actual + 1
            bts.append(ord(i))

        maximum = max(maximum, actual)

        ret = pygame.Surface((
            maximum * self._letter_size.width,
            (nl + 1) * line_height
        ), pygame.HWSURFACE | pygame.SRCALPHA)

        current = 0
        line = 0

        for i in text:
            if i == "\n":
                line = line + 1
                current = 0
            else:
                ret.blit(self.gen_letter(ord(i)), (
                    current * self._letter_size.width,
                    line * line_height + letter_offset
                ))
                current += 1

        if color is not None:
            ret.fill(color, None, pygame.BLEND_RGB_MIN)

        return ret

    def gen_letter(self, letter_id : int):
        if letter_id < 0 or letter_id >= (self._cols * self._rows):
            raise TypeError("letter_id needs to have value between 0 and {}".format(self._cols * self._rows))

        pos_x = letter_id % self._cols
        pos_y = letter_id // self._rows

        ret = pygame.Surface(self._letter_size.tuple, pygame.HWSURFACE | pygame.SRCALPHA)

        ret.blit(self._font, (0, 0), (
            pos_x * self._letter_size.width,
            pos_y * self._letter_size.height,
            self._letter_size.width,
            self._letter_size.height
        ))

        return ret.copy()

    def clone(self):
        return Text(
            self._font,
            self._letter_size,
            self._ascender_height,
            self._baseline
        )
