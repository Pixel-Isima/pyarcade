################################################################################
# Filename: direction.py                                                       #
# Created by: Venceslas Duet                                                   #
# Created at: 02-15-2018                                                       #
# Last update at: 02-16-2018                                                   #
# Description: Enum for set direction for animation or gradient class. This    #
# class work in pygame (SDL 2 python binding) library                          #
# Licence: None                                                                #
################################################################################

import enum


class Direction(enum.Enum):
    LTR = 0
    RTL = 1
    TTB = 2
    BTT = 3
