################################################################################
# Filename: elements/base.py                                                   #
# Created by: Venceslas Duet                                                   #
# Created at: 03-14-2022                                                       #
# Last update at: 03-15-2022                                                   #
# Description: Base class of graphical elements                                #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import pygame


class BaseElement(pygame.Surface):
    NORMAL = 0
    HOVER = 1
    ACTIVE = 2
    DISABLED = 3

    MOUSE_LEFT = 1
    MOUSE_MIDDLE = 2
    MOUSE_RIGHT = 3

    def resize(self, size): raise NotImplementedError()
    def enable(self): raise NotImplementedError()
    def disable(self): raise NotImplementedError()
    def set_hover(self): raise NotImplementedError()
    def set_active(self): raise NotImplementedError()
    def set_normal(self): raise NotImplementedError()
    def is_selectable(self): raise NotImplementedError()

    def refresh(self): raise NotImplementedError()
    def hard_refresh(self): raise NotImplementedError()

    # define events
    def event_enter(self): raise NotImplementedError()
    def event_left(self): raise NotImplementedError()
    def event_right(self): raise NotImplementedError()
    def event_top(self): raise NotImplementedError()
    def event_bottom(self): raise NotImplementedError()
