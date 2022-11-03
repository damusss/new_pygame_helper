from classes.ui.window_stack import UIWindowStack
import helper

s,c = helper.init((1920,1000),debug_activated=True)

bg = helper.Background(helper.load_image("C:\work\images\purplebg.png"),(1920,1080),s)

sprite = helper.Sprite(helper.empty_image((100,100),"green"),(200,100))
anim = sprite.add_transform_animation(False,True,helper.transform_animation_schedule_example)

anim.play()

while True:
    helper.debug.clear()
    helper.global_input.update()
    
    for e in helper.get_events():
        helper.quit_event(e)
        
    bg.draw()
    
    if helper.global_input.buttons[0]:
        anim.restart()
    
    sprite.draw(s)
    sprite.update_positions()
    sprite.update_transform_animation()
    
    helper.debug.log(round(c.get_fps()))
    helper.debug.draw()
    
    helper.update_window(c,60,s)