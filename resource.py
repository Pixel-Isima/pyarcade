################################################################################
# Filename: resource.py                                                        #
# Created by: Venceslas Duet                                                   #
# Created at: 05-04-2018                                                       #
# Last update at: 03-15-2022                                                   #
# Description: High level class for manage resource                            #
# Licence: GNU GPL v3.0 (See LICENSE.MD for more information)                  #
################################################################################

# TODO: Import metrics from configuration

import json

import pygame
from graphics import text, frame
from graphics.metrics import Size

import internal


class Resource:
    # Fonts Resources
    FONT_DEFAULT = 0

    font_names = ["DEFAULT"]
    fonts = []

    # Misc Image Resource
    MISC = 0

    MISC_ICON_32 = 0
    PIXEL_LOGO = 1

    misc_img_names = ["ICON", "PIXEL_LOGO"]
    misc_images = []

    # UI Image and color Resource
    UI = 1

    UI_TOOLBAR_BACKGROUND = 0
    UI_CLOCK_BACKGROUND = 1
    UI_CARD_BACKGROUND = 2
    UI_THUMBNAIL_BACKGROUND = 3

    ui_img_names = ["TOOLBAR_BACKGROUND", "CLOCK_BACKGROUND", "CARD_BACKGROUND", "THUMBNAIL_BACKGROUND"]
    ui_images = []

    # Icon Resource
    ICON = 2

    ICON_JOYSTICK = 0
    ICON_BUTTON_HOME = 1

    icon_img_names = ["JOYSTICK", "BUTTON_HOME"]
    icon_images = []

    # Metric resources
    METRIC_WINDOW_WIDTH = 0
    METRIC_WINDOW_HEIGHT = 1
    METRIC_TOOLBAR_HEIGHT = 2
    METRIC_CLOCK_MARGIN = 3
    METRIC_CARD_ICON_SIZE = 4
    METRIC_CARD_MARGIN = 5
    METRIC_CARD_PADDING = 6
    METRIC_BUTTON_ICON_MARGIN = 7

    metric_names = [
        "WINDOW_WIDTH",
        "WINDOW_HEIGHT",
        "TOOLBAR_HEIGHT",
        "CLOCK_MARGIN",
        "CARD_ICON_SIZE",
        "CARD_MARGIN",
        "CARD_PADDING",
        "BUTTON_ICON_MARGIN"
    ]
    metric = []

    # Color resources
    COLOR_BACKGROUND = 0

    color_names = [
        "background"
    ]
    colors = []

    _loaded = False
    _path = None

    use_smooth_resize = False

    @staticmethod
    def extractColors(names: list[str], desc_info: dict[str, list[int]]) -> list[list[int]]:
        length = len(names)
        ret = [[]] * length

        for i in range(length):
            if names[i] in desc_info:
                col = desc_info[names[i]]
                Resource.check_color(col)
                ret[i] = col
            else:
                raise ValueError("Color called {} is unavailable. Please check desc.json".format(names[i]))

        return ret

    @staticmethod
    def check_color(color : list[int]):
        length = 0
        for i in color:
            if 0 > i or i > 255:
                raise ValueError("color must be an array of integer with value between 0 and 255")
            length += 1
        if length < 3 or length > 4:
            raise ValueError("color must have 3 or 4 components (alpha is optional)")

    @staticmethod
    def extractImages(path: str, names: list[str], desc_info):
        length = len(names)
        ret = [None] * length

        for i in range(length):
            if names[i] in desc_info:
                ret[i] = Resource.generateImageElement(path, names[i], desc_info[names[i]])
            else:
                raise ValueError("Graphical element called {} for Misc module is unavailable. Please check desc.json".format(names[i]))

        return ret

    @staticmethod
    def extractMetrics(names, desc_info):
        length = len(names)
        ret = [None] * length

        for i in range(length):
            if names[i] in desc_info:
                tmp = desc_info[names[i]]
                try:
                    ret[i] = float(tmp)
                except:
                    raise ValueError("Value called {} have for value {} which is not an integer. Please check desc.json".format(names[i], tmp))
            else:
                raise ValueError("Metric called {} for Misc module is unavailable. Please check desc.json".format(names[i]))

        return ret

    @staticmethod
    def load(path):
        Resource._path = path
        descriptors = Resource.readFiles(path)
        Resource._loaded = False
        # Read descriptor for images
        if (
                "misc" in descriptors[1] and
                "ui" in descriptors[1] and
                "icon" in descriptors[1] and
                "color" in descriptors[1] and
                "metric" in descriptors[1]
        ):
            # Image Resource
            # Miscellaneous images
            Resource.misc_images = Resource.extractImages(descriptors[0], Resource.misc_img_names, descriptors[1]["misc"])

            # UI images
            Resource.ui_images = Resource.extractImages(descriptors[0], Resource.ui_img_names, descriptors[1]["ui"])

            # Menu images
            Resource.icon_images = Resource.extractImages(descriptors[0], Resource.icon_img_names, descriptors[1]["icon"])

            # Colors
            Resource.colors = Resource.extractColors(Resource.color_names, descriptors[1]["color"])

            # Metrics
            Resource.metric = Resource.extractMetrics(Resource.metric_names, descriptors[1]["metric"])
        else:
            raise ValueError("All modules (misc, ui and icon) are not allowed. Please check desc.json")

        try:
            Resource.use_smooth_resize = bool(descriptors[1]["use_smooth_resize"])
        except:
            Resource.use_smooth_resize = False

        # Read descriptor for fonts
        Resource.fonts = []
        for i in Resource.font_names:
            if i in descriptors[3]:
                Resource.fonts.append(Resource.generateFontElement(descriptors[2], i, descriptors[3][i]))
            else:
                raise ValueError("Element called " + i + " for font is unavailable. Please check font.json")

        Resource._loaded = True

    @staticmethod
    def reload():
        Resource._loaded = False
        Resource.load(Resource._path)

    @staticmethod
    def generateFontElement(path, name, data):
        if "image" in data:
            try:
                image_path = path + "/" + data["image"]
                image = pygame.image.load(image_path)
            except:
                raise ValueError(
                    "For create element, 'image' need to be valid path for valid image in " + name + " element")
            if "canvas" in data:
                if internal.correct_tuple(data["canvas"], int, 2):
                    return text.Text(image, Size.from_tuple(data["canvas"]), data["ascender-height"], data["baseline"])
                else:
                    raise ValueError(
                        "For create Font element, 'canvas' need to be (int width, int height) in " + name + " element")
            else:
                raise ValueError(
                    "For create Font element, it need to have 'canvas' as property in " + name + " element")
        else:
            raise ValueError("For create element, it need to have 'image' as property in " + name + " element")

    @staticmethod
    def generateImageElement(path: str, name: str, data):
        if "type" in data:
            if "image" in data:
                try:
                    image_path = path + "/" + data["image"]
                    image = pygame.image.load(image_path)
                except:
                    raise ValueError(
                        "For create element, 'image' need to be valid path for valid image in " + name + " element")
                if data["type"] == "Image":
                    return image
                elif data["type"] == "Frame":
                    if "margin" in data:
                        if internal.correct_tuple(data["margin"], int, 4):
                            return frame.Frame(image, frame.Margin.from_tuple(data["margin"]))
                        else:
                            raise ValueError(
                                "For create Frame element, 'margin' need to be (int top, int left, int bottom, int right) in " + name + " element")
                    else:
                        raise ValueError(
                            "For create Frame element, it need to have 'margin' as property in " + name + " element")
                elif data["type"] == "Animation":
                    if "canvas" in data:
                        if internal.correct_tuple(data["canvas"], int, 2):
                            # Actually not implemented
                            ret = pygame.Surface(data["canvas"], pygame.HWSURFACE | pygame.SRCALPHA)
                            ret.blit(image, (0, 0))
                            return ret
                        else:
                            raise ValueError(
                                "For create Animation element, 'canvas' need to be (int width, int height) in " + name + " element")
                    else:
                        raise ValueError(
                            "For create Animation element, it need to have 'canvas' as property in " + name + " element")
            else:
                raise ValueError("For create element, it need to have 'image' as property in " + name + " element")
        else:
            raise ValueError("For create element, it need to have 'type' as property in " + name + " element")

    @staticmethod
    def getImage(cat, name):
        if Resource._loaded:
            if cat == Resource.MISC:
                return Resource.misc_images[name]
            elif cat == Resource.UI:
                return Resource.ui_images[name]
            elif cat == Resource.ICON:
                return Resource.icon_images[name]
            else:
                raise ValueError("cat need to be between 0 and 2")
        else:
            raise ValueError("Resource is not initialized")

    @staticmethod
    def getFont(name) -> text.Text:
        if name in range(1):
            return Resource.fonts[name]
        else:
            raise ValueError("name need to be between 0 and 1")

    @staticmethod
    def getColor(name):
        return Resource.colors[name]

    @staticmethod
    def getMetric(name):
        return Resource.metric[name]

    @staticmethod
    def readJSON(file):
        lines = open(file, 'r').read().split('\n')
        line = ""
        for i in lines:
            line += i
        return json.loads(line)

    @staticmethod
    def readFiles(path):
        image_workspace = path + "/Images"
        image_descriptor_path = image_workspace + "/desc.json"
        image_descriptor = Resource.readJSON(image_descriptor_path)

        font_workspace = path + "/Images"
        font_descriptor_path = font_workspace + "/font.json"
        font_descriptor = Resource.readJSON(font_descriptor_path)

        return image_workspace, image_descriptor, font_workspace, font_descriptor
