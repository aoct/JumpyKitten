from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.lang import Builder

class Obstacle(Widget):
    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)

        self.velocity = Vector(-3, 0)
        self.marked = False

    def update(self):
        self.pos[0] += self.velocity[0]

Builder.load_string("""
<Obstacle>:
    width: 30
    height: 100
    canvas:
        Color:
            rgb: 21 / 255.0, 180 / 255.0, 39 / 255.0

        Rectangle:
            pos: self.x, 112
            size: self.width, self.height
    # Image:
    #     source: "images/pipe_bottom.png"
    #     center_x: root.center_x
    #     y: root.gap_top - 20
""")
