################################################################################
# Filename: main.py                                                            #
# Created by: Venceslas Duet                                                   #
# Created at: 04-07-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: Main file for the interface                                     #
# Licence: None                                                                #
################################################################################

import os
import pygame

from resource import Resource

from graphics import layer, background

import config
from components import Toolbar, Clock


class Game:
    # Definition of the launcher's states
    LAUNCHER_MENU = 0
    IN_GAME = 1

    def __init__(self):
        self.refresh = None
        self.ratio = None
        self.last_hover_element = None

        # Load resources
        Resource.load("MainPack")

        # Load the launcher's configuration file
        config.Config.load()

        # Setting the icon and the title of the launcher
        pygame.display.set_icon(Resource.getImage(Resource.MISC, Resource.MISC_ICON_32))
        pygame.display.set_caption("pyArcade launcher")

        # Hide cursor
        # pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

        # Setting the minimal page size
        # TODO: Use theme metrics instead
        self.minsize = (200, 200)

        # Platform hack to support HiDPI screens
        if os.name == "nt":
            from ctypes import windll
            windll.user32.SetProcessDPIAware()
            self.screen_size = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        else:
            self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        # Initialize the launcher modules
        # TODO: Adapter à la borne
        self.game = None

        # Initializing graphical objects
        self.window = None
        self.draw_canvas = layer.Layer(self.minsize, 5, 0)
        self.background = background.Background(self.minsize, Resource.getColor(Resource.COLOR_BACKGROUND))
        self.toolbar = Toolbar()
        self.clock = Clock()

        # Initializing the software state variables
        self.run = False
        self.err = False
        self.errName = ""

        # Resizing the window
        self.resize(self.get_size())

        # Initializing layers
        self.background_id = self.draw_canvas.add_surface(self.background, (0, 0), 0)
        self.toolbar_id = self.draw_canvas.add_surface(self.toolbar, (0, 0), clip=(layer.ClipPosition.LEFT, layer.ClipPosition.BOTTOM))
        self.clock_id = self.draw_canvas.add_surface(self.clock, (0, 0), clip=(layer.ClipPosition.CENTER, layer.ClipPosition.TOP))

    def resize(self, new_size):
        # TODO: Avoid the vertical line at the right of the screen
        # Checking the size of the window
        if new_size[0] < self.minsize[0] or new_size[1] < self.minsize[1]:
            if new_size[0] < self.minsize[0]:
                new_size = (self.minsize[0], new_size[1])
            if new_size[1] < self.minsize[1]:
                new_size = (new_size[0], self.minsize[1])

        new_size_ratio = new_size[0] / new_size[1]
        minsize_ratio = self.minsize[0] / self.minsize[1]
        self.ratio = new_size_ratio / minsize_ratio

        size = self.minsize
        if self.ratio < 1:
            size = (self.minsize[0], int(self.minsize[1] / self.ratio))
        elif self.ratio > 1:
            size = (int(self.minsize[0] * self.ratio), self.minsize[1])

        # Resize elements
        self.background.resize(size)
        self.toolbar.resize(size)
        self.draw_canvas.resize(size)

        if self.run:
            self.create_window()

        os.environ["SDL_VIDEO_CENTERED"] = '1'

    def create_window(self):
        self.window = pygame.display.set_mode(self.get_size(),
#                                              pygame.FULLSCREEN |
                                              pygame.DOUBLEBUF | pygame.HWSURFACE)

    def get_size(self):
        return self.screen_size

    def main(self):
        pygame.init()
        pygame.key.set_repeat(400, 100)

        self.refresh = True
        self.run = True
        self.create_window()
        self.last_hover_element = -1

        step = 0

        # TODO: Use a specific function managing inputs

        while self.run:
            # k_up, k_down, k_right, k_left, k_enter, k_shift = False, False, False, False, False, False
            k_esc = False
            reload_pressed = False
            hard_refresh = False

            for event in [pygame.event.wait(1000)] + pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.run = False
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE: k_esc = True
                            case pygame.K_r:
                                if not reload_pressed:
                                    reload_pressed = True
                                    Resource.load("MainPack")
                                    hard_refresh = True
                    case pygame.KEYUP:
                        match event.key:
                            case pygame.K_r:
                                reload_pressed = False

            if k_esc:
                self.run = False

            if self.clock.update_hour():
                self.refresh = True

            if hard_refresh:
                self.background.change_color(Resource.getColor(Resource.COLOR_BACKGROUND))
                self.toolbar.hard_refresh()
                self.clock.refresh()

                self.refresh = True

            if self.refresh or step < 2:
                self.refresh = False

                if step < 1:
                    step += 1

                self.clock.refresh()
                self.draw_canvas.change_surface(self.clock_id, self.clock)
                self.draw_canvas.refresh()

                to_render = pygame.transform.scale(self.draw_canvas, self.get_size())
                self.window.blit(to_render, (0, 0))

                pygame.display.flip()

        config.Config.save()
        pygame.quit()


if __name__ == "__main__":
    # Start game
    game = Game()
    game.main()
