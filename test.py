from pygame_helper import helper

s,c = helper.init((1920,1000),debug_activated=True)

bg = helper.Background(helper.load_image("C:\work\images\purplebg.png"),(1920,1080),s)

group = helper.Group()

ss = helper.Sprite(helper.empty_image((50,400),"blue"),(400,100),group)
ss.setup_attributes((-1,0),(1,1))
ss.set_labels("wall","walls")

class TestInherit(helper.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = helper.empty_image((100,200),"red")
        self.rect = self.image.get_rect(topleft=(200,300))
        
        self.set_original_image()
        self.set_hitbox()
        self.refresh_position()
        self.setup_attributes((1,0),(2,1))
        self.set_labels("main sprite","normal sprite")
        
    def on_collision_enter(self, sprite, direction):
        print(sprite,direction)
        
    def update(self):
        self.normalize_direction()
        self.collisions_and_positions(group)

sprite = TestInherit()

while True:
    helper.debug.clear()
    helper.global_input.update()
    
    for e in helper.get_events():
        helper.quit_event(e)
        
    bg.draw()
    
    group.draw(s)
    
    sprite.draw(s)
    sprite.update()
    
    helper.debug.log(round(c.get_fps()))
    helper.debug.draw()
    
    helper.update_window(c,60,s)