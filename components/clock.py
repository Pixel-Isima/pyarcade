################################################################################
# Filename: components/clock.py                                                #
# Created by: Venceslas Duet                                                   #
# Created at: 03-14-2022                                                       #
# Last update at: 03-15-2022                                                   #
# Description: Clock component                                                 #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import pygame
from datetime import datetime

from graphics.layer import Layer, ClipPosition

from resource import Resource

from elements import BaseElement


class Clock(BaseElement):
    def enable(self):
        pass

    def disable(self):
        pass

    def set_hover(self):
        pass

    def set_active(self):
        pass

    def set_normal(self):
        pass

    def event_enter(self):
        pass

    def event_left(self):
        pass

    def event_right(self):
        pass

    def event_top(self):
        pass

    def event_bottom(self):
        pass

    def event_mouse_hover(self, pos):
        pass

    def event_mouse_click(self, pos, button):
        pass

    def event_mouse_leave(self):
        pass

    def event_mouse_scroll(self, pos, amount):
        pass

    def __init__(self):
        self.time = (0, 0)
        self.background = Resource.getImage(Resource.UI, Resource.UI_CLOCK_BACKGROUND)
        self.font = Resource.getFont(Resource.FONT_DEFAULT)
        self.lateral_margin = 4

        self.layer = Layer((1, 1), 2)

        self.layer.add_surface(self.background, (0, 0), clip=(ClipPosition.CENTER, ClipPosition.TOP))
        self.clock_id = self.layer.add_surface(pygame.Surface((1, 1)), (0, 2), clip=(ClipPosition.CENTER, ClipPosition.TOP))

        self.refresh()

    def is_selectable(self):
        return False

    def resize(self, size):
        pass

    def update_hour(self) -> bool:
        now = datetime.now()
        hour, minute = self.time

        if now.hour != hour or now.minute != minute:
            self.time = (now.hour, now.minute)
            return True
        else:
            return False

    def refresh(self):
        hour, minute = self.time
        clock = self.font.gen_text("{:02}:{:02}".format(hour, minute))
        size = (clock.get_width() + 2*self.lateral_margin, self.background.get_height())

        self.background.resize(size)
        pygame.Surface.__init__(self, size, pygame.HWSURFACE | pygame.SRCALPHA)

        self.layer.change_surface(self.clock_id, clock)
        self.layer.resize(size)
        self.layer.refresh()

        pygame.Surface.blit(self, self.layer, (0, 0))
