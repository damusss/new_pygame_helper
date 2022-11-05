from random import choice, uniform
from ...graphics.surface import *
import pygame
from typing import List, Tuple, Union
#import sys
#sys.path.append("..")

"""
Contains the particle classes.
"""


class CircleParticles():
    """
    A particles generator fully customizable that uses only circles.
    """

    def __init__(self,
                 origin: Union[Tuple[int, int], List[int], pygame.math.Vector2],
                 anchor_sprite=None,
                 anchor_offset: Union[Tuple[int, int],
                                      List[int], pygame.math.Vector2] = (0, 0),
                 active: bool = True,
                 colors: List[Union[str, Tuple[int, int, int]]] = ["white"],
                 use_gravity: bool = True,
                 gravity_speed: float = 0.1,
                 cooldown: int = 1000,
                 speed_random_range: Tuple[Tuple[float, float], Tuple[float, float]] = (
                     (-1.0, 1.0), (-1.0, 1.0)),
                 change_over_time: bool = True,
                 change_multiplier: int = -1,
                 start_radius: int = 3,
                 destroy_or_hide_cooldown: int = 9999,
                 destroy_after_time: bool = False,
                 hide_after_time: bool = False):

        self.origin_point:pygame.math.Vector2 = pygame.math.Vector2(origin)
        """From where particles originates. <get, set>"""
        self.anchor_sprite = anchor_sprite
        """The sprite the particles are attached to. <get, set>"""
        self.anchor_offset:pygame.Vector2 = pygame.math.Vector2(anchor_offset)
        """The offset from the sprite. <get, set>"""

        self.particles:list[dict] = []
        """The particles list. <get>"""

        self.use_gravity:bool = use_gravity
        """If particles use gravity. <get, set>"""
        self.gravity_speed:float = gravity_speed
        """The speed of the gravity. <get, set>"""
        self._cooldown = cooldown
        
        self.speed_random_range:tuple[tuple[float,float],tuple[float,float]] = speed_random_range
        """The speed range. <get, set>"""
        self.change_over_time:bool = change_over_time
        """If the particles change size over time. <get, set>"""
        self.change_multiplier:int = change_multiplier
        """If the particles grows or shrink. <get, set>"""
        self._start_scale = start_radius
        self.destroy_or_hide_cooldown:int = destroy_or_hide_cooldown
        """Cooldown for destroying or hiding the particles. <get, set>"""
        self.destroy_after_time:bool = destroy_after_time
        """If the particles should destroy after the cooldown. <get, set>"""
        self.hide_after_time:bool = hide_after_time
        """If the particles should hide after the cooldown. <get, set>"""
        self.active:bool = active
        """If the particles can generate. <get, set>"""
        self.colors:list = colors
        """The colors list. <get, set>"""

        self.scaleMinuser = self._start_scale/self._cooldown
        """internal"""

        self.lastTime:int = pygame.time.get_ticks()
        """Last pygame tick. <get>"""
        self.lastHide:int = pygame.time.get_ticks()
        """Last time hidden. <get>"""

    def copy(self):
        """Returns a copy of the particles."""
        return CircleParticles(self.origin_point.xy, self.anchor_sprite, self.anchor_offset, self.active, self.colors, self.use_gravity, self.gravity_speed, self.cooldown, self.speed_random_range, self.change_over_time, self.change_multiplier, self.start_radius, self.destroy_or_hide_cooldown, self.destroy_after_time, self.hide_after_time)

    @property
    def cooldown(self) -> int:
        """How much particles last."""
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value: int):
        self._cooldown = value
        self.scaleMinuser = self._start_scale/self._cooldown

    @property
    def start_radius(self) -> int:
        """The start radius of particles."""
        return self._start_scale

    @start_radius.setter
    def start_radius(self, value: int):
        self._start_scale = value
        self.scaleMinuser = self._start_scale/self._cooldown

    def empty_particles(self) -> None:
        """
        Clears the particle list.
        """
        self.particles.clear()

    def update_position(self) -> None:
        """
        Changes the origin point to the anchor sprite center offsetted.
        """
        if self.anchor_sprite:
            self.origin_point.xy = self.anchor_offset + self.anchor_sprite.rect.center

    def generate(self) -> None:
        """
        Adds one particle to the list.
        """
        if self.active:
            self.particles.append({"color": choice(self.colors), "pos": list(self.origin_point.xy), "speed": [uniform(self.speed_random_range[0][0], self.speed_random_range[0][1]), uniform(
                self.speed_random_range[1][0], self.speed_random_range[1][1])], "time": self._cooldown, "scale": self._start_scale})

    def draw(self, surface: pygame.Surface) -> None:
        """
        Blit the particles and update them.
        """
        current = pygame.time.get_ticks()

        toRemove = []

        for particle in self.particles:
            particle["pos"][0] += particle["speed"][0]
            particle["pos"][1] += particle["speed"][1]

            dt = current-self.lastTime

            particle["time"] -= dt

            if self.use_gravity:
                particle["speed"][1] += self.gravity_speed

            if particle["time"] <= 0:
                toRemove.append(particle)

            if self.change_over_time:
                preview = particle["scale"] + \
                    ((dt*self.scaleMinuser) * self.change_multiplier)
                if round(preview) > 0:
                    particle["scale"] = preview

            pygame.draw.circle(surface, particle["color"], (int(
                particle["pos"][0]), int(particle["pos"][1])), round(particle["scale"]))

        for particle in toRemove:
            self.particles.remove(particle)

        if self.destroy_after_time or self.hide_after_time:
            if current-self.lastHide >= self.destroy_or_hide_cooldown:
                if self.destroy_after_time:
                    self.kill()
                elif self.hide_after_time:
                    self.active = False
                    self.empty_particles()
                self.lastHide = current

        self.lastTime = current

    def kill(self) -> None:
        """
        Delete itself.
        """
        del self


