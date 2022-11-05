import sys
#sys.path.append("..")
from ..graphics.surface import *
import pygame
from typing import Tuple


"""
Contains the Background class.
"""


class Background():
    """
    A little bit easier way to make a background. Do not set manually the attributes, always use the methods.
    """

    def __init__(self, image: pygame.Surface, window_sizes: Tuple[int, int], window_surface: pygame.Surface):
        self.original = image
        self.image = scale_image(self.original, None, window_sizes)
        self.window_sizes = window_sizes
        self.window = window_surface

    def get_image(self) -> pygame.Surface:
        return self.image

    def change_image(self, image: pygame.Surface) -> pygame.Surface:
        """
        Change the image and resize it.
        """
        self.original = image
        self.image = scale_image(self.original, None, self.window_sizes)
        return self.image

    def resize(self, window_sizes: Tuple[int, int]):
        """
        Resize the image.
        """
        self.window_sizes = window_sizes
        self.image = scale_image(self.original, None, self.window_sizes)

    def set_window(self, window_surface: pygame.Surface):
        """
        Change the window surface.
        """
        self.window = window_surface

    def draw(self):
        """
        Draw the background.
        """
        self.window.blit(self.image, (0, 0))
