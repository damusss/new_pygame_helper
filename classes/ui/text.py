import pygame
from typing import Tuple, Union
from pygame.font import Font, SysFont


class UIText():
    """
    Easier way to draw some text. When some value changes, the image is resetted. 
    """

    def __init__(self, center_pos: Tuple[int, int] = (0, 0), topleft_pos: Tuple[int, int] = None, font: pygame.font.Font = None, text: str = "Text", color: Union[str, Tuple[int, int, int]] = "black", antialiasing: bool = True, bg_color: Union[str, Tuple[int, int, int]] = None, stick_topleft: bool = False):
        if font:
            self._font = font
        else:
            self._font = pygame.font.Font(None, 20)
        self._text = text
        self._color = color
        self._antialiasing = antialiasing
        self._bg_color = bg_color
        self.center_pos = center_pos
        self.topleft_pos = topleft_pos
        self.button = None
        self.stick_topleft = stick_topleft
        self.image = self._font.render(
            self._text, self._antialiasing, self._color, self._bg_color)
        if self.topleft_pos:
            self.rect = self.image.get_rect(topleft=self.topleft_pos)
        else:
            self.rect = self.image.get_rect(center=self.center_pos)

        self.ui_group_offset = pygame.Vector2()

        self.draw_outline = False

        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self):
        pass

    def setup_outline(self, outline_inflate: Tuple[int, int] = (7, 7), outline_color: Union[str, Tuple[int, int, int]] = "copy_text", outline_width: int = 2, outline_border_radius: int = 0, fill_outline_color=None):
        self.draw_outline = True
        self.outline_inflate = outline_inflate
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.outline_border_radius = outline_border_radius
        self.fill_outline_color = fill_outline_color

    def draw(self, surface: pygame.Surface):
        """
        Draw the text.
        """
        if self.visible:
            if self.draw_outline:
                if self.fill_outline_color:
                    if self.outline_color == "copy_text":
                        self.outline_color = self._color
                    pygame.draw.rect(surface, self.fill_outline_color, self.rect.inflate(
                        self.outline_inflate), 0, self.outline_border_radius)

            surface.blit(self.image, self.rect)
            if self.draw_outline:
                if self.outline_color == "copy_text":
                    self.outline_color = self._color
                pygame.draw.rect(surface, self.outline_color, self.rect.inflate(
                    self.outline_inflate), self.outline_width, self.outline_border_radius)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, f):
        self._font = f
        self.refresh_image()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = str(t)
        self.refresh_image()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, tc):
        self._color = tc
        self.refresh_image()

    @property
    def antialiasing(self):
        return self._antialiasing

    @antialiasing.setter
    def antialiasing(self, a):
        self._antialiasing = a
        self.refresh_image()

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, bc):
        self._bg_color = bc
        self.refresh_image()

    def refresh_image(self) -> None:
        """
        Reset the text image.
        """
        self.image = self._font.render(
            self._text, self._antialiasing, self._color, self._bg_color)
        if self.stick_topleft:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)
        if self.button:
            self.button.refresh_hitbox()

    def _ui_group_on_pos_change(self, group_pos):
        if self.stick_topleft:
            self.rect.topleft = (group_pos+self.ui_group_offset).xy
        else:
            self.rect.center = (group_pos+self.ui_group_offset).xy

    def _ui_group_set_offset(self):
        if self.stick_topleft:
            self.ui_group_offset.xy = self.rect.topleft
        else:
            self.ui_group_offset.xy = self.rect.center
