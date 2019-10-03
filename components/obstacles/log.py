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

        self.type = 'log'
        image_num = randint(1,3)

        self.width = (1+0.01*log(score+1))*uniform(0.85, 1.15)*Window.size[0]*0.15
        if image_num == 1:
            self.height = (1+0.01*log(score+1))*uniform(0.85, 1.15)*Window.size[1]/6.
        elif image_num == 2:
            self.height = (1+0.01*log(score+1))*uniform(1, 1.3)*Window.size[1]/6.
        else:
            self.height = (1+0.01*log(score+1))*uniform(1.3, 1.45)*Window.size[1]/6.
        
        self.base_velocity = Vector(-Window.size[0]/200., 0)
        self.velocity = self.base_velocity * (1 + 0.05*log(1+30*score)/10)

        self.marked = False
        self.log_image.source = 'images/obstacles/logOnGrass_{}.png'.format(image_num)

    def update(self):
        self.pos[0] += self.velocity[0]

Builder.load_string("""
<Log>:
    # canvas:
    #     Color:
    #         rgb: 221 / 255.0, 40 / 255.0, 40 / 255.0
    #     Rectangle:
    #         pos: self.x, root.obstacle_base
    #         size: root.width, root.height
    log_image: image
    Image:
        id: image
        center_x: root.center_x
        y: root.obstacle_base*0.9 - 30
        size: root.width, root.height
""")