class Particles():
    """
    A particles generator fully customizable.
    """

    def __init__(self,
                 origin: Union[Tuple[int, int], List[int], pygame.math.Vector2],
                 anchor_sprite=None,
                 anchor_offset: Union[Tuple[int, int],
                                      List[int], pygame.math.Vector2] = (0, 0),
                 images: List[pygame.Surface] = [],
                 active: bool = True,
                 use_gravity: bool = True,
                 gravity_speed: float = 0.1,
                 cooldown: int = 1000,
                 speed_random_range: Tuple[Tuple[float, float], Tuple[float, float]] = (
                     (-1.0, 1.0), (-1.0, 1.0)),
                 change_over_time: bool = True,
                 change_multiplier: int = -1,
                 start_scale: float = 1.0,
                 destroy_or_hide_cooldown: int = 9999,
                 destroy_after_time: bool = False,
                 hide_after_time: bool = False):

        self.origin_point = pygame.math.Vector2(origin)
        self.anchor_sprite = anchor_sprite
        self.anchor_offset = pygame.math.Vector2(anchor_offset)

        self.particles = []

        self.use_gravity = use_gravity
        self.gravity_speed = gravity_speed
        self._cooldown = cooldown
        self.speed_random_range = speed_random_range
        self.change_over_time = change_over_time
        self.change_multiplier = change_multiplier
        self._start_scale = start_scale
        self.destroy_or_hide_cooldown = destroy_or_hide_cooldown
        self.destroy_after_time = destroy_after_time
        self.hide_after_time = hide_after_time
        self.active = active

        self.original_images = images if len(images) > 0 else [
            empty_image((5, 5), "white")]

        self.scaleMinuser = self._start_scale/self._cooldown

        self.lastTime = pygame.time.get_ticks()
        self.lastHide = pygame.time.get_ticks()

        for image in self.original_images:
            image = scale_image(image, self._start_scale)

    def copy(self):
        return CircleParticles(self.origin_point.xy, self.anchor_sprite, self.anchor_offset, self.original_images, self.active, self.use_gravity, self.gravity_speed, self.cooldown, self.speed_random_range, self.change_over_time, self.change_multiplier, self.start_scale, self.destroy_or_hide_cooldown, self.destroy_after_time, self.hide_after_time)

    @property
    def cooldown(self) -> int:
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value: int):
        self._cooldown = value
        self.scaleMinuser = self._start_scale/self._cooldown

    @property
    def start_scale(self) -> float:
        return self._start_scale

    @start_scale.setter
    def start_scale(self, value: float):
        self._start_scale = value
        self.scaleMinuser = self._start_scale/self._cooldown
        for image in self.original_images:
            image = scale_image(image, self._start_scale)

    def empty_particles(self) -> None:
        """
        Empty the particle list.
        """
        self.particles.clear()

    def update_position(self) -> None:
        """
        Change the origin point to the anchor sprite rect center offsetted.
        """
        if self.anchor_sprite:
            self.origin_point.xy = self.anchor_offset + self.anchor_sprite.rect.center

    def generate(self) -> None:
        """
        Add one particle to the list.
        """
        if self.active:
            image = choice(self.original_images)
            self.particles.append({"pos": list(self.origin_point.xy), "speed": [uniform(self.speed_random_range[0][0], self.speed_random_range[0][1]), uniform(
                self.speed_random_range[1][0], self.speed_random_range[1][1])], "time": self._cooldown, "scale": self._start_scale, "image": image, "original": image})

    def draw(self, surface: pygame.Surface) -> None:
        """
        Blit the particles and update them.
        """
        current = pygame.time.get_ticks()

        toRemove = []

        for particle in self.particles:
            particle["pos"][0] += particle["speed"][0]
            particle["pos"][1] += particle["speed"][1]

            dt = current-self.lastTime

            particle["time"] -= dt

            if self.use_gravity:
                particle["speed"][1] += self.gravity_speed

            if particle["time"] <= 0:
                toRemove.append(particle)

            if self.change_over_time:
                preview = particle["scale"] + \
                    ((dt*self.scaleMinuser) * self.change_multiplier)
                if preview > 0:
                    particle["scale"] = preview
                particle["image"] = scale_image(
                    particle["original"], particle["scale"])

            surface.blit(particle["image"], particle["pos"])

        for particle in toRemove:
            self.particles.remove(particle)

        if self.destroy_after_time or self.hide_after_time:
            if current-self.lastHide >= self.destroy_or_hide_cooldown:
                if self.destroy_after_time:
                    self.kill()
                elif self.hide_after_time:
                    self.active = False
                    self.empty_particles()
                self.lastHide = current

        self.lastTime = current

    def kill(self) -> None:
        """
        Delete itself.
        """
        del self
