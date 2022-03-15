################################################################################
# Filename: graphics/text.py                                                   #
# Created by: Venceslas Duet                                                   #
# Created at: 03-27-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: High level class for create surface from string                 #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import pygame

import internal


class Text:
    def __init__(self, font, letter_size):
        if not isinstance(font, pygame.Surface):
            raise TypeError("font needs to be a pygame.Surface")
        if not internal.correct_tuple(letter_size, int, 2):
            raise TypeError("letter_size needs to be (int width, int height)")
        if (font.get_width() % letter_size[0] != 0 or
                font.get_height() % letter_size[1] != 0):
            raise TypeError("font must have size proportional size of letter_size")
        self.font = font
        self.canvas = letter_size
        self.nb_x = font.get_width() // letter_size[0]
        self.nb_y = font.get_height() // letter_size[1]
        self.color = None

    def gen_text(self, text):
        if not isinstance(text, str):
            raise TypeError("text needs to be a string")
        bts = []
        nl = 0
        actual = 0
        maximum = 0
        for i in text:
            if i == "\n":
                nl = nl + 1
                maximum = max(maximum, actual)
                actual = 0
            else:
                actual = actual + 1
            bts.append(ord(i))
        maximum = max(maximum, actual)
        ret = pygame.Surface((maximum * self.canvas[0], (nl + 1) * self.canvas[1]),
                             pygame.HWSURFACE | pygame.SRCALPHA)
        current = 0
        line = 0
        for i in text:
            if i == "\n":
                line = line + 1
                current = 0
            else:
                ret.blit(self.gen_letter(ord(i)), (current * self.canvas[0],
                                                   line * self.canvas[1]))
                current += 1

        if self.color is not None:
            ret.fill(self.color, None, pygame.BLEND_RGB_MIN)

        return ret

    def gen_letter(self, letter_id):
        if not isinstance(letter_id, int):
            raise TypeError("letter_id needs to be a integer")
        if letter_id < 0 or letter_id >= (self.nb_x * self.nb_y):
            raise TypeError("letter_id needs to have value between 0 and", (self.nb_x * self.nb_y))
        pos_x = letter_id % self.nb_x
        pos_y = letter_id // self.nb_x
        ret = pygame.Surface(self.canvas, pygame.HWSURFACE | pygame.SRCALPHA)
        ret.blit(self.font, (0, 0), (pos_x * self.canvas[0], pos_y * self.canvas[1], self.canvas[0], self.canvas[1]))
        return ret.copy()

    def set_color(self, color):
        if not (isinstance(color, pygame.Color) or color is None):
            raise TypeError("color needs to be a pygame.Color")
        self.color = color

    def clone(self):
        return Text(self.font, self.canvas)
