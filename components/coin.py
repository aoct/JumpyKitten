from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.core.window import Window

from random import uniform
from math import log

class Coin(Widget):
    def __init__(self, score, min_y=None, **kwargs):
        super(Coin, self).__init__(**kwargs)

        self.type = 'ground steady'

        self.width = 0.05*Window.size[0]
        self.height = self.width

        if min_y is None:
            min_y = 0.1*Window.size[1]
        self.y = uniform(min_y, 0.7*Window.size[1])

        self.base_velocity = Vector(-Window.size[0]/200., 0)
        self.velocity = self.base_velocity * (1 + 0.05*log(1+30*score)/10)

    def update(self, score):
        self.velocity = self.base_velocity * (1 + 0.05*log(1+30*score)/10)
        self.pos[0] = self.velocity[0]  + self.pos[0]

Builder.load_string("""
<Coin>:
    Image:
        source: "images/COIN_HD.png"
        center_x: root.center_x
        y: root.y
        size: root.width, root.height
""")
