from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.image import Image

from kivy.config import Config
from kivy.core.window import Window

from kivy.lang import Builder

class Mcnay(Widget):
    mcnay_image = ObjectProperty(Image())

    def __init__(self, **kwargs):
        super(Mcnay, self).__init__(**kwargs)

        self.impulse = 800 #pizel * frame_rate^2
        self.mass = 50
        self.velocity = Vector(0, 0)
        self.pos = Vector(Window.size[0]/8, Window.size[1]/3)

        self.ground = Window.size[1]/5.35 - 20

        self.size = (Window.size[0]/8., Window.size[0]/8.)

        self.updatesSinceLastImageChange = 0
        self.imageFrame = 5

    def reset(self):
        self.pos = Vector(Window.size[0]/8, Window.size[1]/3)
        self.velocity = Vector(0, 0)

    def jump(self):
        self.velocity[1] = self.impulse / self.mass

    def on_touch_down(self, touch):
        if self.pos[1] == self.ground:
            self.jump()

    def update(self, g_grav):
        self.pos[1] = self.pos[1] + (self.velocity[1] + 0.5*g_grav)*Window.size[1]/600.
        self.velocity[1] = self.velocity[1] + g_grav

        if self.pos[1] <= self.ground:
            self.pos[1] = self.ground
            self.velocity[1] = 0

        if self.updatesSinceLastImageChange > 4: #The gif I took it from had 0.07 frame rate and our app run at 1/60 --> ~ 4.2
            self.imageFrame += 1
            self.mcnay_image.source = 'images/cats/pink_nyan/frame_{}_delay-0.07s.png'.format(self.imageFrame%5)
            self.updatesSinceLastImageChange = 0
        else:
            self.updatesSinceLastImageChange += 1

Builder.load_string("""
<Mcnay>:
    mcnay_image: image
    Image:
        id: image
        source: "images/cats/pink_nyan/frame_5_delay-0.07s.png"
        size: root.size
        pos: root.pos
""")
