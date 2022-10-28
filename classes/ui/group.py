import pygame
from typing import Tuple, List, Union
from . import text, inputbox, buttons, statusbar, image,checkbox,slider,dropdown


class UIGroup():
    def __init__(self, position, hitbox_width=None, hitbox_height=None, on_drag_func=None, drag_button=0):
        self.elements = []
        self.position = pygame.Vector2(position)
        if hitbox_width:
            self.hitbox = pygame.Rect(
                self.position.x, self.position.y, hitbox_width, hitbox_height)
        self.was_pressing = False
        self.drag_rel_pos = pygame.Vector2()

        self.on_drag = on_drag_func
        self.button = drag_button

        self.visible = True
        
        self.was_pressing_outside = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def add(self, *elements):
        for element in elements:
            if not isinstance(element, (text.UIText, inputbox.UIInputBox, buttons.UIImageButton, buttons.UITextButton, statusbar.UIStatusBar, image.UIImage,checkbox.UICheckBox,slider.UISlider,dropdown.UIDropDown)):
                raise TypeError(
                    f"Element can only be of types Text, InputBox, ImageButton, TextButton, StatusBar, Image, CheckBox, Slider, DropDown.")
            self.elements.append(element)
            element._ui_group_set_offset()
            element._ui_group_on_pos_change(self.position)

    def draw(self, surface):
        if self.visible:
            for e in self.elements:
                e.draw(surface)

    def update(self):
        if self.visible:
            self.update_drag()
            for e in self.elements:
                e.update()

    def update_elements_pos(self):
        for e in self.elements:
            e._ui_group_on_pos_change(self.position)

    def set_pos(self, topleft_pos):
        self.position.xy = topleft_pos
        self.update_elements_pos()

    def move(self, amount_x, amount_y):
        self.position.x += amount_x
        self.position.y += amount_y
        self.update_elements_pos()

    def update_drag(self):
        mouse = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if mouse[self.button]:
            if self.hitbox.collidepoint(pos[0], pos[1]) or self.was_pressing:
                if not self.was_pressing_outside:
                    if not self.was_pressing:
                        self.was_pressing = True
                        self.drag_rel_pos.xy = (
                            pos[0]-self.position.x, pos[1]-self.position.y)
                    else:
                        self.position.xy = (
                            pos[0]-self.drag_rel_pos.x, pos[1]-self.drag_rel_pos[1])
                        self.hitbox.topleft = self.position.xy
                        self.update_elements_pos()
                        if self.on_drag:
                            self.on_drag()
            else:
                self.was_pressing = False
                self.was_pressing_outside = True
        if not mouse[self.button]:
            self.was_pressing = False
            self.was_pressing_outside = False
