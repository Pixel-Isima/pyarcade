########################################################################################################################
# Filename: box_sizer.py                                                                                               #
# Created by: Venceslas Duet                                                                                           #
# Created at: 04-10-2018                                                                                               #
# Last update at: 04-10-2018                                                                                           #
# Description: box sizer class system                                                                                  #
# Licence: None                                                                                                        #
########################################################################################################################

import pygame
import internal

from .sizer import Sizer
from .base import BaseElement

from graphics import Direction


class BoxSizer(Sizer):
    def __init__(self, size, direction=Direction.TTB):
        if not internal.correct_tuple(size, int, 2):
            raise TypeError("size need to be (int width, int height)")
        if not isinstance(direction, Direction):
            raise TypeError("direction need to be Direction")
        self.direction = direction
        self.size = size
        self.last_size = None
        self.elements = list()
        self.elements_pos = list()
        self.elements_margin = list()
        self.elements_selectable = list()
        self.selected = -1
        self.last_selected = -1

    def append(self, element, margin=(0, 0, 0, 0)):
        if not isinstance(element, BaseElement):
            raise TypeError("element need to be elements_base.BaseElement")
        if not internal.correct_tuple(margin, int, 4):
            raise TypeError("margin need to be (int top, int left, int bottom, int right")
        ret = len(self.elements)
        self.elements.append(element)
        self.elements_pos.append((0, 0))
        self.elements_margin.append(margin)
        self.elements_selectable.append(ret)
        return ret

    def resize(self, size):
        if not internal.correct_tuple(size, int, 2):
            raise TypeError("size need to be (int width, int height)")
        self.size = size

    def count_elements(self):
        return len(self.elements)

    def get_selected_element(self):
        if self.selected != -1:
            return self.elements_selectable[self.selected]
        else:
            return -1

    def get_element_rect(self, idx, box_type=Sizer.OUTER_BOX):
        if not box_type in range(Sizer.INNER_BOX, Sizer.OUTER_BOX + 1):
            raise TypeError("box_type need to be INNER_BOX or OUTER_BOX")
        if idx != -1:
            margin = self.elements_margin[idx]
            size = self.elements[idx].get_size()
            position = self.elements_pos[idx]
            if box_type == BoxSizer.INNER_BOX:
                return position[0], position[1], size[0], size[1]
            else:
                return (
                    position[0] - margin[1],
                    position[1] - margin[0],
                    size[0] + margin[1] + margin[3],
                    size[1] + margin[0] + margin[2]
                )
        else:
            return None

    def count_selectable_elements(self):
        return len(self.elements_selectable)

    def select_element(self, element_id):
        if not isinstance(element_id, int):
            raise TypeError("element_id need to be int")
        if element_id in range(len(self.elements_selectable)):
            self.selected = element_id
            self.toggle_select()
        else:
            raise ValueError("element_id need to be between 0 and the number of seletable elements")

    def select_next(self):
        self.selected = (self.selected + 1) % len(self.elements_selectable)
        self.toggle_select()

    def select_back(self):
        self.selected = (self.selected - 1) % len(self.elements_selectable)
        self.toggle_select()

    def deselect(self):
        self.selected = -1
        self.toggle_select()

    def toggle_select(self):
        if self.selected != self.last_selected:
            if self.selected >= 0:
                self.elements[self.elements_selectable[self.selected]].set_hover()
            if self.last_selected >= 0:
                self.elements[self.elements_selectable[self.last_selected]].set_normal()
            self.last_selected = self.selected

    def force_horizontal(self):
        return True if self.direction == Direction.LTR or self.direction == Direction.RTL else False

    def force_vertical(self):
        return True if self.direction == Direction.TTB or self.direction == Direction.BTT else False

    def prepare_surface(self):
        if self.direction == Direction.TTB or self.direction == Direction.BTT:
            surface_height = 0
            for i in range(len(self.elements)):
                self.elements[i].resize((self.size[0] - self.elements_margin[i][1] - self.elements_margin[i][3],
                                         self.elements[i].get_height()))
                self.elements_pos[i] = (self.elements_margin[i][1], surface_height + self.elements_margin[i][0])
                surface_height += (
                            self.elements_margin[i][0] + self.elements_margin[i][2] + self.elements[i].get_height())
            self.size = (self.size[0], surface_height)
        else:
            surface_width = 0
            for i in range(len(self.elements)):
                self.elements[i].resize((self.elements[i].get_width(),
                                         self.size[1] - self.elements_margin[i][0] - self.elements_margin[i][2]))
                self.elements_pos[i] = (surface_width + self.elements_margin[i][1], self.elements_margin[i][0])
                surface_width += (self.elements_margin[i][1] + self.elements_margin[i][3])
            self.size = (surface_width, self.size[1])

    def refresh(self):
        if self.last_size != self.size:
            self.prepare_surface()
            pygame.Surface.__init__(self, self.size, pygame.HWSURFACE | pygame.SRCALPHA)
            self.last_size = self.size
        for i in range(len(self.elements)):
            self.blit(self.elements[i], self.elements_pos[i])

    def event_enter(self):
        if self.selected != -1:
            self.elements[self.elements_selectable[self.selected]].event_entr()

    def event_left(self):
        if self.selected != -1:
            self.elements[self.elements_selectable[self.selected]].event_left()

    def event_right(self):
        if self.selected != -1:
            self.elements[self.elements_selectable[self.selected]].event_right()

    def enable(self): pass

    def disable(self): pass

    def set_hover(self): pass

    def set_active(self): pass

    def set_normal(self): pass

    def is_selectable(self): pass

    def hard_refresh(self): pass

    def event_top(self): pass

    def event_bottom(self): pass

