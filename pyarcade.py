#!/bin/python2

################################################################################
# Description: Main file for the interface                                     #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

import os

import pygame

import config
from components import Toolbar, Clock, Cards
from gamedb import GameDB
from graphics import layer, background, Size
from resource import Resource
from controller import Controllers, Axis


class Game:
    # Definition of the launcher's states
    LAUNCHER_MENU = 0
    IN_GAME = 1

    def _load_resources(self):
        # Load resources
        Resource.load(self._resource_pack_path)
        GameDB.load(self._game_info_path)

        # Setting the icon of the launcher
        pygame.display.set_icon(Resource.getImage(Resource.MISC, Resource.MISC_ICON_32))

        # Setting the title of the launcher
        pygame.display.set_caption("pyArcade launcher")

        # Hide cursor
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

        # Platform hack to support HiDPI screens
        if os.name == "nt":
            from ctypes import windll
            windll.user32.SetProcessDPIAware()
            self.screen_size = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        else:
            self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        # Setting the minimal page size
        self.minsize = Size(
            Resource.getMetric(Resource.METRIC_WINDOW_WIDTH),
            Resource.getMetric(Resource.METRIC_WINDOW_HEIGHT)
        )

        # Initializing graphical objects
        self.draw_canvas = layer.Layer(self.minsize.tuple, 5, 0)
        self.background = background.Background(self.minsize.tuple, Resource.getColor(Resource.COLOR_BACKGROUND))
        self.toolbar = Toolbar()
        self.clock = Clock()
        self.cards = Cards(GameDB.get_cards(), self.minsize)

        # Resizing the window
        self.resize(self.get_size())

        # Initializing layers
        self.background_id = self.draw_canvas.add_surface(self.background, (0, 0), 0)
        self.toolbar_id = self.draw_canvas.add_surface(self.toolbar, (0, 0),
                                                       clip=(layer.ClipPosition.LEFT, layer.ClipPosition.BOTTOM))
        self.clock_id = self.draw_canvas.add_surface(self.clock, (0, 0),
                                                     clip=(layer.ClipPosition.CENTER, layer.ClipPosition.TOP))
        self.card_id = self.draw_canvas.add_surface(self.cards, (0, (self.clock.get_height() - self.toolbar.get_height())//2),
                                                    clip=(layer.ClipPosition.CENTER, layer.ClipPosition.MIDDLE))


    def __init__(self, resource_pack_path, game_info_path):
        self.refresh = None
        self.ratio = None
        self.last_hover_element = None
        self._resource_pack_path = resource_pack_path
        self._game_info_path = game_info_path
        self._controller = Controllers()

        # Initializing graphical objects
        self.window = None

        # Initializing the software state variables
        self.run = False
        self.err = False
        self.errName = ""

        self._load_resources()

    def resize(self, new_size):
        # Checking the size of the window
        if new_size[0] < self.minsize.width or new_size[1] < self.minsize.height:
            if new_size[0] < self.minsize.width:
                new_size = (self.minsize.width, new_size[1])
            if new_size[1] < self.minsize.height:
                new_size = (new_size[0], self.minsize.height)

        new_size_ratio = new_size[0] / new_size[1]
        minsize_ratio = self.minsize.width / self.minsize.height
        self.ratio = new_size_ratio / minsize_ratio

        size = self.minsize
        if self.ratio < 1:
            size = (self.minsize.width, int(self.minsize.height / self.ratio))
        elif self.ratio > 1:
            size = (int(self.minsize.width * self.ratio), self.minsize.height)

        # Resize elements
        self.background.resize(size)
        self.toolbar.resize(size)
        self.cards.resize(Size.from_tuple(size))
        self.draw_canvas.resize(size)

        self.cards.refresh()

        if self.run:
            self.create_window()

        os.environ["SDL_VIDEO_CENTERED"] = '1'

    def create_window(self):
        self.window = pygame.display.set_mode(self.get_size(),
                                              pygame.FULLSCREEN |
                                              pygame.DOUBLEBUF | pygame.HWSURFACE)

    def get_size(self):
        return self.screen_size

    def get_input(self):
        k_esc = False
        k_left = False
        k_right = False
        k_launch = False
        k_refresh = False

        for event in [pygame.event.wait(1000)] + pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.run = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            k_esc = True
                        case pygame.K_LEFT:
                            k_left = True
                        case pygame.K_RIGHT:
                            k_right = True
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_r:
                            k_refresh = True
                        case pygame.K_KP_ENTER | pygame.K_RETURN:
                            k_launch = True
                case pygame.JOYAXISMOTION:
                    if self._controller.get_joystick_position(Axis.X_POSITIVE):
                        k_right = True
                    if self._controller.get_joystick_position(Axis.X_NEGATIVE):
                        k_left = True
                case pygame.JOYBUTTONUP:
                    self._controller.print_all()
                    k_launch = self._controller.get_validation_action()

        if k_esc:
            self.run = False

        if k_left:
            self.cards.event_left()
        elif k_right:
            self.cards.event_right()

        if k_left or k_right:
            self.cards.refresh()
            self.refresh = True

        return k_launch, k_refresh

    def _loop(self):
        pygame.init()
        pygame.key.set_repeat(400, 100)

        self.refresh = True
        self.run = True
        self.create_window()
        self.last_hover_element = -1

        step = 0

        while self.run:
            launch, refresh = self.get_input()

            if refresh:
                Resource.reload()
                return True

            if launch:
                GameDB.launch_game(self.cards.current)

            if self.clock.update_hour():
                self.refresh = True

                self.clock.refresh()

            if self.refresh or step < 2:
                self.refresh = False

                if step < 1:
                    step += 1

                self.draw_canvas.change_surface(self.clock_id, self.clock)
                self.draw_canvas.change_surface(self.card_id, self.cards)
                self.draw_canvas.refresh()

                self.blit_to_window(self.draw_canvas)

                pygame.display.flip()

        config.Config.save()
        pygame.quit()

        return False

    def blit_to_window(self, origin):
        if Resource.use_smooth_resize:
            pygame.transform.smoothscale(origin, self.window.get_size(), self.window)
        else:
            pygame.transform.scale(origin, self.window.get_size(), self.window)

    def loop(self):
        loop = True

        while loop:
            try:
                self._load_resources()
                loop = self._loop()
            except:
                pass

if __name__ == "__main__":
    # Start game
    game = Game("./resource/Voxel", "./data")
    game.loop()
