import pygame
from typing import Any

class AnimationActions:
    """The different transforms you can change."""
    position:str = "position"
    """Changes the position."""
    direction:str = "direction"
    """Changes the direction."""
    speed:str = "speed"
    """Changes the speed."""
    angle:str = "angle"
    """Changes the rotation."""
    scale:str = "scale"
    """Changes the scale."""
    
class AnimationAction:
    """The action that mpdify the sprite. Give an appropriate value for the type selected."""
    def __init__(self,sprite,action_type:str,value:Any):
        self.sprite = sprite
        """The sprite to modify. <get>"""
        self.value:Any = value
        """The desired value. <get>"""
        self.type:str = action_type
        """The action type. <get>"""
        self.update_value:Any = None
        """The value that will be applied every frame. Depends of the time. <get>"""
        self.last_milli:float = pygame.time.get_ticks()
        """The last pygame tick. <get>"""
        
    def calculate_value(self,time:float)->None:
        """Internal method to calclulate the update_value."""
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
        
    def apply(self)->None:
        """Applies the update_value to the sprite."""
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
                    