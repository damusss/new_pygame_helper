import pygame
from .text import UIText


class UIStatusBar():
    def __init__(self, topleft_pos, width, height, max_value, start_value, sprite_to_follow=None, offset_from_sprite=(0, 0), bg_color="black", fill_color="red", outline_color=None, outline_size=2, label: UIText = None, label_offset_from_topleft=(0, 0), border_radius=-1):
        self.width = width
        self.height = height
        self.max_value = max_value
        self.start_value = start_value
        self.current_value = self.start_value
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_size = outline_size
        self.sprite_following = sprite_to_follow
        self.offset_from_sprite = offset_from_sprite
        self.border_radius = border_radius
        self.label = label
        if self.label:
            self.label_offset = label_offset_from_topleft
            self.label.stick_topleft = True
            self.label.rect.topleft = (
                topleft_pos[0]+self.label_offset[0], topleft_pos[1]+self.label_offset[1])

        self.bg_rect = pygame.Rect(topleft_pos, (width, height))
        self.fill_rect = pygame.Rect(topleft_pos, (width, height))
        self.apply_bar_changes()
        if self.sprite_following:
            self.follow_sprite()

        self.ui_group_offset = pygame.Vector2()

        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self):
        pass

    def apply_bar_changes(self):
        self.bg_rect.w = self.width
        self.bg_rect.h = self.height
        self.fill_rect.height = self.height
        self.update_current_value(self.current_value)
        self.create_outline_rect()

    def create_outline_rect(self):
        self.outline_rect = self.bg_rect.inflate(
            self.outline_size, self.outline_size)

    def update_current_value(self, new_value):
        self.current_value = new_value
        self.fill_rect.width = self.current_value/(self.max_value/self.width)

    def get_value_percentage(self):
        return (100*self.current_value)/(self.max_value)

    def get_value_ratio(self, max_value):
        return (max_value*self.current_value)/(self.max_value)

    def follow_sprite(self):
        self.bg_rect.center = (self.sprite_following.rect.centerx +
                               self.offset_from_sprite[0], self.sprite_following.rect.centery+self.offset_from_sprite[1])
        self.fill_rect.topleft = self.bg_rect.topleft
        self.outline_rect.topleft = (
            self.bg_rect.topleft[0]-self.outline_size, self.bg_rect.topleft[1]-self.outline_size)
        if self.label:
            self.label.rect.topleft = (
                self.bg_rect.topleft[0]+self.label_offset[0], self.bg_rect.topleft[1]+self.label_offset[1])

    def change_pos(self, topleft_pos, _internal=False):
        self.bg_rect.topleft = topleft_pos
        self.fill_rect.topleft = topleft_pos
        self.outline_rect.topleft = (
            self.bg_rect.topleft[0]-self.outline_size, self.bg_rect.topleft[1]-self.outline_size)
        if self.label:
            self.label.rect.topleft = (
                self.bg_rect.topleft[0]+self.label_offset[0], self.bg_rect.topleft[1]+self.label_offset[1])
        if not _internal:
            self.ui_group_offset.xy = self.bg_rect.topleft

    def update_label_text(self, mode="current_over_max", custom_text="", available_modes_are="current_over_max,current,percentage", float_rounding=1):
        if custom_text:
            self.label.text = custom_text
            return
        if mode == "current_over_max":
            self.label.text = str(round(self.current_value, float_rounding)) + \
                "/"+str(round(self.max_value, float_rounding))
        elif mode == "current":
            self.label.text = str(round(self.current_value, float_rounding))
        elif mode == "percentage":
            self.label.text = str(
                round(self.get_value_percentage(), float_rounding))+"%"

    def _ui_group_on_pos_change(self, group_pos):
        self.change_pos((group_pos+self.ui_group_offset).xy, True)

    def _ui_group_set_offset(self):
        self.ui_group_offset.xy = self.bg_rect.topleft

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.bg_color, self.bg_rect,
                             border_radius=self.border_radius)
            pygame.draw.rect(surface, self.fill_color,
                             self.fill_rect, border_radius=self.border_radius)
            if self.outline_color:
                pygame.draw.rect(surface, self.outline_color, self.outline_rect,
                                 self.outline_size, border_radius=self.border_radius)
            if self.label:
                self.label.draw(surface)
