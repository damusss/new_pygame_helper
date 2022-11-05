import pygame
from typing import Union, Tuple, List
#import sys

"""
Contains the Trail class.
"""


class Trail():
    """
    A customizable trail generator to attach to a sprite.
    """

    def __init__(self, sprite, offset: Union[Tuple[int, int], List[int], pygame.math.Vector2] = (0, 0), color: Union[str, Tuple[int, int, int]] = "white", trail_thicness: int = 5, disappear_speed: float = 0.1, active: bool = True):
        self.sprite = sprite
        """The sprite attached to. <get, set>"""

        self.offset:pygame.Vector2 = pygame.math.Vector2(offset)
        """The offset from the sprite. <get, set>"""
        self.origin_point:pygame.Vector2 = self.offset+self.sprite.rect.center
        """The origin point. Will follow the sprite+offset. <get>"""
        self.color:str|tuple[int,int,int]|pygame.Color = color
        """The color of the trail. <get, set>"""
        self.trail_thicness:int = trail_thicness
        """The thicness of the trail. <get, set>"""
        self.disappear_speed:float = disappear_speed
        """How slowly the trail disappear. <get, set>"""
        self.previus:pygame.Vector2 = pygame.math.Vector2(self.origin_point)
        """Previous origin point. <get>"""
        self.active:bool = active
        """Whether the trail grows or not. <get, set>"""

        self.lines:list[dict] = []
        """The lines list. <get>"""

    def copy(self):
        """Returns a copy of the trail."""
        new = Trail(self.sprite, self.offset, self.color,
                    self.trail_thicness, self.disappear_speed, self.active)
        new.lines = self.lines
        return new

    def kill(self) -> None:
        """
        Deletes itself.
        """
        del self

    def clear_trail(self) -> None:
        """
        Clears the trail list.
        """
        self.lines.clear()

    def update_position(self) -> None:
        """
        Changes th origin point to the sprite rect center offsetted.
        """
        self.origin_point = self.offset+self.sprite.rect.center

    def generate(self) -> None:
        """
        Adds one trail line to the list.
        """
        if self.active:
            if self.previus != self.origin_point:
                self.lines.append({"color": self.color, "size": self.trail_thicness,
                                  "pos1": self.origin_point.xy, "pos2": self.previus.xy})

            self.previus = self.origin_point

    def draw(self, surface: pygame.Surface, dt: float = 1.0) -> None:
        """
        Draws the trail lines.
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
