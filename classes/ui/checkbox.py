import pygame
from .image import UIImage

class UICheckBox:
    def __init__(self,topleft_pos,size,checkbox_on_image,on_toggle_change_func=None,start_on=False,bg_color=(50,50,50),outline_color=(20,20,20),click_button=0):
        self.size = size
        self.bg_color = bg_color
        self.outline_color = outline_color
        self.on_image = checkbox_on_image
        self.on_toggle = on_toggle_change_func
        self.button = click_button
        
        i1 = pygame.Surface((size,size))
        i1.fill(self.bg_color)
        self.bg_image = UIImage(i1,topleft_pos,self.outline_color)
        self.on_image_rect = self.on_image.get_rect(center=(self.bg_image.rect.centerx-self.bg_image.outline_size//2,self.bg_image.rect.centery-self.bg_image.outline_size//2))
        
        self.is_on = start_on
        
        self.visible = True
        
        self.clicked = False
        
    def draw(self,surface):
        if self.visible:
            self.bg_image.draw(surface)
            if self.is_on:
                surface.blit(self.on_image,self.on_image_rect)
        
    def update(self):
        pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        if self.bg_image.rect.collidepoint(pos):
            if mouse[self.button]:
                if self.clicked == False:
                    self.is_on = not self.is_on
                    self.clicked = True
                    if self.on_toggle:
                        self.on_toggle()

            if not mouse[self.button]:
                self.clicked = False
        
    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
        
    def _ui_group_on_pos_change(self, group_pos):
        self.bg_image._ui_group_on_pos_change(group_pos)
        self.on_image_rect.center = (self.bg_image.rect.centerx-self.bg_image.outline_size//2,self.bg_image.rect.centery-self.bg_image.outline_size//2)

    def _ui_group_set_offset(self):
        self.bg_image._ui_group_set_offset()