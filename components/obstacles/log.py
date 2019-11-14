from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.core.window import Window

from random import randint

from random import uniform
from math import log

class Log(Widget):
    obstacle_base =  NumericProperty(Window.size[1]*0.10)

    def __init__(self, score, **kwargs):
        super(Log, self).__init__(**kwargs)

        self.type = 'ground steady'
        image_num = randint(1,3)
        self.image_num = image_num

        if image_num == 1:
            scale = [0.9, 1]
        elif image_num == 2:
            scale = [0.8, 1.4]
        else:
            scale = [0.7, 1.8]
        self.size_hint_x = (1+0.02*log(score+1))*0.15*scale[0]*uniform(0.8, 1.2)
        self.size_hint_y = (1+0.02*log(score+1))*0.16*scale[1]*uniform(0.8, 1.2)

        self.y = Window.size[1]*0.05

        self.base_velocity = Vector(-Window.size[0]/200., 0)
        self.velocity = self.base_velocity * (1 + 0.07*log(1+30*score)/10)

        self.marked = False
        self.log_image.source = 'images/obstacles/logOnGrass_{}.png'.format(image_num)

    def update(self, score):
        self.velocity = self.base_velocity * (1 + 0.05*log(1+30*score)/10)
        self.pos[0] = self.velocity[0] + self.pos[0]

Builder.load_string("""
<Log>:
    log_image: image
    # Image:
    #     size: root.size
    #     pos: root.pos
    #     source: "images/cats/CAT_FRAME_0_HD_debug.png"
    #     allow_stretch: True
    #     keep_ratio: False
    Image:
        id: image
        center_x: root.center_x
        y: root.y
        size: root.width, root.height
        allow_stretch: True
        keep_ratio: False
""")
