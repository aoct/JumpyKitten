from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivy.core.window import Window

from random import triangular
from math import log
from kivy.properties import ObjectProperty
from kivy.uix.image import Image


class Bird(Widget):
    obstacle_base =  NumericProperty(Window.size[1]*0.15)
    image = ObjectProperty(Image())

    def __init__(self, score, **kwargs):
        super(Bird, self).__init__(**kwargs)

        self.type = 'bird'

        self.height = 0.12*Window.size[1]
        self.width = self.height

        self.base_velocity = Vector(-1e-2*Window.size[0], 0)
        self.velocity = self.base_velocity * (1 + 0.05*score/10)

        self.y = triangular(0.15*Window.size[1], 0.7*Window.size[1], 0.45*Window.size[1])

        self.updatesSinceLastImageChange = 0
        self.imageFrame = 0

    def update(self):
        self.pos[0] += self.velocity[0]

        if self.updatesSinceLastImageChange > 8:
            self.imageFrame += 1
            self.image.source = 'images/obstacles/pinkBird/pixil-frame-{}_HD.png'.format(self.imageFrame%2)
            self.updatesSinceLastImageChange = 0
        else:
            self.updatesSinceLastImageChange += 1

Builder.load_string("""
<Bird>:
    image: image_
    Image:
        id: image_
        source: "images/obstacles/pinkBird/pixil-frame-0_HD.png"
        center_x: root.center_x
        y: root.y
        size: root.width, root.height
""")
