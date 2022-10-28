import sys
sys.path.append("...")
from _utils import det, tuple_slope, in_range
from typing import Tuple, Union
import pygame
import math


"""
Contains the Segment and Line class.
"""


class Segment():
    """
    A useful class to more easly work with segments in pygame or in general.
    """

    def __init__(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], color: Union[str, Tuple[int, int, int]] = "white", thicness: int = 2):
        self.start = pygame.math.Vector2(start_pos)
        self.end = pygame.math.Vector2(end_pos)
        self.color = color
        self.thicness = thicness

    def to_tuple(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return (self.start.xy, self.end.xy)

    def colliderect(self, rect: pygame.Rect) -> bool:
        return any([self.tuple_intersects((rect.topleft, rect.bottomleft)), self.tuple_intersects((rect.topleft, rect.topright)), self.tuple_intersects((rect.bottomleft, rect.bottomright)), self.tuple_intersects((rect.topright, rect.bottomright))])

    def set_start(self, pos: Tuple[int, int]):
        """
        Set the start xy attribute.
        """
        self.start.xy = (pos[0], pos[1])

    def set_end(self, pos: Tuple[int, int]):
        """
        Set the end xy attribute.
        """
        self.end.xy = (pos[0], pos[1])

    def int(self):
        """
        Correct any non-int value on the points.
        """
        self.start.x = int(self.start.x)
        self.start.y = int(self.start.y)
        self.end.x = int(self.end.x)
        self.end.y = int(self.end.y)

    def int_point(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """
        Correct any non-int values in a point and return it.
        """
        return (int(point[0]), int(point[1]))

    def move(self, x: int, y: int):
        """
        Move the segment by an amount.
        """
        self.start.x += x
        self.start.y += y
        self.end.x += x
        self.end.y += y

    def extend(self, amount, extend_start=False):
        current_x = self.end.x-self.start.x
        current_y = self.end.y-self.start.y
        if current_x == 0:
            if extend_start:
                self.start.y += amount
            else:
                self.end.y += amount
            return 0, amount
        if current_y == 0:
            if extend_start:
                self.start.x += amount
            else:
                self.end.x += amount
            return amount, 0
        hypotenus = math.sqrt((current_x**2+current_y**2))
        hypotenus += amount
        new_x = math.sqrt((hypotenus**2-current_y**2))
        new_y = math.sqrt((hypotenus**2-current_x**2))
        offset_x = new_x-current_x
        offset_y = new_y-current_y
        if extend_start:
            self.start.y += offset_y
            self.start.x += offset_x
        else:
            self.end.y += offset_y
            self.end.x += offset_x
        return offset_x, offset_y

    def copy(self):
        """
        Return an exact copy of the segment.
        """
        return Segment(self.start, self.end, self.color, self.thicness)

    def to_line(self):
        """
        Return a line with the same properties of this segment.
        """
        return Line(self.start, self.end, self.color, self.thicness)

    def lenght(self) -> float:
        """
        Return the lenght of the segment.
        """
        return math.dist(self.start, self.end)

    def slope(self) -> float:
        """
        Return the slope of the segment.
        """
        if (self.end.x-self.start.x) == 0:
            return None
        return (self.end.y-self.start.y)/(self.end.x-self.start.x)

    def is_parallel(self, segment) -> bool:
        """
        Check if two segments are parallel.
        """
        return self.slope() == segment.slope()

    def tuple_is_parallel(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
        """
        Check if this segment and a tuple based segment are parallel.
        """
        return self.slope() == tuple_slope(tuplee)

    def tuple_intersection_point(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> Tuple[float, float]:
        """
        If the segment and the tuple based segment intersects, return the point, otherwise return (None,None)
        """
        if not self.tuple_is_parallel(tuplee):
            if self.tuple_intersects(tuplee):
                return self.tuple_absolute_intersection_point(tuplee)
        return (None, None)

    def tuple_absolute_intersection_point(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> Tuple[float, float]:
        """
        Calculate the intersection point of a segment and a tuple based segment (non parallel) even if the point is not inside them.
        """
        if self.tuple_is_parallel(tuplee):
            raise ValueError("Parallel segments cannot intersect.")

        xdiff = (self.start.x-self.end.x, tuplee[0][0]-tuplee[1][0])
        ydiff = (self.start.y-self.end.y, tuplee[0][1]-tuplee[1][1])

        div = det(xdiff, ydiff)

        d = (det(self.start, self.end), det(tuplee[0], tuplee[1]))
        return (det(d, xdiff)/div, det(d, ydiff)/div)

    def tuple_intersects(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
        """
        Check if the segment and a tuple based segment intersects.
        """
        if not self.tuple_is_parallel(tuplee):
            point = self.tuple_absolute_intersection_point(tuplee)
            return in_range(self.start.x, self.end.x, point[0]) and in_range(tuplee[0][0], tuplee[1][0], point[0]) and in_range(self.start.y, self.end.y, point[1]) and in_range(tuplee[0][1], tuplee[1][1], point[1])
        return False

    def absolute_intersection_point(self, segment) -> Tuple[float, float]:
        """
        Calculate the intersection point of two segments (non parallel) even if the point is not inside them.
        """
        if self.is_parallel(segment):
            raise ValueError("Parallel segments cannot intersect.")

        xdiff = (self.start.x-self.end.x, segment.start.x-segment.end.x)
        ydiff = (self.start.y-self.end.y, segment.start.y-segment.end.y)

        div = det(xdiff, ydiff)
        if div == 0:
            div = 0.0000001

        d = (det(self.start, self.end), det(segment.start, segment.end))
        return (det(d, xdiff)/div, det(d, ydiff)/div)

    def intersection_point(self, segment) -> Tuple[float, float]:
        """
        If the segments intersects, return the point, otherwise return (None,None)
        """
        if not self.is_parallel(segment):
            if self.intersects(segment):
                return self.absolute_intersection_point(segment)
        return (None, None)

    def intersects(self, segment) -> bool:
        """
        Check if the segments intersects.
        """
        if not self.is_parallel(segment):
            point = self.absolute_intersection_point(segment)
            return in_range(self.start.x, self.end.x, point[0]) and in_range(segment.start.x, segment.end.x, point[0]) and in_range(self.start.y, self.end.y, point[1]) and in_range(segment.start.y, segment.end.y, point[1])
        return False

    def draw(self, surface: pygame.Surface):
        """
        Draw the segment.
        """
        pygame.draw.line(surface, self.color, self.start.xy,
                         self.end.xy, width=self.thicness)


class Line():
    """
    Similar to the segment, but with slightly different math, as two non parallel lines always have an intersection.
    """

    def __init__(self, point1: Tuple[int, int], point2: Tuple[int, int], color: Union[str, Tuple[int, int]] = "white", thicness: int = 2):
        self.point1 = pygame.math.Vector2(point1)
        self.point2 = pygame.math.Vector2(point2)
        self.color = color
        self.thicness = thicness

    def to_tuple(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return (self.point1.xy, self.point2.xy)

    def colliderect(self, rect: pygame.Rect) -> bool:
        return any([self.tuple_intersects((rect.topleft, rect.bottomleft)), self.tuple_intersects((rect.topleft, rect.topright)), self.tuple_intersects((rect.bottomleft, rect.bottomright)), self.tuple_intersects((rect.topright, rect.bottomright))])

    def set_point1(self, pos: Tuple[int, int]):
        """
        Set the point1 xy attribute.
        """
        self.point1.xy = (pos[0], pos[1])

    def set_point2(self, pos: Tuple[int, int]):
        """
        Set the point2 xy attribute.
        """
        self.point2.xy = (pos[0], pos[1])

    def int(self):
        """
        Correct any non-int value on the points.
        """
        self.point1.x = int(self.point1.x)
        self.point1.y = int(self.point1.y)
        self.point2.x = int(self.point2.x)
        self.point2.y = int(self.point2.y)

    def int_point(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """
        Correct any non-int values in a point and return it.
        """
        return (int(point[0]), int(point[1]))

    def move(self, x: int, y: int):
        """
        Move the line by an amount.
        """
        self.point1.x += x
        self.point1.y += y
        self.point2.x += x
        self.point2.y += y

    def lenght(self) -> float:
        """
        Return the lenght between the two known points.
        """
        return math.dist(self.point1, self.point2)

    def slope(self) -> float:
        """
        Return the slope of the line.
        """
        if (self.point2.x-self.point1.x) == 0:
            return None
        return (self.point2.y-self.point1.y)/(self.point2.x-self.point1.x)

    def is_parallel(self, line) -> bool:
        """
        Check if two lines are parallel.
        """
        return self.slope() == line.slope()

    def tuple_is_parallel(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
        """
        Check if this line and a tuple based line are parallel.
        """
        return self.slope() == tuple_slope(tuplee)

    def tuple_intersection_point(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> Tuple[float, float]:
        """
        If the line and the tuple based line intersects, return the point, otherwise return (None,None)
        """
        if not self.tuple_is_parallel(tuplee):
            return self.tuple_absolute_intersection_point(tuplee)
        return (None, None)

    def tuple_absolute_intersection_point(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> Tuple[float, float]:
        """
        Calculate the intersection point of a line and a tuple based line (non parallel) even if the point is not inside them.
        """
        if self.tuple_is_parallel(tuplee):
            raise ValueError("Parallel lines cannot intersect.")

        xdiff = (self.point1.x-self.point2.x, tuplee[0][0]-tuplee[1][0])
        ydiff = (self.point1.y-self.point2.y, tuplee[0][1]-tuplee[1][1])

        div = det(xdiff, ydiff)

        d = (det(self.point1, self.point2), det(tuplee[0], tuplee[1]))
        return (det(d, xdiff)/div, det(d, ydiff)/div)

    def tuple_intersects(self, tuplee: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
        """
        Check if the segment and a tuple based segment intersects.
        """
        if not self.tuple_is_parallel(tuplee):
            return True
        return False

    def copy(self):
        """
        Return an exact copy of the line.
        """
        return Line(self.point1, self.point2, self.color, self.thicness)

    def to_segment(self):
        """
        Convert the line to a segment.
        """
        return Segment(self.point1, self.point2, self.color, self.thicness)

    def absolute_intersection_point(self, line) -> Tuple[float, float]:
        """
        Calculate the intersection point of two lines (non parallel, otherwise throws an error).
        """
        if self.is_parallel(line):
            raise ValueError("Parallel lines cannot intersect.")

        xdiff = (self.point1.x-self.point2.x, line.point1.x-line.point2.x)
        ydiff = (self.point1.y-self.point2.y, line.point1.y-line.point2.y)

        div = det(xdiff, ydiff)

        d = (det(self.point1, self.point2), det(line.point1, line.point2))
        return (det(d, xdiff)/div, det(d, ydiff)/div)

    def intersection_point(self, line) -> Tuple[float, float]:
        """
        If the lines are not parallel, return the intersection point, otherwise return (None,None)
        """
        if not self.is_parallel(line):
            return self.absolute_intersection_point(line)
        return (None, None)

    def intersects(self, line) -> bool:
        """
        Check if the lines intersects (aka if they are not parallel).
        """
        if not self.is_parallel(line):
            return True
        return False

    def draw(self, surface: pygame.Surface):
        """
        Draw the line (it will look like a segment).
        """
        pygame.draw.line(surface, self.color, self.point1.xy,
                         self.point2.xy, width=self.thicness)
