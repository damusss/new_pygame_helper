import pygame

class ClickComponent:
    def __init__(self, sprite, on_click_func, click_button=0, allow_hold=False):
        self.sprite = sprite
        self.on_click = on_click_func
        self.multi_clicks = allow_hold
        self.button = click_button
        self.clicked = False

    def update(self) -> bool:
        """
        Check if the sprite is got clicked or is being clicked. If the click happens the callback will be called.
        """
        action = False

        pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        if self.sprite.hitbox.collidepoint(pos):
            if mouse[self.button]:
                if self.clicked == False or self.multi_clicks == True:
                    action = True
                    self.clicked = True
                    self.on_click()

            if not mouse[self.button]:
                self.clicked = False

        return action
    
    def copy(self):
        return ClickComponent(self.sprite,self.on_click,self.button,self.multi_clicks)

class DragComponent:
    def __init__(self, sprite,on_drag_func=None,drag_button=0):
        self.sprite = sprite
        self.was_pressing = False
        self.drag_rel_pos = pygame.Vector2()
        self.button = drag_button
        self.on_drag = on_drag_func

    def update(self):
        mouse = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if mouse[self.button]:
            if self.sprite.hitbox.collidepoint(pos[0], pos[1]) or self.was_pressing:
                if not self.was_pressing:
                    self.was_pressing = True
                    self.drag_rel_pos.xy = (
                        pos[0]-self.sprite.position.x, pos[1]-self.sprite.position.y)
                else:
                    self.sprite.position.xy = (
                        pos[0]-self.drag_rel_pos.x, pos[1]-self.drag_rel_pos[1])
                    self.sprite.update_positions()
                    if self.on_drag:
                        self.on_drag()
            else:
                self.was_pressing = False
        if not mouse[self.button]:
            self.was_pressing = False
            
    def copy(self):
        return DragComponent(self.sprite,self.on_drag,self.button)
