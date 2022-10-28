import pygame
from typing import Tuple,Union
from os import walk

from pygame.transform import flip,rotate,rotozoom
from pygame import Surface
from pygame.draw import rect as draw_rect
from pygame.draw import circle as draw_circle
from pygame.draw import line as draw_line
from pygame.draw import lines as draw_lines
from pygame.draw import polygon as draw_polygon

"""
Contains seful methods related to pygame surfaces.
"""

def resize_rect(original_rect:pygame.Rect,surface:pygame.Surface)->pygame.Rect:
	"""Return a rect of the same sizes of the image passed but at the same position of the original."""
	return surface.get_rect(center=original_rect.center)

def empty_image(sizes:Tuple[int,int]=(1,1),color:Union[str,Tuple[int,int,int]]=None)->pygame.Surface:
	"""Return a basic surface."""
	image = pygame.Surface(sizes)
	if color:
		image.fill(color)

	return image

# TRANSFORM
def load_image(path:str,convert_alpha:bool=False)->pygame.Surface:
	"""Load an image and return a surface."""
	return pygame.image.load(path).convert() if not convert_alpha else pygame.image.load(path).convert_alpha()

def scale_image(image:pygame.Surface,scale:float=None,sizes:Tuple[int,int]=None,smooth:bool=False)->pygame.Surface:
	"""Scale an image by scale or sizes."""
	if scale:
		if not smooth:
			return pygame.transform.scale(image,(int(image.get_width()*scale),int(image.get_height()*scale)))
		else:
			return pygame.transform.smoothscale(image,(int(image.get_width()*scale),int(image.get_height()*scale)))
	elif sizes:
		if not smooth:
			return pygame.transform.scale(image,(sizes[0],sizes[1]))
		else:
			return pygame.transform.smoothscale(image,(sizes[0],sizes[1]))

# IMPORT
def import_images_folder(folder_path:str,convert_alpha:bool=False,scale:float=None,scale_sizes:Tuple[int,int]=None)->list:
    """Return a list of images from a folder (useful for animations)."""
    surface_list = []

    for _,__,image_files in walk(folder_path):
        for image in image_files:
            full_path = folder_path + '/' + image
            image_surf = load_image(full_path,convert_alpha)
            if scale or scale_sizes:
                image_surf = scale_image(image_surf,scale,scale_sizes[0],scale_sizes[1])
            surface_list.append(image_surf)

    return surface_list

def import_images_folder_dict(folder_path:str,convert_alpha:bool=False,scale:float=None,scale_sizes:Tuple[int,int]=None)->dict:
    """Return a dict of images from a folder (useful for animations)."""
    surface_list = []

    for _,__,image_files in walk(folder_path):
        for image in image_files:
            full_path = folder_path + '/' + image
            image_surf = load_image(full_path,convert_alpha)
            if scale or scale_sizes:
                image_surf = scale_image(image_surf,scale,scale_sizes[0],scale_sizes[1])
            surface_list[image.split(".")[0]] = image_surf

    return surface_list