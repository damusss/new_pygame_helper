import pygame
from .group import UIGroup
from .image import UIImage
from .buttons import UITextButton
from .text import UIText

class UIWindow:
    def __init__(self,topleft_pos,width,height,title_text,on_close_func=None,bg_color=(50,50,50),outlines_color=(20,20,20),title_bar_height=30,close_btn_width=30,close_btn_txt="X",on_drag_func=None):
        self.width = width
        self.height = height
        self.title = title_text
        self.bg_color = bg_color
        self.outlines_color = outlines_color
        self.title_bar_h = title_bar_height
        self.close_btn_w = close_btn_width
        self.content_start_height = self.title_bar_h
        self.on_close_func = on_close_func
        self.on_drag_func = on_drag_func
        
        i1 = pygame.Surface((self.width-self.close_btn_w,self.title_bar_h))
        i1.fill(self.bg_color)
        i2 = pygame.Surface((self.width,self.height-self.title_bar_h))
        i2.fill(bg_color)
        i3 = pygame.Surface((self.close_btn_w,self.title_bar_h))
        i3.fill(self.bg_color)
        self.title_bar = UIImage(i1,(0,0),self.outlines_color)
        
        self.close_bg = UIImage(i3,(self.width-self.close_btn_w,0),self.outlines_color)
        close_text = UIText(self.close_bg.rect.center,None,self.title.font,close_btn_txt,self.title.color,self.title.antialiasing)
        iw,ih = (self.close_btn_w-close_text.rect.w)//2,(self.title_bar_h-close_text.rect.h)//2
        self.close_button = UITextButton(close_text,(iw,ih),self.on_close_button_pressed)
        self.content_image = UIImage(i2,(0,self.title_bar_h),self.outlines_color)
        
        self.group = UIGroup(topleft_pos,self.width-self.close_btn_w,self.title_bar_h,self.on_drag_func)
        self.group.add(self.title_bar,self.content_image,self.close_bg,self.close_button,self.title)
        
        self.visible = True
        
    def add(self,*elements):
        self.group.add(*elements)
        
    def on_close_button_pressed(self):
        if self.on_close_func:
            self.on_close_func()
        else:
            self.hide()
        
    def show(self):
        self.visible = True
        
    def hide(self):
        self.visible = False
    
    def draw(self,surface):
        if self.visible:
            self.group.draw(surface)
    
    def update(self):
        if self.visible:
            self.group.update()
            
    def offset_height(self,relative_height):
        return self.content_start_height+relative_height