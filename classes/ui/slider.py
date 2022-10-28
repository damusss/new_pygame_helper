import pygame
from .image import UIImage

class SliderDirections:
    horizontal = "horizontal"
    vertical = "vertical"

class UISlider:
    def __init__(self,topleft_pos,bar_width,bar_height,min_value,max_value,slider_button_surface:pygame.Surface,direction=SliderDirections.horizontal,on_value_change_func=None,bar_bg_color=(60,60,60),bar_outline_color=(20,20,20)):
        
        self.direction = direction
        if self.direction != SliderDirections.horizontal and self.direction != SliderDirections.vertical:
            raise Exception("Slider direction can only be either horizontal or vertical.")
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_value_change_func
        self.value = (self.min_value+self.max_value)/2
        if self.direction == SliderDirections.horizontal:
            i1 = pygame.Surface((bar_width,bar_height))
            i1.fill(bar_bg_color)
        else:
            i1 = pygame.Surface((bar_height,bar_width))
            i1.fill(bar_bg_color)
            
        self.bar_image = UIImage(i1,topleft_pos,bar_outline_color)
        
        self.button_image = slider_button_surface
        self.button_rect = self.button_image.get_rect(center=self.bar_image.rect.center)
        if self.direction == SliderDirections.horizontal:
            self.fixed_pos = self.bar_image.rect.centery-self.bar_image.outline_size
            self.button_rect.centery = self.fixed_pos
        else:
            self.fixed_pos = self.bar_image.rect.centerx-self.bar_image.outline_size
            self.button_rect.centerx = self.fixed_pos
            
        self.was_pressing = False
        self.relative = pygame.math.Vector2()
        
        self.visible = True
        
        self.was_pressing_outside = False
        
    def calculate_current_value(self):
        if self.direction == SliderDirections.horizontal:
            max_pos = self.bar_image.rect.right-self.bar_image.rect.left
            current_pos = self.button_rect.centerx-self.bar_image.rect.left
            total_value = self.max_value-self.min_value
            result = (current_pos*total_value)/max_pos
            result += self.min_value
            self.value = result
        else:
            max_pos = self.bar_image.rect.bottom-self.bar_image.rect.top
            current_pos = self.button_rect.centery-self.bar_image.rect.top
            total_value = self.max_value-self.min_value
            result = (current_pos*total_value)/max_pos
            result += self.min_value
            self.value = result
        
    def update(self):
        if self.visible:
            mouse = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            
            if mouse[0]:
                if self.was_pressing and not self.was_pressing_outside:
                    temp = pos
                    if self.direction == SliderDirections.horizontal:
                        temp = (temp[0],self.fixed_pos)
                        if temp[0] < self.bar_image.rect.left:
                            temp = (self.bar_image.rect.left,self.fixed_pos)
                        elif temp[0] > self.bar_image.rect.right:
                            temp = (self.bar_image.rect.right,self.fixed_pos)
                        self.button_rect.center = temp
                    else:
                        temp = (self.fixed_pos,temp[1])
                        if temp[1] < self.bar_image.rect.top:
                            temp = (self.fixed_pos,self.bar_image.rect.top)
                        elif temp[1] > self.bar_image.rect.bottom:
                            temp = (self.fixed_pos,self.bar_image.rect.bottom)
                        self.button_rect.center = temp
                    old = self.value
                    self.calculate_current_value()
                    if old != self.value:
                        if self.on_change:
                            self.on_change()
                    
                else:
                    if self.button_rect.collidepoint(pos):
                        self.was_pressing = True
                    else:
                        self.was_pressing_outside = True
        
        if not mouse[0]:
            self.was_pressing = False
            self.was_pressing_outside = False
            
    def draw(self,surface):
        if self.visible:
            self.bar_image.draw(surface)
            surface.blit(self.button_image,self.button_rect)
            
    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
        
    def _ui_group_on_pos_change(self, group_pos):
        offset = (self.button_rect.centerx-self.bar_image.rect.centerx,self.button_rect.centery-self.bar_image.rect.centery)
        self.bar_image._ui_group_on_pos_change(group_pos)
        if self.direction == SliderDirections.horizontal:
            self.fixed_pos = self.bar_image.rect.centery-self.bar_image.outline_size//2
        else:
            self.fixed_pos = self.bar_image.rect.centerx-self.bar_image.outline_size
        self.button_rect.center = (self.bar_image.rect.centerx+offset[0],self.bar_image.rect.centery+offset[1])

    def _ui_group_set_offset(self):
        self.bar_image._ui_group_set_offset()
        if self.direction == SliderDirections.horizontal:
            self.fixed_pos = self.bar_image.rect.centery-self.bar_image.outline_size
        else:
            self.fixed_pos = self.bar_image.rect.centerx-self.bar_image.outline_size
        
        