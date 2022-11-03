import pygame
#from ..sprites.sprite import Sprite

class AnimationActions:
    position = "position"
    direction = "direction"
    speed = "speed"
    angle = "angle"
    scale = "scale"
    
class AnimationAction:
    def __init__(self,sprite,action_type,value):
        self.sprite = sprite
        self.value = value
        self.type = action_type
        self.update_value = None
        self.last_milli = pygame.time.get_ticks()
        
    def calculate_value(self,time):
        match self.type:
            case AnimationActions.position:
                self.update_value = pygame.Vector2(self.value[0]/time,self.value[1]/time)
            case AnimationActions.direction:
                self.update_value = pygame.Vector2(self.value[0]/time,self.value[1]/time)
            case AnimationActions.speed:
                self.update_value = pygame.Vector2(self.value[0]/time,self.value[1]/time)
            case AnimationActions.angle:
                self.update_value = self.value/time
            case AnimationActions.scale:
                self.update_value = pygame.Vector2((self.value[0]-1)/time,(self.value[1]-1)/time)
        
    def apply(self):
        current = pygame.time.get_ticks()
        dt = (current-self.last_milli)
        match self.type:
            case AnimationActions.position:
                self.sprite.position+=self.update_value*dt
                self.sprite.rect.center = (round(self.sprite.position.x),round(self.sprite.position.y))
                self.sprite.hitbox.center = self.sprite.rect.center
            case AnimationActions.direction:
                self.sprite.direction+=self.update_value*dt
            case AnimationActions.speed:
                self.sprite.speed+=self.update_value*dt
            case AnimationActions.angle:
                self.sprite.angle += self.update_value*dt
            case AnimationActions.scale:
                start = self.sprite.scale
                self.sprite.set_scale(start[0]+self.update_value[0]*dt,start[1]+self.update_value[1]*dt)
        self.last_milli = current
                    