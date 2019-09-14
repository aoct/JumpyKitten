from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.core.window import Window

from random import uniform
from math import log

class Rock(Widget):
    obstacle_base =  NumericProperty(Window.size[1]*0.15)

    def __init__(self, score, **kwargs):
        super(Rock, self).__init__(**kwargs)

        self.type = 'rock'

        self.width = (1+0.01*log(score+1))*uniform(0.85, 1.15)*Window.size[0]*0.15
        self.height = (1+0.01*log(score+1))*uniform(0.85, 1.15)*Window.size[1]/6.

        self.base_velocity = Vector(-Window.size[0]/120., 0)
        self.velocity = self.base_velocity * (1 + 0.05*score/10)

        self.marked = False

    def update(self):
        self.pos[0] += self.velocity[0]

Builder.load_string("""
<Rock>:
    # canvas:
    #     Color:
    #         rgb: 221 / 255.0, 40 / 255.0, 40 / 255.0
    #     Rectangle:
    #         pos: self.x, root.obstacle_base
    #         size: root.width, root.height
    Image:
        source: "images/obstacle.png"
        center_x: root.center_x
        y: root.obstacle_base*0.9 - 30
        size: root.width, root.height
""")
