import pygame, sys
from typing import Tuple,Union
# pygame shortcuts
from pygame.key import get_pressed as get_keys_pressed
from pygame.mouse import get_pressed as get_buttons_pressed
from pygame.mouse import get_pos as get_mouse_pos
from pygame.mouse import get_focused as get_mouse_focused
from pygame.mouse import get_visible as get_mouse_visible
from pygame.mouse import set_visible as set_mouse_visible
from pygame.mouse import set_pos as set_mouse_pos
from pygame.mouse import set_cursor
from pygame.event import get as get_events
from pygame.time import get_ticks

# CONSTANTS
LEFT_BUTTON = 1
RIGHT_BUTTON = 3
MIDDLE_BUTTON = 2
WHEEL_UP = 4
WHEEL_DOWN = 5

RIGHT_CLICK = 2
MIDDLE_CLICK = 1
LEFT_CLICK = 0

LEFT = -1
RIGHT = 1
UP = -1
DOWN = 1

HORIZONTAL = "h"
VERTICAL = "v"

# EVENT
def quit_event(event:pygame.event.Event,custom_function=None)->None:
    """Check for exit event and quit the game/run a custom function."""
    if event.type == pygame.QUIT:
        if custom_function:
            custom_function()
        else:
            pygame.quit()
            sys.exit()
            

def check_event(event:pygame.event.Event,type)->bool:
    """Check if an event is of the type specified."""
    return event.type == type

def key_event(event:pygame.event.Event,key,direction:str="down")->bool:
    """Check if an event is of the key specified."""
    if direction == "down":
        if event.type == pygame.KEYDOWN:
            return event.key == key
    elif direction == "up":
        if event.type == pygame.KEYUP:
            return event.key == key
    return False

def button_event(event:pygame.event.Event,button:int,direction:str="down")->bool:
    """
    Check if an event is of the button specified.

    Do not use the {type}_CLICK variables here, instead the {type}_BUTTON.
    """
    if direction == "down":
        if event.type == pygame.MOUSEBUTTONDOWN:
            return event.button == button
    elif direction == "up":
        if event.type == pygame.MOUSEBUTTONUP:
            return event.button == button
    return False


def key_is_pressed(key,keys_pressed:list=None)->bool:
    """Check if a key is being pressed."""
    keys = pygame.key.get_pressed() if not keys_pressed else keys_pressed

    return keys[key]

def button_is_pressed(button:int,buttons_pressed:tuple=None)->bool:
    """
    Check if a button (mouse) if being pressed.

    Do not use the {type}_BUTTON variables here, instead the {type}_CLICK.
    """
    mouse = pygame.mouse.get_pressed() if not buttons_pressed else buttons_pressed

    return mouse[button]

# DELTA TIME
def get_dt(desired_fps:int,clock:pygame.time.Clock)->float:
    """
    Return a value similar to one if the framerate is as desired, otherwise the value will be bigger or smaller if the framerate is lower or bigger than the desired.
    """
    fps = clock.get_fps()
    if fps <= 0:
        fps = desired_fps
    return desired_fps/fps