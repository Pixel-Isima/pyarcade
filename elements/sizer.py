from .base import BaseElement


class Sizer(BaseElement):
    INNER_BOX = 1000
    OUTER_BOX = 1001

    # Sizer methods
    def append(self, element, margin): raise NotImplementedError()
    def count_elements(self): raise NotImplementedError()
    def get_selected_element(self): raise NotImplementedError()
    def get_element_rect(self, id, box_type): raise NotImplementedError()
    def count_selectable_elements(self): raise NotImplementedError()
    def select_element(self, element_id): raise NotImplementedError()
    def select_next(self): raise NotImplementedError()
    def select_back(self): raise NotImplementedError()
    def deselect(self): raise NotImplementedError()
    def force_horizontal(self): raise NotImplementedError()
    def force_vertical(self): raise NotImplementedError()

    # BaseElement methods
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
