import pygame
from ..graphics.surface import scale_image

"""Contains the Zoom class."""

class Zoom:
    """Creates a zoomable and draggable surface to use instead of the main one."""
    def __init__(self,topleft_pos:tuple[int,int]|pygame.Vector2,map_size:tuple[int,int],min_zoom:float=1,max_zoom:float=2,zoom_speed:float=0.1):
        self.map_size:tuple[int,int] = map_size
        """The size of the surface. <get>"""
        self.surface:pygame.Surface = pygame.Surface(self.map_size)
        """The actual surface to use to blit things on. <get>"""
        self.scaled:pygame.Surface = self.surface
        """The scaled surface that is blit to the main one. <get>"""
        self.rect:pygame.Rect = self.scaled.get_rect(topleft=topleft_pos)
        """The rect of the scaled surface. <get>"""
        self.scale:float = 1
        """The current scale. <get>"""
        self.min_scale:float = min_zoom
        """The minimun scale. <get, set>"""
        self.max_scale:float = max_zoom
        """The maximum scale. <get, set>"""
        self.speed:float = zoom_speed
        """The zoom speed. <get, set>"""
        self.main_surface_rect = pygame.display.get_surface().get_rect(topleft=(0,0))
        
    def set_scale(self,scale:float,bypass_limits:bool=False)->None:
        """Manually sets the scale."""
        self.scale = scale
        if not bypass_limits:
            if self.scale < self.min_scale:
                self.scale = self.min_scale
            elif self.scale > self.max_scale:
                self.scale = self.max_scale
        self.scaled = scale_image(self.surface,self.scale)
        self.rect = self.scaled.get_rect(center=self.rect.center)
        
    def clear(self,color:str|tuple[int,int,int]|pygame.Color="black")->None:
        """Clears the surface. at the end/start of the frame."""
        self.surface.fill(color)
        
    def draw(self,main_surface:pygame.Surface,zooming_enabled:bool=True)->None:
        """Draws the scaled surface on the main surface."""
        if zooming_enabled:
            self.scaled = scale_image(self.surface,self.scale)
            self.rect = self.scaled.get_rect(center=self.rect.center)
        main_surface.blit(self.scaled,self.rect)
        
    def zoom_event(self,event:pygame.event.Event)->None:
        """Call this in the event loop to enable zooming."""
        if event.type == pygame.MOUSEWHEEL:
            self.scale += event.y*self.speed
            if self.scale < self.min_scale:
                self.scale = self.min_scale
            elif self.scale > self.max_scale:
                self.scale = self.max_scale
            self.scaled = scale_image(self.surface,self.scale)
            self.rect = self.scaled.get_rect(center=self.rect.center)
            
    def drag_event(self,event:pygame.event.Event,button:int=0)->None:
        """Call this in the event loop to enable dragging."""
        mouse = pygame.mouse.get_pressed()
        if mouse[button]:
            if event.type == pygame.MOUSEMOTION:
                self.rect.center = (self.rect.centerx+event.rel[0],self.rect.centery+event.rel[1])
                
    def relative_point(self,x:float,y:float)->tuple[float,float]:
        """Returns a point relative to the scaled surface."""
        return (x-self.rect.topleft[0],y-self.rect.topleft[1])