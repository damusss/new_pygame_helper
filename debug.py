import pygame

        
class _Debug:
    def __init__(self,activated,font_size,screen):
        self.activated = activated
        self.font = pygame.font.Font(None, font_size)
        self.items_log = []
        self.screen = screen
        
    def change_screen(self,surface):
        self.screen = surface
        
    def clear(self):
        self.items_log.clear()
        
    def log(self,*debug_items):
        if self.activated:
            for i in debug_items:
                self.items_log.append(i)
        else:
            raise Exception(
                "Debug mode is not activated. Enable this option from the init method.") 
            
    def console(self):
        if self.activated:
            string = "[debug]: "
            for item in self.items_log:
                string += str(item) + ", "
            print(string)
        else:
            raise Exception(
                "Debug mode is not activated. Enable this option from the init method.") 
            
    def draw(self,surface_to_debug_on: pygame.Surface = None, x: int = 20, y: int = 20):
        if self.activated:
            string = "[debug]: "
            for item in self.items_log:
                string += str(item) + ", "
            if not surface_to_debug_on:
                surface_to_debug_on = self.screen
            surface_to_debug_on.blit(self.font.render(
                    string, True, "white", "black"), (x, y))
        else:
            raise Exception(
                "Debug mode is not activated. Enable this option from the init method.")
        
    def quick_debug(self,*debug_items, to_console: bool = False, surface_to_debug_on: pygame.Surface = None, x: int = 20, y: int = 20) -> None:
        """
        Debug to the screen or console whatever you pass to it.
        """
        if self.activated:
            string = "[debug]: "
            for item in debug_items:
                string += str(item) + ", "
            if to_console:
                print(string)
            else:
                if not surface_to_debug_on:
                    surface_to_debug_on = self.screen
                surface_to_debug_on.blit(self.font.render(
                    string, True, "white", "black"), (x, y))
        else:
            raise Exception(
                "Debug mode is not activated. Enable this option from the init method.") 