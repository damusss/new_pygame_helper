import pygame
from .text import UIText
from .image import UIImage
from .buttons import UITextButton

class DropDownDirections:
    up = "up"
    down = "down"

class UIDropDown:
    def __init__(self,topleft_pos,width,height,option_height,options,selected_option,example_text:UIText,on_option_change_func=None,direction=DropDownDirections.down,arrow_down_btn_width=30,arrow_down_char="\u25bc",arrow_up_char="\u25b2",bg_color=(60,60,60),outlines_color=(20,20,20)):
        self.options = options
        self.selected_option = selected_option
        self.on_change = on_option_change_func
        self.direction = direction
        if self.direction != DropDownDirections.down and self.direction != DropDownDirections.up:
            raise Exception("DropDown direction can only be either up or down.")
        
        i1 = pygame.Surface((width,height))
        i1.fill(bg_color)
        
        self.main_image = UIImage(i1,topleft_pos,outlines_color)
        
        i3 = pygame.Surface((arrow_down_btn_width,height))
        i3.fill(bg_color)
        self.arrow_down_image =UIImage(i3,(topleft_pos[0]+width,topleft_pos[1]),outlines_color)
        arrow_down_text = UIText(self.arrow_down_image.rect.center,None,example_text.font,arrow_down_char if self.direction == DropDownDirections.down else arrow_up_char,example_text.color,example_text.antialiasing)
        iw2,ih2 = (arrow_down_btn_width-arrow_down_text.rect.w)/2,(height-arrow_down_text.rect.h)/2
        self.arrow_down_button = UITextButton(arrow_down_text,(iw2,ih2),self.selected_button_pressed)
        
        self.selected_text = UIText(self.main_image.rect.center,None,example_text.font,self.selected_option,example_text.color,example_text.antialiasing)
        iw,ih = (width-self.selected_text.rect.w)/2,(height-self.selected_text.rect.h)/2
        self.selected_button = UITextButton(self.selected_text,(iw,ih),self.selected_button_pressed)
        
        self.options_buttons = []
        tmpsurf = pygame.Surface((width,option_height))
        for i,option in enumerate(self.options):
            
            if self.direction == DropDownDirections.down:
                temp_image = UIImage(tmpsurf,(topleft_pos[0],self.main_image.rect.bottom+i*option_height))
            else:
                temp_image = UIImage(tmpsurf,(topleft_pos[0],self.main_image.rect.top-i*option_height-option_height))
            pos = temp_image.rect.center
            del temp_image
            text = UIText(pos,None,example_text.font,option,example_text.color,example_text.antialiasing)
            iw,ih = (width-text.rect.w)/2,(height-text.rect.h)/2
            button = UITextButton(text,(iw,ih),self.option_button_pressed)
            self.options_buttons.append(button)
        
        if self.direction == DropDownDirections.up:
            i2 = pygame.Surface((width,self.main_image.rect.top-self.options_buttons[-1].hitbox.top))
            i2.fill(bg_color)
            self.options_bg_image = UIImage(i2,(topleft_pos[0],self.main_image.rect.top-i2.get_height()),outlines_color)
        else:
            i2 = pygame.Surface((width,self.options_buttons[-1].hitbox.bottom-self.main_image.rect.bottom))
            i2.fill(bg_color)
            self.options_bg_image = UIImage(i2,(topleft_pos[0],self.main_image.rect.bottom),outlines_color)
        
        self.visible = True
        self.options_visible = False
        
    def draw(self,surface):
        if self.visible:
            self.main_image.draw(surface)
            self.arrow_down_image.draw(surface)
            self.selected_button.draw(surface)
            self.arrow_down_button.draw(surface)
            if self.options_visible:
                self.options_bg_image.draw(surface)
                for b in self.options_buttons:
                    b.draw(surface)
    
    def update(self):
        if self.visible:
            self.selected_button.update()
            self.arrow_down_button.update()
            if self.options_visible:
                for b in self.options_buttons:
                    b.update()
        
    def selected_button_pressed(self):
        self.options_visible = not self.options_visible
    
    def option_button_pressed(self):
        pos = pygame.mouse.get_pos()
        for b in self.options_buttons:
            if b.hitbox.collidepoint(pos):
                self.selected_option = b.text.text
                self.selected_text.text = self.selected_option
                self.options_visible = False
                if self.on_change:
                    self.on_change()
                
    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
        
    def show_options(self):
        self.options_visible = True
        
    def hide_options(self):
        self.options_visible = False
        
    def _ui_group_on_pos_change(self, group_pos):
        self.main_image._ui_group_on_pos_change(group_pos)
        self.selected_button._ui_group_on_pos_change(group_pos)
        self.options_bg_image._ui_group_on_pos_change(group_pos)
        self.arrow_down_image._ui_group_on_pos_change(group_pos)
        self.arrow_down_button._ui_group_on_pos_change(group_pos)
        for b in self.options_buttons:
            b._ui_group_on_pos_change(group_pos)

    def _ui_group_set_offset(self):
        self.main_image._ui_group_set_offset()
        self.selected_button._ui_group_set_offset()
        self.arrow_down_image._ui_group_set_offset()
        self.arrow_down_button._ui_group_set_offset()
        for b in self.options_buttons:
            b._ui_group_set_offset()
        self.options_bg_image._ui_group_set_offset()