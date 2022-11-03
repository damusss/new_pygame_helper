import pygame
from .window import UIWindow

class UIWindowStack:
    def __init__(self):
        self.visible = True
        
        self.windows:list[UIWindow] = []
        
    def is_at_front(self,window):
        return window == self.windows[-1]
    
    def bring_to_front(self,window):
        self.windows.remove(window)
        self.windows.append(window)
            
        
    def add(self,*window):
        for w in window:
            self.windows.append(w)
        
    def remove(self,window):
        self.windows.remove(window)
    
    def draw(self,surface):
        if self.visible:
            for w in self.windows:
                w.draw(surface)
    
    def update(self):
        if self.visible:
            for w in self.windows:
                w.update()
            self.update_clicks()
                
    def update_clicks(self):
        
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            pos = pygame.mouse.get_pos()
            for w in reversed(self.windows):
                if w.hover_area.collidepoint(pos):
                    if w.visible:
                        if not self.is_at_front(w): 
                            self.bring_to_front(w)
                        return
            
    def get_hovering_window(self):
        pos = pygame.mouse.get_pos()
        for w in self.windows:
            if w.hover_area.collidepoint(pos):
                if w.visible:
                    return w
        return None