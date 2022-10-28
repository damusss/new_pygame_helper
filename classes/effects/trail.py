import pygame
from typing import Union, Tuple, List
import sys

"""
Contains the Trail class.
"""


class Trail():
    """
    A customizable trail generator to attach to a sprite.
    """

    def __init__(self, sprite, offset: Union[Tuple[int, int], List[int], pygame.math.Vector2] = (0, 0), color: Union[str, Tuple[int, int, int]] = "white", trail_thicness: int = 5, disappear_speed: float = 0.1, active: bool = True):
        self.sprite = sprite

        self.offset = pygame.math.Vector2(offset)
        self.origin_point = self.offset+self.sprite.rect.center
        self.color = color
        self.trail_thicness = trail_thicness
        self.disappear_speed = disappear_speed
        self.previus = pygame.math.Vector2(self.origin_point)
        self.active = active

        self.lines = []

    def copy(self):
        new = Trail(self.sprite, self.offset, self.color,
                    self.trail_thicness, self.disappear_speed, self.active)
        new.lines = self.lines
        return new

    def kill(self) -> None:
        """
        Delete itself.
        """
        del self

    def clear_trail(self) -> None:
        """
        Clear the trail list.
        """
        self.lines.clear()

    def update_position(self) -> None:
        """
        Change th origin point to the sprite rect center offsetted.
        """
        self.origin_point = self.offset+self.sprite.rect.center

    def generate(self) -> None:
        """
        Add one trail line to the list.
        """
        if self.active:
            if self.previus != self.origin_point:
                self.lines.append({"color": self.color, "size": self.trail_thicness,
                                  "pos1": self.origin_point.xy, "pos2": self.previus.xy})

            self.previus = self.origin_point

    def draw(self, surface: pygame.Surface, dt: float = 1.0) -> None:
        """
        Draw the trail lines.
        """

        toRemove = []

        for par in self.lines:
            par["size"] -= self.disappear_speed*dt
            if round(par["size"]) <= 0:
                toRemove.append(par)
                continue
            else:
                pygame.draw.line(
                    surface, par["color"], par["pos1"], par["pos2"], round(par["size"]))

        for p in toRemove:
            self.lines.remove(p)
