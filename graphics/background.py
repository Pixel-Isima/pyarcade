################################################################################
# Filename: graphics/background.py                                             #
# Created by: Venceslas Duet                                                   #
# Created at: 02-14-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: Class for generating size agnostic background. This class work  #
# in pygame (SDL 2 python binding) library                                     #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

# TODO: Implement image background support

import pygame


class Background(pygame.Surface):
    def __init__(self, size, plain_color=pygame.Color(0, 0, 0),
                 image=None,
                 image_width=-1, image_height=-1,
                 image_repeat_x=1, image_repeat_y=1):
        """!@brief Creates a new Gradient object

        The Gradient object that create quickly gradient in pygame.Surface

        @param size The background surface size
        @param plain_color The main colour of the background
        @param image The texture to draw as wallpaper. Is image=None then only the plain_color is shown
        @param image_width The width of the image. If image_width=-1 then the width is automatically calculated
        @param image_height The height of the image. If image_height=-1 then the height is automatically calculated
        """
        self.color = plain_color
        self.resize(size)

    def change_color(self, color):
        self.color = color
        self.resize(self.get_size())

    def resize(self, size):
        pygame.Surface.__init__(self, size)
        self.fill(self.color, (0, 0, size[0], size[1]))
