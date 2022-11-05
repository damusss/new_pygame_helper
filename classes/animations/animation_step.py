import pygame
from .animation_action import AnimationAction
from ..timers import Timer
from typing import Any

class AnimationStep:
    """A step of the transform animation. Can have different actions."""
    def __init__(self,time:float,sprite,transform_animation,*actions:AnimationAction):
        self.time:float = time
        """How much time for the step to end. <get>"""
        self.sprite = sprite
        """The sprite to apply the actions to. <get>"""
        self.actions:list[AnimationAction] = list(actions)
        """The action list. <get>"""
        self.timer:Timer = Timer(self.time,self.on_timer_end)
        """The timer to check the end of the step. <get>"""
        self.transform_animation = transform_animation
        """The parent transform animation. <get>"""
        
    def start(self)->None:
        """Internal method to start the step."""
        self.timer.activate()
        for a in self.actions:
            a.calculate_value(self.time)
        
    def new_action(self,action_type:str,value:Any)->AnimationAction:
        """Creates a new action."""
        action = AnimationAction(self.sprite,action_type,value)
        self.actions.append(action)
        return action
        
    def add_action(self,action:AnimationAction)->None:
        """Adds an action to the list."""
        self.actions.append(action)
        
    def on_timer_end(self)->None:
        """Internal function to end the step."""
        self.transform_animation.next()
        self.timer.deactivate()
            
    def update(self)->None:
        """Updates the actions and the timer."""
        for a in self.actions:
            a.apply()
        self.timer.update()
        