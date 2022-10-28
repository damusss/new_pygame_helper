import pygame
from typing import List,Dict,Any,Type
from ..sprites.sprite import Sprite

class Group(pygame.sprite.Group):
    """
    A pygame group that allows json serialization.
    """
    def __init__(self):
        super().__init__()

    def to_json(self,ignore_attributes=[])->list:
        """
        Return a list of the serialized sprites using their own to_json methods.
        """
        sprites = []
        for sprite in self.sprites():
            if hasattr(sprite, "to_json"):
                json = sprite.to_json(ignore_attributes)
                sprites.append(json)
            else:
                raise AttributeError("Sprites need to have the to_json method defined in order to be serialized.")
        return sprites

    def from_json(self,json:List[Dict[str,Any]],sprite_type:Type,*from_json_extra_args)->list:
        """
        Create the sprites from a list of dictionaries to then add them to itself.
        """
        example = sprite_type()
        for sprite in json:
            if hasattr(example, "from_json"):
                s = example.from_json(sprite,from_json_extra_args)
                self.add(s)
            else:
                raise AttributeError("Sprites need to have the from_json method defined in order to be deserialized.")

class CameraGroup(Group):
    """
    Very useful for games with a camera like Stardew Valley.
    """
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()

    def draw(self,screen:pygame.Surface,main_sprite:Sprite,layers:list,screen_center:tuple)->None:
        """
        Draw the sprites sorting them by y coordinate and by layer, positioning the camera to the center of the main sprite.

        The sprites needs to have a z_index, rect and image.
        """
        self.offset.x = main_sprite.rect.centerx - screen_center[0]
        self.offset.y = main_sprite.rect.centery - screen_center[1]

        for layer in layers.values():
            for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
                if sprite.z_index == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset

                    screen.blit(sprite.image, offset_rect)

                    
class StaticGroup(Group):
    def __init__(self,surface_size,topleft_pos,background_color="black"):
        super().__init__()
        
        self.surface_size = surface_size
        self.background_color = background_color
        self.surface = pygame.Surface(surface_size)
        self.surface.set_colorkey("black")
        self.surface.fill(self.background_color)
        self.topleft_pos = topleft_pos
        
    def resize(self,new_size):
        self.surface_size = new_size
        self.surface = pygame.Surface(self.surface_size)
        self.refresh()
        
    def change_bg_color(self,new_color):
        self.background_color = new_color
        self.refresh()
        
    def refresh(self):
        self.surface.fill(self.background_color)
        for s in self.sprites():
            s.draw(self.surface)
            
    def draw(self,surface):
        surface.blit(self.surface,self.topleft_pos)
