import pygame
from typing import Union

"""
Contains useful functions related to graphics.
"""

# PIXEL CALCULATOR
def width_calculator(your_window_width:int,desired_result:Union[int,float],current_width:int=None,rounded:bool=False)->Union[int,float]:
	"""
	Return a pixel number caluculated with a formula, that will have a different output based on the current window sizes.

	Very useful to make your objects different sizes, based on the screen resolution.

	if the current sizes are the same as the one passed, it will actually return the desired result.

	This function takes in considertion only the width. Otherwise there are the functions 'height_calculator' and 'medium_calculator'.
	"""
	divider = your_window_width/desired_result
	pixels = (current_width if current_width else pygame.display.get_window_size()[0])/divider
	if rounded:
		return round(pixels)
	else:
		return pixels

def height_calculator(your_window_height:int,desired_result:Union[int,float],current_height:int=None,rounded:bool=False)->Union[int,float]:
	"""
	Return a pixel number caluculated with a formula, that will have a different output based on the current window sizes.

	Very useful to make your objects different sizes, based on the screen resolution.

	if the current sizes are the same as the one passed, it will actually return the desired result.

	This function takes in considertion only the height. Otherwise there are the functions 'width_calculator' and 'medium_calculator'.
	"""
	divider = your_window_height/desired_result
	pixels = (current_height if current_height else pygame.display.get_window_size()[1])/divider
	if rounded:
		return round(pixels)
	else:
		return pixels

def medium_calculator(your_window_width:int,your_window_height:int,desired_result:Union[int,float],current_width:int=None,current_height:int=None,rounded:bool=False)->Union[int,float]:
	"""
	Return a pixel number caluculated with a formula, that will have a different output based on the current window sizes.

	Very useful to make your objects different sizes, based on the screen resolution.

	if the current sizes are the same as the one passed, it will actually return the desired result.

	This function makes the medium of the width and height. Otherwise there are the functions 'height_calculator' and 'width_calculator'.
	"""
	first = width_calculator(your_window_width,desired_result,current_width,rounded)
	second = height_calculator(your_window_height,desired_result,current_height,rounded)
	pixels = (first+second)/2
	if rounded:
		return round(pixels)
	else:
		return pixels