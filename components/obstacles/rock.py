from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.core.window import Window

from random import uniform
from math import log

class Rock(Widget):
    # obstacle_base =  NumericProperty(Window.size[1]*0.10)

    def __init__(self, score, **kwargs):
        super(Rock, self).__init__(**kwargs)

        self.type = 'ground steady'

        scale = uniform(0.7, 1.7)*(1+0.01*log(score+1))
        self.size_hint_x = scale*0.1
        self.size_hint_y = scale*0.15

        self.y = Window.size[1]*0.05

        self.base_velocity = Vector(-Window.size[0]/200., 0)
        self.velocity = self.base_velocity * (1 + 0.05*log(1+30*score)/10)

        self.marked = False

    def update(self, score):
        self.velocity = self.base_velocity * (1 + 0.05*log(1+30*score)/10)
        self.pos[0] = self.velocity[0]  + self.pos[0]

Builder.load_string("""
<Rock>:
    Image:
        source: "images/obstacles/rockOnGrass_debug.png"
        center_x: root.center_x
        y: root.y
        size: root.size
    Image:
        source: "images/obstacles/rockOnGrass.png"
        center_x: root.center_x
        y: root.y
        size: root.size
        allow_stretch: True
        keep_ratio: False
""")
