import pygame
from typing import Tuple, Union


class UIInputBox():
    """
    An easy way to implement an imput box, with events binding.
    """

    def __init__(self, box_rect: pygame.Rect, font: pygame.font.Font, start_text: str = 'Type Here', max_char: int = 25, color_active: Union[str, Tuple[int, int, int]] = "white", color_inactive: Union[str, Tuple[int, int, int]] = (200, 200, 200), antialiasing: bool = True, start_focused=False, bar_width: int = 2):
        self.rect = box_rect
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = self.color_inactive
        self.start_text = start_text
        self.text = start_text
        self.font = font
        self.antialiasing = antialiasing
        self.txt_surface = self.font.render(
            self.text, self.antialiasing, self.color)
        self.active = False
        self.max = max_char
        self.on_text_change = None
        self.on_text_increase = None
        self.on_text_decrease = None
        self.on_return_pressed = None
        test = self.font.render("MAX", True, "white")
        self.bar_rect = pygame.Rect(
            self.rect.left, self.rect.left, bar_width, test.get_height()+bar_width*2)
        del test
        self.bar_visible = True
        self.start_bar = pygame.time.get_ticks()
        self.bar_cooldown = 420
        self.bar_width = bar_width
        if start_focused:
            self.focus()

        self.ui_group_offset = pygame.Vector2()

        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def focus(self):
        """
        Focus the input box.
        """
        self.active = True
        self.color = self.color_active
        self.refresh_surface()

    def unfocus(self):
        """
        Unfocus the input box.
        """
        self.active = False
        self.color = self.color_inactive
        self.refresh_surface()

    def bind_events(self, on_text_change=None, on_text_increase=None, on_text_decrease=None, on_return_pressed=None):
        """
        Bind the events functions.
        """
        self.on_text_change = on_text_change
        self.on_text_increase = on_text_increase
        self.on_text_decrease = on_text_decrease
        self.on_return_pressed = on_return_pressed

    def handle_event(self, event: pygame.event.Event):
        """
        Process the events. Put this under the event loop.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
            self.refresh_surface()
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    before = self.text
                    self.text = self.text[:-1]
                    if len(self.text) != len(before):
                        if self.on_text_decrease:
                            self.on_text_decrease()
                        if self.on_text_change:
                            self.on_text_change()
                    if not self.text.strip():
                        self.set_text(self.start_text)
                    if before.strip() == self.start_text:
                        self.set_text("")
                elif event.key == pygame.K_RETURN:
                    if self.on_return_pressed:
                        self.on_return_pressed()
                else:
                    if self.text.strip() == self.start_text:
                        self.set_text("")
                    if not len(self.text) > self.max:
                        self.text += event.unicode
                        if self.on_text_increase:
                            self.on_text_increase()
                        if self.on_text_change:
                            self.on_text_change()
                # Re-render the text.
                self.refresh_surface()

    def refresh_surface(self):
        """
        Set the surface to the new text.
        """
        self.txt_surface = self.font.render(
            self.text, self.antialiasing, self.color)

    def draw(self, surface, text_offset: Tuple[int, int] = (0, 0), draw_rect: bool = True, rect_color: Union[str, Tuple[int, int, int]] = "copy_text", width: int = 5, draw_bar=True):
        """
        Draw the text and the rect (optional).
        """
        if self.visible:
            # Blit the text.
            surface.blit(self.txt_surface, (self.rect.x +
                                            text_offset[0], self.rect.y+text_offset[1]))
            # Blit the rect.
            if draw_rect:
                if rect_color == "copy_text":
                    rect_color = self.color
                pygame.draw.rect(surface, rect_color, self.rect, width)
            if draw_bar and self.active:
                if pygame.time.get_ticks()-self.start_bar >= self.bar_cooldown:
                    self.start_bar = pygame.time.get_ticks()
                    self.bar_visible = not self.bar_visible
                if self.bar_visible:
                    self.bar_rect.center = (self.rect.left+self.txt_surface.get_width(
                    )+text_offset[0]+2, self.rect.top+text_offset[1]+self.bar_rect.h/2-self.bar_width)
                    pygame.draw.rect(surface, self.color, self.bar_rect)

    def update(self):
        if self.visible:
            for e in pygame.event.get():
                self.handle_event(e)

    def get_text(self) -> str:
        """
        Return the text.
        """
        return self.text

    def set_text(self, text: str, ignore_max_char: bool = False):
        if len(text) <= self.max or ignore_max_char:
            self.text = text
        self.refresh_surface()

    def _ui_group_on_pos_change(self, group_pos):
        self.rect.topleft = (group_pos+self.ui_group_offset).xy

    def _ui_group_set_offset(self):
        self.ui_group_offset.xy = self.rect.topleft
