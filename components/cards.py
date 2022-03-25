from __future__ import annotations

import pygame

from elements import BaseElement
from resource import Resource
from graphics.metrics import Rect, Position, Size
from graphics import Frame
from gamedb import CardInfo

class Cards(BaseElement):
    _elements : list[CardInfo]
    _length : int
    _position : int
    _size : Size
    _resized : True

    def __init__(self, elements : list[CardInfo], size: Size):
        super(Cards, self).__init__(size.tuple, pygame.SRCALPHA)

        self._elements = elements
        self._length = len(elements)
        self._position = 0
        self._size = size
        self._resized = True

        self.refresh()

    @staticmethod
    def generate_card(info: CardInfo, active : bool) -> pygame.Surface:
        padding = Resource.getMetric(Resource.METRIC_CARD_PADDING)
        icon_size = Resource.getMetric(Resource.METRIC_CARD_ICON_SIZE)
        background: Frame = Resource.getImage(Resource.UI, Resource.UI_CARD_BACKGROUND)
        thumbnail_bg: Frame = Resource.getImage(Resource.UI, Resource.UI_THUMBNAIL_BACKGROUND)

        width = Cards.card_width()
        height = padding

        title_surface = Resource.getFont(Resource.FONT_DEFAULT).gen_text(info.title)
        title_width = min(title_surface.get_width(), icon_size)
        title_rect = Rect(
            Position(padding + (icon_size - title_width) // 2, padding),
            Size(title_width, title_surface.get_height())
        )

        height += title_surface.get_height() + padding

        thumbnail_frame_rect = Rect(
            Position(
                padding - thumbnail_bg.margin.left,
                height - thumbnail_bg.margin.top
            ),
            Size(
                icon_size + thumbnail_bg.margin.left + thumbnail_bg.margin.right,
                icon_size + thumbnail_bg.margin.top + thumbnail_bg.margin.bottom
            )
        )

        thumbnail_rect = Rect(
            Position(padding, height),
            Size(icon_size, icon_size)
        )

        height += icon_size + padding

        action = None
        action_rect = Rect(Position(0, 0), Size(0, 0))

        if active:
            action_title = Resource.getFont(Resource.FONT_DEFAULT).gen_text("Jouer")
            action_icon = Resource.getImage(Resource.ICON, Resource.ICON_BUTTON_HOME)

            buf_w = min(action_title.get_width() + action_icon.get_width(), icon_size)
            buf_h = max(action_title.get_height(), action_icon.get_height())

            action = pygame.Surface((buf_w, buf_h), pygame.SRCALPHA)

            x = 0
            y = (buf_h - action_icon.get_height()) // 2

            action.blit(action_icon, (x, y))

            x = action_icon.get_width() + Resource.getMetric(Resource.METRIC_BUTTON_ICON_MARGIN)
            y = (buf_h - action_title.get_height()) // 2

            action.blit(action_title, (x, y))

            action_rect = Rect(
                Position(padding + (icon_size - buf_w) // 2, height),
                Size(buf_w, buf_h)
            )

            height += buf_h + padding

        ret = pygame.Surface((width, height), pygame.SRCALPHA)

        background.generate(ret, Rect(Position(0, 0), Size(width, height)))

        ret.blit(title_surface, title_rect.tuple, Rect(Position(0,0), title_rect.size).tuple)

        thumbnail_bg.generate(ret, thumbnail_frame_rect)

        ret.blit(info.thumbnail, thumbnail_rect.tuple)

        if active:
            ret.blit(action, action_rect.tuple)

        return ret

    @staticmethod
    def card_width() -> int:
        padding = Resource.getMetric(Resource.METRIC_CARD_PADDING)
        icon_size = Resource.getMetric(Resource.METRIC_CARD_ICON_SIZE)
        return 2 * padding + icon_size

    def resize(self, size):
        self._resized = True
        self._size = size

    def hard_refresh(self):
        pass

    def refresh(self):
        import math
        from random import randint

        card_margin = Resource.getMetric(Resource.METRIC_CARD_MARGIN)

        width = self._size.width

        card_area_width = Cards.card_width() + card_margin

        shown_card_number = int(math.floor(float(width) / float(card_area_width))) + 2

        if shown_card_number % 2 == 0:
            shown_card_number += 1

        elements = []
        height = 0
        content_width = 0

        for i in range(shown_card_number):
            idx = (i - shown_card_number // 2 + self._position) % self._length

            card = Cards.generate_card(self._elements[idx], i == shown_card_number // 2)
            elements.append(card)

            height = max(height, card.get_height())
            content_width += card_area_width

        if self._resized:
            pygame.Surface.__init__(self, (width, height), pygame.SRCALPHA)

        self.fill((0,0,0,0))

        x = (card_margin + width - content_width) // 2

        for i in elements:
            y = (height - i.get_height()) // 2

            self.blit(i, (x, y))

            x += card_area_width

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

    def is_selectable(self):
        pass

    def event_enter(self):
        pass

    def event_left(self):
        self._position = (self._position - 1) % self._length

    def event_right(self):
        self._position = (self._position + 1) % self._length

    def event_top(self):
        pass

    def event_bottom(self):
        pass

if __name__ == "__main__":
    pygame.init()

    Resource.load("../resource/MainPack")

    cards = Cards([
        CardInfo.generate_random(),
        CardInfo.generate_random(),
        CardInfo.generate_random(),
        CardInfo.generate_random()
    ], Size(640, 320))

    size = (
        cards.get_width() * 2,
        cards.get_height() * 2
    )

    window = pygame.display.set_mode(size)

    pygame.transform.scale(cards, size, window)

    pygame.display.flip()

    pygame.time.wait(5000)

    cards.event_left()

    cards.refresh()
    pygame.transform.scale(cards, size, window)

    pygame.display.flip()

    pygame.time.wait(5000)

    pygame.quit()


