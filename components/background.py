from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder

from kivy.core.window import Window

class Background(Widget):
    image_1 = ObjectProperty(Image())
    image_2 = ObjectProperty(Image())
    image_3 = ObjectProperty(Image())

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.velocity = [-Window.size[0]/400., 0] #pxl*frame_rate

    def update(self):
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
        source: "images/background_4.png"
        size: root.height * self.image_ratio, root.height
    Image:
        id: image_2
        allow_stretch: True
        source: "images/background_4.png"
        size: root.height * self.image_ratio, root.height
    Image:
        id: image_3
        allow_stretch: True
        source: "images/background_4.png"
        size: root.height * self.image_ratio, root.height
""")
