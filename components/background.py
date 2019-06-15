from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder


class Background(Widget):
    image_one = ObjectProperty(Image())
    image_two = ObjectProperty(Image())

    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.velocity = [-2, 0] #pxl*frame_rate

    def update(self):
        self.image_one.pos[0] = self.velocity[0] + self.image_one.pos[0]
        self.image_two.pos[0] = self.velocity[0] + self.image_two.pos[0]

        if self.image_one.right <= 0:
            self.image_one.pos = (self.width, 0)
        if self.image_two.right <= 0:
            self.image_two.pos = (self.width, 0)

    def update_position(self):
        self.image_one.pos = (0, 0)
        self.image_two.pos = (self.width, 0)

Builder.load_string("""
<Background>:
    image_one: image_one
    image_two: image_two
    Image:
        id: image_one
        allow_stretch: True
        source: "images/background.png"
        pos: 0, 0
        size: root.height * self.image_ratio, root.height
    Image:
        id: image_two
        allow_stretch: True
        source: "images/background.png"
        pos: root.width, 0
        size: root.height * self.image_ratio, root.height
""")
