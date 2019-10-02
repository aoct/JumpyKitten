from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.core.window import Window

from random import uniform
from math import log

class Bird(Widget):
    obstacle_base =  NumericProperty(Window.size[1]*0.15)

    def __init__(self, score, **kwargs):
        super(Bird, self).__init__(**kwargs)

        self.type = 'bird'

        self.height = Window.size[1]/18.
        self.width = self.height

        self.base_velocity = Vector(-Window.size[0]/90., 0)
        self.velocity = self.base_velocity * (1 + 0.05*score/10)

        self.y = uniform(Window.size[1]-Window.size[1]*2/3, Window.size[1]- 100)

        self.marked = False

    def update(self):
        self.pos[0] += self.velocity[0]

Builder.load_string("""
<Bird>:
    Image:
        source: "images/obstacles/blueDot.png"
        center_x: root.center_x
        y: root.y
        size: root.width, root.height
""")
