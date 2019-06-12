from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.lang import Builder

class Obstacle(Widget):
    gap_top = NumericProperty(0)
    gap_size = NumericProperty(150)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    marked = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)

    def update_position(self):
        self.gap_top = 300   #randint(self.gap_size + 112, self.height)

    def update(self):
        self.pos = Vector(*self.velocity) + self.pos

Builder.load_string("""
<Obstacle>:
    width: 30
    canvas:
        Color:
            rgb: 21 / 255.0, 180 / 255.0, 39 / 255.0
        # Rectangle:
        #     pos: self.x, self.gap_top + 20
        #     size: self.width, self.height - self.gap_top
        Rectangle:
            pos: self.x, 112
            size: self.width, self.gap_top - self.gap_size - 112
    # Image:
    #     source: "images/pipe_bottom.png"
    #     center_x: root.center_x
    #     y: root.gap_top - 20
    # Image:
    #     source: "images/pipe_top.png"
    #     center_x: root.center_x
    #     y: root.gap_top - root.gap_size - 40
""")
