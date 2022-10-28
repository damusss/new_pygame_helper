import pygame
from typing import Tuple,Union

from pygame.display import get_window_size,get_surface,set_caption,set_icon,set_mode

"""
Contains useful functions managing the pygame window.
"""

# WINDOW
def update_window(clock:pygame.time.Clock,desired_fps:int,window_surface:pygame.Surface=None,fill_color:Union[str,Tuple[int,int,int]]="black")->None:
	"""Update the window and fill it after using the clock and pygame."""
	clock.tick(desired_fps)
	pygame.display.flip()
	if window_surface:
		window_surface.fill(fill_color)

def resize_window(current_surface,resized_window_sizes,resizable=True,flag=0):
	"""
	Resize the window surface and blit the old one on it. Useful after the VIDEORESIZE event.
	"""
	if resizable:
		flag = pygame.RESIZABLE
	new = pygame.display.set_mode(resized_window_sizes,flag)
	new.blit(current_surface, (0,0))
	return new

def set_fullscreen()->pygame.Surface:
	"""
	Set the window to fullscreen mode.
	"""
	sizes = pygame.display.get_window_size()
	return pygame.display.set_mode(sizes,pygame.FULLSCREEN)

def set_windowed()->pygame.Surface:
	"""
	Exit the fullscreen mode.
	"""
	sizes = pygame.display.get_window_size()
	return pygame.display.set_mode(sizes)

def set_resizable()->pygame.Surface:
	"""
	Set the window to a resizable one.
	"""
	sizes = pygame.display.get_window_size()
	return pygame.display.set_mode(sizes,pygame.RESIZABLE)

def set_noframe()->pygame.Surface:
	"""
	Set the window to no frame mode.
	"""
	sizes = pygame.display.get_window_size()
	return pygame.display.set_mode(sizes,pygame.NOFRAME)