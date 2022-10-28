import sys
sys.path.append("...")
from _utils import dist
import pygame
import math
from pygame.math import Vector2, Vector3
from typing import Tuple, Union, List


"""
Contains the Circle class.
"""


class Circle():
    """
    A useful class with circle informations and methods, similar to the pygame rect one.
    """

    def __init__(self, center: Tuple[int, int], radius: float, color: Union[str, Tuple[int, int, int]] = "white", line_width: int = 0):
        self.center = pygame.math.Vector2(center)
        self.radius = radius
        self.color = color
        self.line_width = line_width

    @staticmethod
    def from_rect(rect: pygame.Rect, color: Union[str, Tuple[int, int, int]] = "white", line_width: int = 0):
        """
        Return a circle made from a rect. This is a static method, working as a second constructor.
        """
        if rect.w != rect.h:
            raise ValueError(
                "Rect width and height must be the same to create a circle.")
        return Circle(rect.center, rect.w/2, color, line_width)

    def to_rect(self) -> pygame.Rect:
        """
        Return the bounding rect of the circle.
        """
        return pygame.Rect(self.center.x-self.radius, self.center.y-self.radius, self.radius*2, self.radius*2)

    def set_center(self, pos):
        """
        Set the center xy attribute.
        """
        self.center.xy = (pos[0], pos[1])

    def collidemouse(self) -> bool:
        """
        Check if the mouse is hovering the circle.
        """
        pos = pygame.mouse.get_pos()
        return self.collidepoint(pos[0], pos[1])

    def draw(self, surface: pygame.Surface, *direction_args):
        """
        Draw the circle.
        """
        pygame.draw.circle(surface, self.color, self.center.xy,
                           self.radius, self.line_width, *direction_args)

    def copy(self):
        """
        Return the exact copy of a circle.
        """
        return Circle(self.center, self.radius, self.color, self.line_width)

    def move(self, x: int, y: int):
        """
        Move the circle center.
        """
        self.center.x += x
        self.center.y += y

    def clamp(self, circle):
        """
        Move the circle on the center of another one.
        """
        self.center.xy = circle.xy

    def clip(self, circle):  # needs math optimisation
        """
        I have no idea, copied it from google.
        """
        length = dist(self.center, circle.center)
        length2 = abs(length - (self.radius + circle.radius))
        newrad = length2 / 2
        newdist = self.radius - newrad
        newvec = pygame.math.Vector2(circle.x - self.x, circle.y - self.y)
        newvec.scale_to_length(newdist)
        return Circle((self.x + newvec.x, self.y + newvec.y), newrad)

    def normalize(self):
        """
        Correct the radius if negative.
        """
        self.radius = abs(self.radius)

    def contains(self, circle) -> bool:
        """
        Check if a circle is inside this circle.
        """
        return dist(self.center, circle.center) + circle.radius <= self.radius

    def collidepoint(self, x: int, y: int) -> bool:
        """
        Check if a point is colliding this circle.
        """
        return dist(self.center, (x, y)) <= self.radius

    def collidecircle(self, circle) -> bool:
        """
        Check if two circles are colliding.
        """
        return dist(self.center, circle.center) < self.radius + circle.radius

    def collidelist(self, circles: list) -> tuple:
        """
        Idk how to explain but it's similar to the rect one.
        """
        for i in range(len(circles)):
            if dist(self.center, circles[i].center) < self.radius + circles[i].radius:
                return tuple((i, circles[i]))

    def collidelistall(self, circles: list) -> List[tuple]:
        """
        Idk how to explain but it's similar to the rect one.
        """
        for i in range(len(circles)):
            if dist(self.center, circles[i].center) < self.radius + circles[i].radius:
                yield tuple((i, circles[i]))

    def collidedict(self, circles, use_values: bool = False) -> tuple:
        """
        Idk how to explain but it's similar to the rect one.
        """
        if not use_values:
            for circle in circles:
                if dist(self.center, circle.center) < self.radius + circle.radius:
                    return tuple((circle, circles[circle]))
        else:
            for key in circles.keys():
                if dist(self.center, circles[key].center) < self.radius + circle[key].radius:
                    return tuple((key, circles[key]))

    def collidedictall(self, circles: dict, use_values: bool = False) -> List[tuple]:
        """
        Idk how to explain but it's similar to the rect one.
        """
        if not use_values:
            for circle in circles:
                if dist(self.center, circle.center) < self.radius + circle.radius:
                    yield tuple((circle, circles[circle]))
        else:
            for key in circles.keys():
                if dist(self.center, circles[key].center) < self.radius + circles[key].radius:
                    yield tuple((key, circles[key]))

    @property
    def x(self):
        return self.center.x

    @x.setter
    def x(self, value):
        self.center.x = value

    @property
    def y(self):
        return self.center.y

    @y.setter
    def y(self, value):
        self.center.y = value

    @property
    def diameter(self):
        return self.radius*2

    @diameter.setter
    def diameter(self, value):
        self.radius = value/2

    @property
    def circumference(self):
        return self.radius * (math.pi*2)

    @circumference.setter
    def circumference(self, value):
        self.radius = value / (math.pi*2)

    @property
    def area(self):
        return self.radius**2*math.pi

    @area.setter
    def area(self, value):
        self.radius = math.sqrt(value/math.pi)
