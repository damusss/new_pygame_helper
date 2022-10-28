import pygame

class _GlobalInput:
    def __init__(self):
        self.buttons = pygame.mouse.get_pressed()
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.relative_mouse_pos = self.mouse_pos
    
    def update(self,inner_surface_map_pos=None):
        self.buttons = pygame.mouse.get_pressed()
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        if inner_surface_map_pos:
            self.relative_mouse_pos = (self.mouse_pos[0]-inner_surface_map_pos[0],self.mouse_pos[1]-inner_surface_map_pos[1])