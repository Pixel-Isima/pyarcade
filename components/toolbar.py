################################################################################
# Filename: components/toolbar.py                                              #
# Created by: Venceslas Duet                                                   #
# Created at: 03-14-2022                                                       #
# Last update at: 03-15-2022                                                   #
# Description: Toolbar component                                               #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import pygame

from graphics.layer import Layer, ClipPosition

from resource import Resource

from elements import BaseElement


class Toolbar(BaseElement):
    size = None

    def __init__(self):
        self.background = Resource.getImage(Resource.UI, Resource.UI_TOOLBAR_BACKGROUND)
        self.logo = Resource.getImage(Resource.MISC, Resource.PIXEL_LOGO)
        self.background_height = int(Resource.getMetric(Resource.METRIC_TOOLBAR_HEIGHT))
        self.toolbar_height = max(self.background_height, self.logo.get_height())

        self.layer = Layer((1, 1), 3)

        joystick_icon = Resource.getImage(Resource.ICON, Resource.ICON_JOYSTICK)

        self.bg_id = self.layer.add_surface(self.background, (0, 0), clip=(ClipPosition.LEFT, ClipPosition.BOTTOM))
        self.joystick_id = self.layer.add_surface(
            joystick_icon,
            (0, (self.background_height - joystick_icon.get_height()) // 2),
            clip=(ClipPosition.RIGHT, ClipPosition.BOTTOM)
        )
        self.logo_id = self.layer.add_surface(self.logo, (0, 0), clip=(ClipPosition.CENTER, ClipPosition.BOTTOM))

        self.resize((1, 1))

    def is_selectable(self):
        return False

    def resize(self, size):
        self.size = (max(1, size[0]), self.toolbar_height)

        pygame.Surface.__init__(self, self.size, pygame.HWSURFACE | pygame.SRCALPHA)

        self.background.resize((size[0], self.background_height))
        self.layer.resize(self.size)

        self.refresh()

    def hard_refresh(self):
        self.background = Resource.getImage(Resource.UI, Resource.UI_TOOLBAR_BACKGROUND)
        self.logo = Resource.getImage(Resource.MISC, Resource.PIXEL_LOGO)
        self.toolbar_height = max(self.background_height, self.logo.get_height())

        self.layer.change_surface(self.bg_id, self.background)
        self.layer.change_surface(self.logo_id, self.logo)
        self.layer.change_surface(self.joystick_id, Resource.getImage(Resource.ICON, Resource.ICON_JOYSTICK))

        self.resize(self.size)
        self.refresh()

    def refresh(self):
        self.layer.refresh()

        pygame.Surface.blit(self, self.layer, (0, 0))

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

    def enable(self):
        pass
