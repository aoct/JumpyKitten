import kivy
kivy.require("1.8.0")

from random import randint
import sys

from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from components.background import Background
from components.mcnay import Mcnay
from components.obstacles import Obstacle


class endGamePopup(Popup):
    pass
    # self.layout = FloatLayout(size=(300, 300))
    #
    # startButton = Button(text='Start', size_hint=(.6, .6), pos_hint={'x':.2, 'y':.2})
    # startButton.bind(on_release=self.startButton_func)
    # self.layout.add_widget(startButton)

class JumpyKittenGame(Widget):
    mcnay = ObjectProperty(Mcnay())
    background = ObjectProperty(Background())
    obstacles = ListProperty([])
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(JumpyKittenGame, self).__init__(**kwargs)
        self.reset()
        self.bind(size=self.size_callback)

    def start(self):
        self.process = Clock.schedule_interval(self.update, 1.0/60.0)

    def reset(self):
        self.mcnay.normal_velocity = [0, -4]
        self.mcnay.velocity = self.mcnay.normal_velocity
        self.background.velocity = [-2, 0]
        for obstacle in self.obstacles:
            self.remove_obstacle()

    def remove_obstacle(self):
        self.remove_widget(self.obstacles[0])
        self.obstacles = self.obstacles[1:]

    def new_obstacle(self, remove=True):
        if remove:
            self.remove_obstacle()
        new_obstacle = Obstacle()
        new_obstacle.height = self.height
        new_obstacle.x = self.width
        new_obstacle.update_position()
        new_obstacle.velocity = [-3, 0]
        self.add_widget(new_obstacle)
        self.obstacles = self.obstacles + [new_obstacle]

    def size_callback(self, instance, value):
        for obstacle in self.obstacles:
            obstacle.height = value[1]
            obstacle.update_position()
        self.background.size = value
        self.background.update_position()

    def update(self, dt):
        self.mcnay.update()
        self.background.update()
        # Loop through and update obstacles. Replace obstacles which went off the screen.
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.x < self.mcnay.x and not obstacle.marked:
                obstacle.marked = True
                self.score += 1
                self.new_obstacle(remove=False)
        if len(self.obstacles) == 0:
            self.new_obstacle(remove=False)
        elif self.obstacles[0].x < 0:
            self.remove_obstacle()
        # If obstacles is emply
        # See if the player collides with any obstacles
        for obstacle in self.obstacles:
            # if self.mcnay.collide_widget(Widget(pos=(obstacle.x, obstacle.gap_top + 20), size=(obstacle.width, obstacle.height - obstacle.gap_top))):
            #     # This will be replaced later on
            #     sys.exit()
            if self.mcnay.collide_widget(Widget(pos=(obstacle.x, 0), size=(obstacle.width, obstacle.gap_top - obstacle.gap_size))):

                self.mcnay.velocity = [0, 0]
                self.mcnay.normal_velocity = [0,0]
                self.background.velocity = [0,0]
                self.obstacles.velocity = [0,0]

                self.process.cancel()
                popup = endGamePopup()
                popup.open()

class JumpyKittenPage(Screen):
    def __init__(self, **kwargs):
        super(JumpyKittenPage, self).__init__(**kwargs)
        self.game = JumpyKittenGame()
        self.add_widget(self.game)

    def on_enter(self):
        self.game.start()

    def on_leave(self):
        self.game.reset()
