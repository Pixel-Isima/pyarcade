################################################################################
# Filename: graphics/frame.py                                                  #
# Created by: Venceslas Duet                                                   #
# Created at: 04-07-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: base UI system for create zoom framed image                     #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import pygame

import internal


class Frame(pygame.Surface):
    def __init__(self, image, margin=(0, 0, 0, 0)):
        if not isinstance(image, pygame.Surface):
            raise TypeError("image need to be pygame.Surface")
        if not internal.correct_tuple(margin, int, 4):
            raise TypeError("margin need to be (int top, int right, int bottom, int left)")
        if ((margin[0] + margin[2]) >= image.get_height()) or ((margin[1] + margin[3]) >= image.get_width()):
            raise ValueError("margin may not overlap")
        self.margin = margin
        pos_y = [
            0,
            margin[0],
            image.get_height() - margin[2],
            image.get_height()
        ]
        pos_x = [
            0,
            margin[1],
            image.get_width() - margin[3],
            image.get_width()
        ]
        self.min_size = (margin[1] + margin[3]), (margin[0] + margin[2])
        self.elements = list()
        for i in range(3):
            line = list()
            for j in range(3):
                element = pygame.Surface((pos_x[j + 1] - pos_x[j], pos_y[i + 1] - pos_y[i]),
                                         pygame.HWSURFACE | pygame.SRCALPHA)
                element.blit(image, (0, 0), (pos_x[j], pos_y[i], element.get_width(), element.get_height()))
                line.append(element)
            self.elements.append(line)
        pygame.Surface.__init__(self, image.get_size(), pygame.HWSURFACE | pygame.SRCALPHA)
        self.blit(image, (0, 0))

    def resize(self, size):
        if not internal.correct_tuple(size, int, 2):
            raise TypeError("size need to be a (int width, int height)")
        size = (max(size[0], self.min_size[0]), max(size[1], self.min_size[1]))
        pygame.Surface.__init__(self, size, pygame.HWSURFACE | pygame.SRCALPHA)
        pos_y = [
            0,
            self.margin[0],
            size[1] - self.margin[2]
        ]
        pos_x = [
            0,
            self.margin[1],
            size[0] - self.margin[3]
        ]
        for i in range(3):
            for j in range(3):
                to_blit = self.elements[j][i]
                if i == 1:
                    to_blit = pygame.transform.scale(to_blit, (pos_x[2] - pos_x[1], to_blit.get_height()))
                if j == 1:
                    to_blit = pygame.transform.scale(to_blit, (to_blit.get_width(), pos_y[2] - pos_y[1]))
                self.blit(to_blit, (pos_x[i], pos_y[j]))

    def get_min_size(self):
        return self.min_size


class MultiStateFrame(pygame.Surface):
    def __init__(self, image, states, margin=(0, 0, 0, 0), default=0):
        if not isinstance(image, pygame.Surface):
            raise TypeError("image need to be pygame.Surface")
        if not isinstance(states, int):
            raise TypeError("states need to be int")
        if not internal.correct_tuple(margin, int, 4):
            raise TypeError("margin need to be (int top, int right, int bottom, int left)")
        if not isinstance(default, int):
            raise TypeError("default need to be int")
        if states <= 0 or states > image.get_height():
            raise ValueError("states need to be between 0 and height of image")
        if default not in range(states):
            raise ValueError("default need to be between 0 and states number")
        self.states = list()
        height = image.get_height() // states
        self.size = (image.get_width(), height)
        self.min_size = (margin[1] + margin[3]), (margin[0] + margin[2])
        self.actual_state = default

        for i in range(states):
            part = pygame.Surface((image.get_width(), height), pygame.HWSURFACE | pygame.SRCALPHA)
            part.blit(image, (0, 0), (0, height * i, image.get_width(), height))
            self.states.append(Frame(part, margin))

        self.refresh()

    def change_state(self, state):
        if not isinstance(state, int):
            raise TypeError("state need to be int")
        if state not in range(len(self.states)):
            raise ValueError("state need to be between 0 and states number")
        self.actual_state = state
        self.refresh()

    def resize(self, size):
        if not internal.correct_tuple(size, int, 2):
            raise TypeError("size need to be (int width, int height)")
        self.size = size
        for i in range(len(self.states)):
            self.states[i].resize(size)
        self.refresh()

    def get_min_size(self):
        return self.min_size

    def refresh(self):
        pygame.Surface.__init__(self, self.size, pygame.HWSURFACE | pygame.SRCALPHA)
        self.blit(self.states[self.actual_state], (0, 0))
