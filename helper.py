#  imports
import pygame
import sys
from pygame.constants import *
from pygame.locals import *
from typing import Tuple
# modules imports
from .events.events import *
from .events.input import _GlobalInput
from .graphics.color import *
from .graphics.surface import *
from .graphics.utils import *
from .graphics.window import *
from .classes.background import *
from .classes.video import *
from .classes.timers import *
from .classes.pathfinding import *
from .classes.grids import *
from .classes.zoom import *
from .classes.geometry.ray import *
from .classes.geometry.circle import *
from .classes.geometry.lines import *
from .classes.effects.trail import *
from .classes.effects.particles import *
from .classes.sprites.sprite import *
from .classes.sprites.animated import *
from .classes.sprites.groups import *
from .classes.sprites.components import *
from .classes.ui.text import *
from .classes.ui.buttons import *
from .classes.ui.image import *
from .classes.ui.inputbox import *
from .classes.ui.statusbar import *
from .classes.ui.group import *
from .classes.ui.window import *
from .classes.ui.checkbox import *
from .classes.ui.slider import *
from .classes.ui.dropdown import *
from .classes.ui.window_stack import *
from .classes.animations.transform_animation import *
from .classes.animations.animation_step import *
from .classes.animations.animation_action import *
from .debug import _Debug

"""
This is the main modules with 3 main functions. The content of the other modules are all imported aswell.
"""

# globals
global_input:_GlobalInput = None
debug:_Debug=None

# INIT


def init(window_sizes: Tuple[int, int], window_caption: str = "Pygame Helper Window", window_flag: int = 0, window_icon_path: str = None, debug_activated: bool = False, debug_font_size: int = 30) -> Tuple[pygame.Surface, pygame.time.Clock]:
    """
    Init pygame, setup it and return the main screen and the clock in a tuple.
    """
    global global_input, debug
    # init
    pygame.init()
	
    # get main objects
    screen = pygame.display.set_mode(window_sizes, window_flag)
    clock = pygame.time.Clock()
    # set caption and icon
    pygame.display.set_caption(window_caption)
    if window_icon_path:
        icon_surface = load_image(window_icon_path, True)
        pygame.display.set_icon(icon_surface)
    # message
    print("Thanks for using pygame helper.")
    # set debug mode
    if debug_activated:
        print("Debug mode is activated - disable before publishing!")
    # return objects

    global_input = _GlobalInput()
    debug = _Debug(debug_activated,debug_font_size,screen)
    return screen, clock

# QUIT


def quit() -> None:
    """
    Quit pygame and exit.
    """
    pygame.quit()
    sys.exit()
