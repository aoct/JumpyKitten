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

        self.ground = Window.size[1]*0.05

        self.size = (Window.size[0]/7., Window.size[0]/7.)

        self.updatesSinceLastImageChange = 0
        self.imageFrame = 5

        self.doubleJump = 0

    def reset(self):
        self.pos = Vector(Window.size[0]/8, Window.size[1]/3)
        self.velocity = Vector(0, 0)

    def jump(self):
        self.imageFrame = 0
        self.mcnay_image.source = 'images/cats/basePinkCat_aoct/CAT_FRAME_0_HD.png'
        self.velocity[1] = self.impulse / self.mass

    def on_touch_down(self, touch):
        if self.pos[1] == self.ground:
            self.jump()

        if self.pos[1] != self.ground and self.doubleJump == 0:
            self.jump()
            self.doubleJump = 1

    def update(self, g_grav):
        self.pos[1] = self.pos[1] + (self.velocity[1] + 0.5*g_grav)*Window.size[1]/600.
        self.velocity[1] = self.velocity[1] + g_grav

        if self.pos[1] <= self.ground:
            self.pos[1] = self.ground
            self.velocity[1] = 0
            self.doubleJump = 0

        if self.updatesSinceLastImageChange > 4 and self.pos[1] <= self.ground:
            self.imageFrame += 1
            self.mcnay_image.source = 'images/cats/basePinkCat_aoct/CAT_FRAME_{}_HD.png'.format(self.imageFrame%4)
            self.updatesSinceLastImageChange = 0
        else:
            self.updatesSinceLastImageChange += 1

        if self.velocity[1] != 0:
            self.updatesSinceLastImageChange = 0

    def collision_with_obstacle(self, o):
        xCenterObstacle = o.pos[0] + o.width/2
        yCenterObstacle = o.pos[1] + o.height/2
        radiusObstacle = 0.45*o.width

        xCenterMcNay = self.pos[0] + self.size[0]/2
        yCenterMcNay = self.pos[1] + self.size[1]/2

        radiusMcnay = 0.4*self.width

        #The contact is based on circles centered at middle of the widgets
        if (xCenterObstacle - xCenterMcNay)**2 + (yCenterObstacle - yCenterMcNay)**2 <= (radiusObstacle + radiusMcnay)**2:
            return True
        else:
            return False

    def death(self):
        self.velocity[1] = 0.5* self.impulse / self.mass
        self.velocity[0] = -0.2*Window.size[0]/200.
        self.mcnay_image.source = 'images/cats/basePinkCat_aoct/CAT_FRAME_DEATH_HD.png'


Builder.load_string("""
<Mcnay>:
    mcnay_image: image
    Image:
        id: image
        source: 'images/cats/basePinkCat_aoct/CAT_FRAME_0_HD.png'
        size: root.size
        pos: root.pos
""")
