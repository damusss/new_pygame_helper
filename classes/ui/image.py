import pygame


class UIImage():
    def __init__(self, surface, topleft_pos, outline_color=None, outline_size=2):
        self.image = surface
        self.rect: pygame.Rect = self.image.get_rect(topleft=topleft_pos)

        self.outline_color = outline_color
        self.outline_size = outline_size
        self.outline_rect = self.rect.inflate(
            self.outline_size, self.outline_size)
        self.outline_rect.topleft = (
            self.rect.topleft[0]-self.outline_size, self.rect.topleft[1]-self.outline_size)

        self.ui_group_offset = pygame.Vector2()
        
        self.visible = True
        
    def show(self):
        self.visible = True
        
    def hide(self):
        self.visible = False
        
    def update(self):
        pass

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            if self.outline_color:
                pygame.draw.rect(surface, self.outline_color,
                                self.outline_rect, self.outline_size)

    def _ui_group_on_pos_change(self, group_pos):
        self.rect.topleft = (group_pos+self.ui_group_offset).xy
        self.outline_rect.topleft = (
            self.rect.topleft[0]-self.outline_size, self.rect.topleft[1]-self.outline_size)

    def _ui_group_set_offset(self):
        self.ui_group_offset.xy = self.rect.topleft
