from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.core.window import Window

from random import uniform

class Obstacle(Widget):
    base =  NumericProperty(Window.size[1]/5.35)

    def __init__(self, score, **kwargs):
        super(Obstacle, self).__init__(**kwargs)

        self.width = uniform(0.8, 1.2)*Window.size[0]*0.05
        self.height = uniform(0.8, 1.2)*Window.size[1]/6.

        self.base_velocity = Vector(-Window.size[0]/250., 0)
        self.velocity = self.base_velocity * (1 + 0.05*score/10)

        self.marked = False

    def update(self):
        self.pos[0] += self.velocity[0]

Builder.load_string("""
<Obstacle>:
    canvas:
        Color:
            rgb: 21 / 255.0, 180 / 255.0, 39 / 255.0
        Rectangle:
            pos: self.x, root.base
            size: root.width, root.height
    # Image:
    #     source: "images/pipe_bottom.png"
    #     center_x: root.center_x
    #     y: root.gap_top - 20
""")
