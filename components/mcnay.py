from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.image import Image

from kivy.config import Config
from kivy.clock import Clock

from kivy.lang import Builder

class Mcnay(Widget):
    mcnay_image = ObjectProperty(Image())

    jump_time = NumericProperty(0.5)
    jump_height = NumericProperty(120)

    time_jumped = NumericProperty(0)

    jumping = BooleanProperty(False)

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    normal_velocity_x = NumericProperty(0)
    normal_velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    normal_velocity = ReferenceListProperty(normal_velocity_x, normal_velocity_y)

    def __init__(self, **kwargs):
        super(Mcnay, self).__init__(**kwargs)
        self.pos = [0,0]
        if Config.getdefault('input', 'keyboard', False):
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self, 'text')
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def reset(self):
        self.normal_velocity = [0, -4]
        self.velocity = self.normal_velocity

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def switch_to_normal(self, dt):
        Clock.schedule_once(self.stop_jumping, self.jump_time  * (4.0 / 5.0))

    def stop_jumping(self, dt):
        self.jumping = False
        self.velocity_y = self.normal_velocity_y

    def on_touch_down(self, touch):
        if self.pos[1] == 104:
            self.jumping = True
            self.velocity_y = self.jump_height / (self.jump_time * 60.0)
            Clock.unschedule(self.stop_jumping)
            Clock.schedule_once(self.switch_to_normal, self.jump_time  / 5.0)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.on_touch_down(None)

    def update(self):
        self.pos = Vector(*self.velocity) + self.pos
        if self.pos[1] <= 104:
            Clock.unschedule(self.stop_jumping)
            self.pos = (self.pos[0], 104)


Builder.load_string("""
<Mcnay>:
    mcnay_image: image
    size: 60, 60
    Image:
        id: image
        source: "images/pixel_gray_base.png"
        size: root.size
        pos: root.pos
""")
