from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.image import Image
from kivy.lang import Builder


class Background(Widget):
    image_one = ObjectProperty(Image())
    image_two = ObjectProperty(Image())

    velocity_x = NumericProperty(-2)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def update(self):
        self.image_one.pos = Vector(*self.velocity) + self.image_one.pos
        self.image_two.pos = Vector(*self.velocity) + self.image_two.pos

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
        source: "images/background.png"
        pos: 0, 0
        size: 800, 600
    Image:
        id: image_two
        source: "images/background.png"
        pos: root.width, 0
        size: 800, 600
""")
