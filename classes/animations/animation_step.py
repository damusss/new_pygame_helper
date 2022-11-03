import pygame
from .animation_action import AnimationAction
from ..timers import Timer

class AnimationStep:
    def __init__(self,time,sprite,transform_animation,*actions):
        self.time = time
        self.sprite = sprite
        self.actions = list(actions)
        self.timer = Timer(self.time,self.on_timer_end)
        self.transform_animation = transform_animation
        
    def start(self):
        self.timer.activate()
        for a in self.actions:
            a.calculate_value(self.time)
        
    def new_action(self,action_type,value):
        self.actions.append(AnimationAction(self.sprite,action_type,value))
        
    def add_action(self,action):
        self.actions.append(action)
        
    def on_timer_end(self):
        self.transform_animation.next()
        self.timer.deactivate()
            
    def update(self):
        for a in self.actions:
            a.apply()
        self.timer.update()
        