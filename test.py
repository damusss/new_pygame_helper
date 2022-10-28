import helper

s,c = helper.init((1200,800),debug_activated=True)

bg = helper.Background(helper.load_image("C:\work\images\purplebg.png"),(1200,800),s)

title = helper.UIText(None,(3,3),helper.SysFont("Segoe UI",15),"Window Title","white")
window = helper.UIWindow((100,100),800,500,title)

def onclick():
    window.show()
    
def ontoggle():
    helper.debug.log("toggled")
    
def onchange():
    helper.debug.log(slider.value)

toggle = helper.UIImageButton(helper.empty_image((30,30),"grey"),(20,800-20),on_click_func=onclick)

check = helper.UICheckBox((50,window.offset_height(50)),30,helper.empty_image((20,20),"gray"),ontoggle)

slider = helper.UISlider((50,150),300,20,-50,20,helper.empty_image((20,20),"gray"),"h",onchange)

window.add(check,slider)

while True:
    helper.debug.clear()
    helper.global_input.update()
    
    for e in helper.get_events():
        helper.quit_event(e)
        
    bg.draw()
    
    toggle.draw(s)
    toggle.update()
    window.draw(s)
    window.update()
    
    helper.debug.log(round(c.get_fps()))
    helper.debug.draw()
    
    helper.update_window(c,60,s)