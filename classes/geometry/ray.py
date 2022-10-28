import sys
sys.path.append("..")
from .lines import Segment
from ..sprites import sprite as sprites
import pygame
from typing import Tuple, List, Union

"""
Contains the Ray class and raycast function.
"""

# RAYCAST


class Ray():
    """
    Another way of checking collisions between a ray and a list of sprites.

    That is the class version, meaning the ray is created once and only its attributes are changed.

    A bit more efficient, but only useful if the check is run every frame.

    Do not change the attributes that starts with a _, only use the functions! Or it will break.

    The thicness will not effect the ray collision range, just a visual effect.
    """

    def __init__(self, origin: Tuple[int, int], direction: Tuple[float, float], lenght: int, color: Union[str, Tuple[int, int, int]] = "white", thicness: int = 2):
        self.ray = Segment(
            origin, (origin[0]+direction[0]*lenght, origin[1]+direction[1]*lenght), color, thicness)
        self._lenght = lenght
        self._direction = direction

    def cast(self, sprites: List[sprites.Sprite], draw: bool = False, surface: pygame.Surface = None) -> List[sprites.Sprite]:
        """
        Return a list with the sprites that collides with the ray.
        """
        colliding = []
        for sprite in sprites:
            if self.ray.colliderect(sprite.rect):
                colliding.append(sprite)
        if draw:
            self.ray.draw(surface)
        return colliding

    def draw(self, surface: pygame.Surface):
        """
        Draw the ray without checking collisions.
        """
        self.ray.draw(surface)

    def set_origin(self, origin: Tuple[int, int]):
        """
        Set the origin of the ray, and shift the end.
        """
        self.ray.start.xy = origin
        self.ray.end.xy = (self.ray.start[0]+self._direction[0]*self._lenght,
                           self.ray.start[1]+self._direction[1]*self._lenght)

    def set_direction(self, direction: Tuple[float, float]):
        """
        Set the direction of the ray and shift its end.
        """
        self._direction = direction
        self.ray.end.xy = (
            self.ray.start[0]+direction[0]*self._lenght, self.ray.start[1]+direction[1]*self._lenght)

    def set_lenght(self, lenght: int):
        """
        Set the lenght of the ray and shift the end.
        """
        self._lenght = lenght
        self.ray.end.xy = (self.ray.start[0]+self._direction[0]
                           * lenght, self.ray.start[1]+self._direction[1]*lenght)

    def set_color(self, color):
        """
        Set the color of the ray.
        """
        self.ray.color = color

    def set_thicness(self, thicness):
        """
        Set the thicness of the ray.

        This will not effect the ray collision range, just a visual effect.
        """
        self.ray.thicness = thicness

    def follow_sprite(self, sprite: sprites.Sprite, follow_direction: bool = True):
        """
        Set the origin to the sprite position and (optional) the direction to the sprite one.
        """
        self.set_origin(sprite.position)
        if follow_direction:
            self.set_direction(sprite.direction)


def raycast(origin: Tuple[int, int], direction: Tuple[float, float], lenght: int, sprites: list, draw: bool = False, surface: pygame.Surface = None, color: Union[str, Tuple[int, int, int]] = "white", thicness: int = 2) -> list:
    """
    Return a list with the sprites that collides with a ray.

    The thicness will not effect the ray collision range, just a visual effect.
    """
    ray = Segment(origin, (origin[0]+direction[0]*lenght,
                  origin[1]+direction[1]*lenght), color, thicness)
    colliding = []
    for sprite in sprites:
        if ray.colliderect(sprite.rect):
            colliding.append(sprite)
    if draw:
        ray.draw(surface)
    return colliding
