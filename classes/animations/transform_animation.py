import pygame
from .animation_step import AnimationStep
from .animation_action import AnimationAction

transform_animation_schedule_example = {
    "steps":[
        {"time":2000,
         "actions":[
            {"type":"position","value":(200,100)},
            {"type":"angle","value":45},
            {"type":"scale","value":(1,2)}
         ]}
    ]
}

class TransformAnimation:
    def __init__(self,sprite,loop = False,single_step=False,schedule = None,on_next_step_func=None):
        self.sprite = sprite
        self.loop = loop
        self.steps = []
        if single_step:
            self.new_step(0.1)
        
        self.current_step = None
        self.current_index = 0
        
        self.set_initial_sprite()
        
        self.schedule:dict = schedule
        if self.schedule:
            self.apply_schedule()
            
        self.on_next = on_next_step_func
            
    def set_initial_sprite(self):
        self.initial_sprite = {
            "pos":self.sprite.position.xy,
            "dir":self.sprite.direction.xy,
            "speed":self.sprite.speed.xy,
            "angle":self.sprite.angle,
            "scale":self.sprite.scale
        }
        
        
    def apply_schedule(self):
        steps = self.schedule["steps"]
        for step in steps:
            actions = step["actions"]
            actual_actions = []
            for a in actions:
                actual_actions.append(AnimationAction(self.sprite,a["type"],a["value"]))
            self.steps.append(AnimationStep(step["time"],self.sprite,self,*actual_actions))
        
    def new_step(self,time,*actions):
        self.steps.append(AnimationStep(time,self.sprite,self,*actions))
        
    def add_step(self,step):
        self.steps.append(step)
        
    def restart(self):
        self.stop()
        self.back_to_start_condition()
        self.play()
        
    def play(self):
        self.set_initial_sprite()
        if self.steps:
            self.current_step = self.steps[0]
            self.current_index = 0
            self.current_step.start()
        
    def next(self):
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
                
    def back_to_start_condition(self):
        self.sprite.position.xy = self.initial_sprite["pos"]
        self.sprite.rect.center = (round(self.sprite.position.x),round(self.sprite.position.y))
        self.sprite.hitbox.center = self.sprite.rect.center
        self.sprite.direction.xy = self.initial_sprite["dir"]
        self.sprite.speed.xy = self.initial_sprite["speed"]
        self.sprite.set_scale(self.initial_sprite["scale"][0],self.initial_sprite["scale"][1])
        self.sprite.angle = self.initial_sprite["angle"]
                
    def is_playing(self):
        return self.current_step != None
    
    def stop(self):
        self.current_step = None
        self.current_index = 0
        
    def update(self):
        if self.current_step != None:
            self.current_step.update()