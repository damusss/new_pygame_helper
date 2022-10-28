import pygame
from typing import Tuple,List,Union
import sys
sys.path.append("..")
from graphics.surface import *
from events.events import AxisDirections

class Sprite(pygame.sprite.Sprite):
    """
    A sprite class with the addition of useful methods and attributes.
    """
    def __init__(self,image:pygame.Surface=None,topleft_pos:Tuple[int,int]=None,groups:Union[pygame.sprite.Group,List[pygame.sprite.Group]]=[],z_index:int=0):
        super().__init__(groups)

        self.z_index = z_index

        self.direction = pygame.math.Vector2()
        self.speed = pygame.math.Vector2()
        self.position = pygame.math.Vector2()

        if image:
            self.image = image
            if topleft_pos:
                self.rect = self.image.get_rect(topleft=topleft_pos)
                self.set_hitbox()
                self.refresh_position()
            self.original_image = self.image
            
        self._scale = (1,1)
        self._angle = 0
                
        self.parent = None
        self.parent_offset = pygame.math.Vector2()
        
        self.components = []
        
        self.visible = True
        
    def show(self):
        self.visible = True
        
    def hide(self):
        self.visible = False
        
    def setup_attributes(self,direction:Tuple[int,int]=(0,0),speed:Tuple[float,float]=(0,0)):
        self.direction = pygame.math.Vector2(direction)
        self.speed = pygame.math.Vector2(speed)
        
    def set_parent(self,parent=None,parent_offset:Tuple[int,int]=(0,0)):
        self.parent = parent
        self.parent_offset = pygame.math.Vector2(parent_offset)
        
    def update_components(self):
        for c in self.components:
            c.update()
            
    def add_component(self,component):
        self.components.append(component)
        
    def remove_components(self,component):
        self.components.remove(component)
        
    def set_original_image(self):
        self.original_image = self.image

    def handle_event(self,event:pygame.event.Event):
        """
        Override this method.
        """
        pass

    def copy(self):
        """
        Return an exact copy of the sprite (note: only built in attributes are copied).
        """
        new = Sprite(groups=self.groups(),z_index=self.z_index,topleft_pos= self.rect.topleft)
        new.setup_attributes(self.direction,self.speed)
        new.set_parent(self.parent,self.parent_offset)
        for c in self.components:
            new.add_component(c.copy())
        if hasattr(self,"rect"):
            new.rect = self.rect.copy()
        if hasattr(self, "hitbox"):
            new.hitbox = self.hitbox.copy()
        if hasattr(self,"image"):
            new.image = self.image
        return new

    def to_json(self,ignore_attributes:list=[])->dict:
        """
        Return a dictionary of the sprite that can be saved in a file, to be reloaded.
        """
        json = {}
        if not "z_index" in ignore_attributes:
            json["z_index"] = self.z_index
        if not "direction" in ignore_attributes:
            json["direction"] = {"x":self.direction.x,"y":self.direction.y}
        if not "speed" in ignore_attributes:
            json["speed"] = {"x":self.speed.x,"y":self.speed.y}
        if not "position" in ignore_attributes:
            json["position"] = {"x":self.position.x,"y":self.position.y}

        if hasattr(self, "image") and not "image" in ignore_attributes:
            json["image"] = {"width":self.image.get_width(),"height":self.image.get_height()}
        if hasattr(self, "rect") and not "rect" in ignore_attributes:
            json["rect"] = {"x":self.rect.x,"y":self.rect.y,"w":self.rect.w,"h":self.rect.h,"centerx":self.rect.centerx,"centery":self.rect.centery}
        if hasattr(self, "hitbox") and not "hitbox" in ignore_attributes:
            json["hitbox"] = {"x":self.hitbox.x,"y":self.hitbox.y,"w":self.hitbox.w,"h":self.hitbox.h,"centerx":self.hitbox.centerx,"centery":self.hitbox.centery}
        
        if not "groups" in ignore_attributes:
            json["groups"] = {"len":len(self.groups()),"types":[g.__class__.__name__ for g in self.groups()]}
        return json

    def from_json(self,json:dict,*other_args):
        """
        Return a new sprite loaded from a dictionary.
        """
        new = self.__class__(*other_args)
        keys = json.keys()
        if "z_index" in keys:
            new.z_index = json["z_index"]

        if "direction" in keys:
            new.direction.xy = (json["direction"]["x"],json["direction"]["y"])
        if "speed" in keys:
            new.speed.xy = (json["speed"]["x"],json["speed"]["y"])
        if "position" in keys:
            new.position.xy = (json["position"]["x"],json["position"]["y"])

        if "image" in keys:
            new.image = pygame.Surface((json["image"]["width"],json["image"]["height"]))
        if "rect" in keys:
            if "image" in keys:
                new.rect = new.image.get_rect(center=(json["rect"]["centerx"],json["rect"]["centery"]))
            else:
                new.rect = pygame.Rect(json["rect"]["x"], json["rect"]["y"], json["rect"]["w"], json["rect"]["h"])
        if "hitbox" in keys and "rect"in keys:
            new.hitbox = pygame.Rect(json["hitbox"]["x"], json["hitbox"]["y"], json["hitbox"]["w"], json["hitbox"]["h"])

        return new

    def set_hitbox(self,hitbox_inflate:Union[Tuple[int,int],List[int],pygame.math.Vector2]=(0,0))->pygame.Rect:
        """
        Setup the hitbox !after rect creation!
        """
        self.hitbox = self.rect.inflate(hitbox_inflate[0], hitbox_inflate[1])
        return self.hitbox

    def draw(self,surface:pygame.Surface)->None:
        """
        Draw the image on the screen.
        """
        if self.visible:
            surface.blit(self.image,self.rect)

    def draw_rect(self,surface,color="white",width:int=2,border_radius:int=0):
        """
        Draw the sprite rect.
        """
        pygame.draw.rect(surface, color, self.rect,width,border_radius)

    def is_on_screen(self,dokill:bool=False,surface:pygame.Surface=None)->bool:
        """
        Check if the sprite is inside the window
        """
        if not surface:
            surface = pygame.display.get_surface()
        if self.rect.right > 0 and self.rect.left < surface.get_width() and self.rect.bottom > 0 and self.rect.top < surface.get_height():
            return True
        return False

    def check_collision(self,sprite):
        """
        Check the collision with another sprite.
        """
        return self.rect.colliderect(sprite.rect)

    def mouse_collision(self):
        """
        Check if the mouse is hovering the sprite.
        """
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos[0], pos[1] )

    def refresh_position(self):
        """
        Set the position to the center of the rectangle (useful after changing the rectangle position manually).
        """
        self.position.xy = self.rect.center

    def update_position(self,direction=AxisDirections.horizontal,dt=1):
        """
        Update the position and rectangle position of the sprite using the speed and direction. 

        You have to specify if you want to update the horizontal or vertical direction, Otherwise use 'update_positions'.
        """
        if direction == AxisDirections.horizontal:
            self.position.x += self.direction.x*self.speed.x*dt
            self.rect.centerx = round(self.position.x)
            self.hitbox.centerx = self.rect.centerx
        elif direction == AxisDirections.vertical:
            self.position.y += self.direction.y*self.speed.y*dt
            self.rect.centery = round(self.position.y)
            self.hitbox.centery = self.rect.centery

    def update_positions(self,dt=1):
        """
        Update the position of both the directions. Check 'update_position' for more.
        """
        self.update_position("h",dt)
        self.update_position("v",dt)

    def normalize_direction(self):
        """
        Normalize the direction of the sprite.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def collision(self,collision_group,direction=AxisDirections.horizontal,on_collision_func=None):
        """
        Check the collisions between itself and a list of sprites. Both needs to have an hitbox.

        After collision detection the sprite will be moved to stop the collision.

        You have to specify in which direction to check collisions, Otherwise, use 'collsions'.
        """
        for sprite in collision_group.sprites():
            if hasattr(sprite, "hitbox"):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == AxisDirections.horizontal:
                        if self.direction.x > 0 and self.hitbox.left < sprite.hitbox.left:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0 and self.hitbox.right > sprite.hitbox.right:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.position.x = self.hitbox.centerx

                    if direction == AxisDirections.vertical:
                        if self.direction.y > 0 and self.hitbox.top < sprite.hitbox.top:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0 and self.hitbox.bottom > sprite.hitbox.bottom:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.position.y = self.hitbox.centery
                    if on_collision_func:
                        on_collision_func(sprite,direction)

    def collisions(self,collision_group,on_collision_func=None):
        """
        Check collisions in both directions. For more check 'collision'.
        """
        self.collision(collision_group,"h",on_collision_func)
        self.collision(collision_group,"v",on_collision_func)

    def resize_rect(self):
        """
        Resize the rect to the image size, keeping the position. Useful after changing image.
        """
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_scale(self,scalex:float=1,scaley:float=1,smooth:bool=False)->pygame.Surface:
        """
        Scale the sprite and resize the rect.
        """
        self._scale = (scalex,scaley)
        scaled_w,scaled_h = self.original_image.get_width()*scalex,self.original_image.get_height()*scaley
        self.image = scale_image(self.original_image,None,(scaled_w,scaled_h))
        self.image = pygame.transform.rotate(self.image, self._angle)
        self.resize_rect()
        return self.image

    def flip(self,horizontal:bool,vertical:bool)->pygame.Surface:
        """
        Flip the sprite and resize the rect.
        """
        self.image = pygame.transform.flip(self.image,horizontal,vertical)
        self.resize_rect()
        return self.image

    def rotate(self,angle:int):
        """
        Rotate the sprite and resize the rect.
        """
        self._angle += angle
        scaled_w,scaled_h = self.original_image.get_width()*self._scale[0],self.original_image.get_height()*self._scale[1]
        self.image = scale_image(self.original_image,None,(scaled_w,scaled_h))
        self.image = pygame.transform.rotate(self.image, self._angle)
        self.resize_rect()
        return self.image

    def stick_to_parent(self):
        """
        Set its position to the parent position offsetted.
        """
        if self.parent:
            self.position = self.parent_offset+self.parent.position
            
    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self,value):
        self.set_scale(value[0],value[1])
        
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self,value):
        self.rotate(value-self._angle)