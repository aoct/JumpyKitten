from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.image import Image

class Background(Widget):
    image_one = ObjectProperty(Image())
    image_two = ObjectProperty(Image())

    velocity_x = NumericProperty(0)
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
