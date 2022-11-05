import pygame
from .animation_step import AnimationStep
from .animation_action import AnimationAction
from typing import Any

transform_animation_schedule_example:dict[str,list[dict[str,Any]]] = {
    "steps":[
        {"time":2000,
         "actions":[
            {"type":"position","value":(200,100)},
            {"type":"scale","value":(1,2)},
            {"type":"angle","value":45},
         ]},
        {
            "time":1000,
            "actions":[
                {"type":"position","value":(-200,100)},
                {"type":"scale","value":(1,1)},
                {"type":"angle","value":-45},
            ]
        }
    ]
}
"""Example of an animation schedule for the transform animation."""

class TransformAnimation:
    """
    Animates a sprite changing the transforms of it.
    """
    schedule_example:dict[str,list[dict[str,Any]]] = transform_animation_schedule_example
    """Example of an animation schedule."""
    def __init__(self,sprite,loop:bool = False,single_step:bool=False,schedule:dict[str,list[dict[str,Any]]] = None,on_next_step_func=None):
        self.sprite = sprite
        """The sprite to apply actions to. <get>"""
        self.loop:bool = loop
        """Whether the animation should loop. <get, set>"""
        self.steps:list[AnimationStep] = []
        """The steps list. <get>"""
        if single_step:
            self.new_step(0.1)
        
        self.current_step:AnimationStep = None 
        """The current playing step. <get>"""
        self.current_index:int = 0
        """The current playing step index. <get>"""
        
        self.set_initial_sprite()
        
        self.schedule:dict[str,list[dict[str,Any]]] = schedule
        """The schedule to follow. <get>"""
        if self.schedule:
            self.apply_schedule()
            
        self.on_next = on_next_step_func
        """The function to run when a step starts to play. <get>"""
            
    def set_initial_sprite(self)->None:
        """
        Remembers the attributes of the sprite before it plays.
        """
        self.initial_sprite = {
            "pos":self.sprite.position.xy,
            "dir":self.sprite.direction.xy,
            "speed":self.sprite.speed.xy,
            "angle":self.sprite.angle,
            "scale":self.sprite.scale
        }
        
        
    def apply_schedule(self)->None:
        """
        Applies the schedule.
        """
        steps = self.schedule["steps"]
        for step in steps:
            actions = step["actions"]
            actual_actions = []
            for a in actions:
                actual_actions.append(AnimationAction(self.sprite,a["type"],a["value"]))
            self.steps.append(AnimationStep(step["time"],self.sprite,self,*actual_actions))
        
    def new_step(self,time:float,*actions:AnimationAction)->AnimationStep:
        """
        Creates a new step.
        """
        step = AnimationStep(time,self.sprite,self,*actions)
        self.steps.append(step)
        return step
        
    def add_step(self,step:AnimationStep)->None:
        """Adds a step to the list."""
        self.steps.append(step)
        
    def restart(self)->None:
        """
        Restarts the animation.
        """
        self.stop()
        self.back_to_start_condition()
        self.play()
        
    def play(self)->None:
        """
        Plays the animation.
        """
        self.set_initial_sprite()
        if self.steps:
            self.current_step = self.steps[0]
            self.current_index = 0
            self.current_step.start()
        
    def next(self)->None:
        """
        Internal method for going to the next step.
        """
        new_i = self.current_index + 1
        if new_i <= len(self.steps)-1:
            self.current_step = self.steps[new_i]
            self.current_index = new_i
            self.current_step.start()
            if self.on_next:
                self.on_next()
        else:
            if self.loop:
                self.back_to_start_condition()
                self.play()
                if self.on_next:
                    self.on_next()
            else:
                self.stop()
                
    def back_to_start_condition(self)->None:
        """
        Brings the sprite to the starting state.
        """
        self.sprite.position.xy = self.initial_sprite["pos"]
        self.sprite.rect.center = (round(self.sprite.position.x),round(self.sprite.position.y))
        self.sprite.hitbox.center = self.sprite.rect.center
        self.sprite.direction.xy = self.initial_sprite["dir"]
        self.sprite.speed.xy = self.initial_sprite["speed"]
        self.sprite.set_scale(self.initial_sprite["scale"][0],self.initial_sprite["scale"][1])
        self.sprite.angle = self.initial_sprite["angle"]
                
    def is_playing(self)->None:
        """Checks if the animation is playing."""
        return self.current_step != None
    
    def stop(self)->None:
        """Stops the animation."""
        self.current_step = None
        self.current_index = 0
        
    def update(self):
        """Updates the animation."""
        if self.current_step != None:
            self.current_step.update()