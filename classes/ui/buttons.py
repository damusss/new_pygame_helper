import pygame
from typing import Tuple, Union
from .text import UIText


class UIImageButton():
    """
    A button based on an image.
    """

    def __init__(self, surface, center_pos: Tuple[int, int] = (0, 0), topleft_pos: Tuple[int, int] = None, hitbox_inflate: Tuple[int, int] = (0, 0), on_click_func=None, allow_hold=False, click_button: int = 0):

        self._image = surface
        self.clicked = False
        self.hitbox_inflate = hitbox_inflate
        self.rect = self._image.get_rect(center=center_pos)
        if topleft_pos:
            self.rect.topleft = topleft_pos
        self.hitbox = self.rect.inflate(self.hitbox_inflate)
        self.on_click_function = on_click_func
        self.on_click_button = click_button
        self.allow_hold = allow_hold

        self.ui_group_offset = pygame.Vector2()

        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def refresh_rect(self):
        """
        Resize the rect to the image size.
        """
        self.rect = self._image.get_rect(center=self.rect.center)
        self.hitbox = self.rect.inflate(self.hitbox_inflate)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.refresh_hitbox()

    def draw(self, surface: pygame.Surface):
        """
        Draw the button and the image and text (both optional)
        """
        if self.visible:
            surface.blit(self.image, self.rect)

    def update(self) -> bool:
        """
        Check if the button is got clicked or is being clicked. If a function is passed in the init, it will be called.
        """
        action = False

        self.hitbox.center = self.rect.center

        pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        if self.hitbox.collidepoint(pos):
            if mouse[self.on_click_button]:
                if self.clicked == False or self.allow_hold == True:
                    action = True
                    self.clicked = True
                    if self.on_click_function:
                        self.on_click_function()

            if not mouse[self.on_click_button]:
                self.clicked = False

        return action

    def _ui_group_on_pos_change(self, group_pos):
        self.rect.topleft = (group_pos+self.ui_group_offset).xy

    def _ui_group_set_offset(self):
        self.ui_group_offset.xy = self.rect.topleft


class UITextButton():
    """
    A button based on a text object.
    """

    def __init__(self, text: UIText, hitbox_inflate: Tuple[int, int] = (0, 0), on_click_func=None, allow_hold=False, click_button: int = 0):
        self.clicked = False

        self.text = text
        self.hitbox_inflate = hitbox_inflate
        self.hitbox = self.text.rect.inflate(self.hitbox_inflate)
        self.text.button = self
        self.on_click_function = on_click_func
        self.on_click_button = click_button
        self.allow_hold = allow_hold

        self.ui_group_offset = pygame.Vector2()

        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def refresh_hitbox(self):
        """
        Refresh the hitbox on the rect size.
        """
        self.hitbox = self.text.rect.inflate(self.hitbox_inflate)

    def draw(self, surface: pygame.Surface):
        """
        Draw the button and and text.
        """
        if self.visible:
            self.text.draw(surface)

    def update(self) -> bool:
        """
        Check if the button is got clicked or is being clicked. If a function is passed in the init, it will be called.
        """
        action = False

        self.hitbox.center = self.text.rect.center

        pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        if self.hitbox.collidepoint(pos):
            if mouse[self.on_click_button]:
                if self.clicked == False or self.allow_hold == True:
                    action = True
                    self.clicked = True
                    if self.on_click_function:
                        self.on_click_function()

            if not mouse[self.on_click_button]:
                self.clicked = False

        return action

    def _ui_group_on_pos_change(self, group_pos):
        self.text._ui_group_on_pos_change(group_pos)

    def _ui_group_set_offset(self):
        self.text._ui_group_set_offset()
        self.ui_group_offset.xy = self.text.rect.topleft
