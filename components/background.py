from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.vector import Vector

from kivy.core.window import Window

from math import log

class Background(Widget):
    image_1 = ObjectProperty(Image())
    image_2 = ObjectProperty(Image())
    image_3 = ObjectProperty(Image())

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.base_velocity = Vector(-Window.size[0]/200., 0)

    def remove_clouds(self):
        self.image_1.source = 'images/background/blueSky_fence_greenGrass.png'
        self.image_2.source = 'images/background/blueSky_fence_greenGrass.png'
        self.image_3.source = 'images/background/blueSky_fence_greenGrass.png'

    def update(self, score):
        self.velocity = self.base_velocity * (1 + 0.07*log(1+30*score)/10)

        self.image_1.pos[0] = self.velocity[0] + self.image_1.pos[0]
        self.image_2.pos[0] = self.velocity[0] + self.image_2.pos[0]
        self.image_3.pos[0] = self.velocity[0] + self.image_3.pos[0]

        if self.image_1.right <= 0:
            self.image_1.pos = (self.image_3.right, 0)
        elif self.image_2.right <= 0:
            self.image_2.pos = (self.image_1.right, 0)
        elif self.image_3.right <= 0:
            self.image_3.pos = (self.image_2.right, 0)



    def update_position(self):
        self.image_1.pos = (0, 0)
        self.image_2.pos = (self.image_1.right, 0)
        self.image_3.pos = (self.image_2.right, 0)

Builder.load_string("""
<Background>:
    image_1: image_1
    image_2: image_2
    image_3: image_3
    Image:
        id: image_1
        allow_stretch: True
        source: "images/background/blueSky_fence_greenGrass_whiteClouds.png"
        size: root.height * self.image_ratio, root.height
    Image:
        id: image_2
        allow_stretch: True
        source: "images/background/blueSky_fence_greenGrass_whiteMoreClouds.png"
        size: root.height * self.image_ratio, root.height
    Image:
        id: image_3
        allow_stretch: True
        source: "images/background/blueSky_fence_greenGrass_whiteMoreClouds.png"
        size: root.height * self.image_ratio, root.height
""")
