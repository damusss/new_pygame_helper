import pygame
from typing import Tuple,List,Union,Dict
#import sys
#sys.path.append("..")
from ...graphics.surface import *
from .sprite import Sprite

class SimpleAnimatedSprite(Sprite):
    """
    Inherit from the helper sprite class, useful to add a basic animation to it.
    """
    def __init__(self,frames:List[pygame.Surface],topleft_pos:Tuple[int,int]=None,groups:Union[pygame.sprite.Group,List[pygame.sprite.Group]]=[],z_index:int=0,frame_speed:float=0.2):
        self.frames = frames

        self.frame_index = 0
        self.old_frame_index = 0
        self.frame_speed = frame_speed

        self.image = self.frames[int(self.frame_index)]
        super().__init__(self.image,topleft_pos,groups,z_index)

    def set_frames(self,frames):
        """
        Set the frames and refresh them.
        """
        self.frames = frames
        
    def apply_transforms(self,resize_rect:bool=True)->pygame.Surface:
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.flip(self.image,self._flipped[0],self._flipped[1])
        newsizes = self.image.get_width()*self._scale[0],self.image.get_height()*self._scale[1]
        self.image = scale_image(self.image,None,newsizes)
        self.image = pygame.transform.rotate(self.image,self._angle)
        if resize_rect:
            self.resize_rect()
        return self.image

    def copy(self):
        """
        Return an exact copy of the sprite (note: only built in attributes are copied).
        """
        new = SimpleAnimatedSprite(frames=self.frames,groups=self.groups(),z_index=self.z_index,frame_speed=self.frame_speed)
        new.setup_attributes(self.direction,self.speed)
        new.set_parent(self.parent,self.parent_offset)
        for c in self.components:
            new.add_component(c.copy())
        if hasattr(self,"rect"):
            new.rect = self.rect.copy()
        if hasattr(self, "hitbox"):
            new.hitbox = self.hitbox.copy()
        new.image = self.image
        new.frame_index = self.frame_index
        return new

    def to_json(self,ignore_attributes:list=[])->dict:
        """
        Return a dictionary of the sprite that can be saved in a file, to be reloaded.
        """
        first = super().to_json(ignore_attributes)
        new = {}
        if not "frame_speed" in ignore_attributes:
            new["frame_speed"] = self.frame_speed
        if not "frames" in ignore_attributes:
            new["frames"] =[{"width":x.get_width(),"height":x.get_height()} for x in self.frames]
        if len(new.keys()) != 0:
            first.update(new)
        return first

    def from_json(self,json:dict,frames:list=[]):
        """
        Return a new sprite loaded from a dictionary.

        Since surfaces can't be properly saved, it's suggested to pass the frames here.
        """
        if len(frames)==0 and not "frames" in json.keys():
            raise AttributeError("Cannot create a new animated sprite without the frames in the argument or json.")
        if len(frames)>0:
            framess = frames 
        else:
            framess = [pygame.Surface((d["width"],d["height"])) for d in json["frames"]]
        new = super().from_json(json,framess)
        if "frame_speed" in json.keys():
            new.frame_speed = json["frame_speed"]
        return new

    def animate(self,kill_at_end:bool=False,dt:float=1.0,resize_rect=True)->None:
        """
        Update the frame index and the image.
        """
        self.old_frame_index = self.frame_index
        # loop over images
        self.frame_index += self.frame_speed*dt
        if self.frame_index >= len(self.frames):
            if kill_at_end:
                self.kill()
            else:
                self.frame_index = 0
        
        # change image
        if int(self.old_frame_index) != int(self.frame_index):
            self.apply_transforms(resize_rect)
        

class AnimatedSprite(Sprite):
    """
    Inherit from the helper sprite class, useful to create some complex animation with different types of them.
    """
    def __init__(self,animations_dict:Dict[str,List[pygame.Surface]],first_animation_name:str=None,topleft_pos:Tuple[int,int]=None,groups:Union[pygame.sprite.Group,List[pygame.sprite.Group]]=[],z_index:int=0,frame_speed=0.2):
        

        self.animations = animations_dict
        self.current_animation = first_animation_name if first_animation_name else list(animations_dict.keys())[0]

        self.frame_index = 0
        self.old_frame_index = 0
        self.frame_speed = frame_speed

        self.image = self.animations[self.current_animation][int(self.frame_index)]

        super().__init__(self.image,topleft_pos,groups,z_index)

    def set_animations(self,animations_dict:Dict[str,List[pygame.Surface]]):
        """
        Set the animations.
        """
        self.animations = animations_dict
        
    def apply_transforms(self,resize_rect:bool=True)->pygame.Surface:
        self.image = self.animations[self.current_animation][int(self.frame_index)]
        self.image = pygame.transform.flip(self.image,self._flipped[0],self._flipped[1])
        newsizes = self.image.get_width()*self._scale[0],self.image.get_height()*self._scale[1]
        self.image = scale_image(self.image,None,newsizes)
        self.image = pygame.transform.rotate(self.image,self._angle)
        if resize_rect:
            self.resize_rect()
        return self.image

    def copy(self):
        """
        Return an exact copy of the sprite (note: only built in attributes are copied).
        """
        new = AnimatedSprite(self.animations,self.current_animation,groups=self.groups(),z_index=self.z_index,frame_speed=self.frame_speed)
        new.setup_attributes(self.direction,self.speed)
        new.set_parent(self.parent,self.parent_offset)
        for c in self.components:
            new.add_component(c.copy())
        if hasattr(self,"rect"):
            new.rect = self.rect.copy()
        if hasattr(self, "hitbox"):
            new.hitbox = self.hitbox.copy()
        new.image = self.image
        new.frame_index = self.frame_index
        new.frame_speed = self.frame_speed
        return new

    def to_json(self,ignore_attributes:list=[])->dict:
        """
        Return a dictionary of the sprite that can be saved in a file, to be reloaded.
        """
        first = super().to_json(ignore_attributes)
        new = {}
        if not "frame_speed" in ignore_attributes:
            new["frame_speed"] = self.frame_speed
        if not "frames" in ignore_attributes:
            new["animations"] ={str(name):[{"width":i.get_width(),"height":i.get_height()} for i in self.animations[name]] for name in self.animations.keys()}
        if not "current_animation" in ignore_attributes:
            new["current_animation"] = self.current_animation
        if len(new.keys()) != 0:
            first.update(new)
        return first

    def from_json(self,json:dict,animations:dict=None,current_animation:str=None):
        """
        Return a new sprite loaded from a dictionary.

        Since surfaces can't be properly saved, it's suggested to pass the animations here.
        """
        if (not animations and not "animations" in json.keys()) or (not current_animation and not "current_animation" in json.keys()):
            raise AttributeError("Cannot create a new animated sprite without the animations or the current animation in the argument or json.")
        if animations:
            frames = animations 
        else:
            frames = {name:[pygame.Surface((i["width"],i["height"])) for i in json["animations"][name]] for name in json["animations"].keys() }
        if current_animation:
            current = current_animation
        else:
            current = json["current_animation"]
        new = super().from_json(json,frames,current)
        if "frame_speed" in json.keys():
            new.frame_speed = json["frame_speed"]
        return new

    def animate(self,dt:float=1.0,resize_rect=True)->None:
        """
        Update the frame index and the image.
        """
        self.old_frame_index = self.frame_index
        self.frame_index += self.frame_speed*dt
        if self.frame_index >= len(self.animations[self.current_animation]):
            self.frame_index = 0

        if int(self.old_frame_index) != int(self.frame_index):
            self.apply_transforms(resize_rect)