import kivy
kivy.require("1.8.0")

from random import randint
import sys
import pickle, os

from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from components.background import Background
from components.mcnay import Mcnay
from components.obstacles import Obstacle

from random import uniform


class endGamePopup(Popup):
    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)


class JumpyKittenGame(Widget):
    background = ObjectProperty(Background())
    obstacles = ListProperty([])
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(JumpyKittenGame, self).__init__(**kwargs)

        self.g_grav = -0.6 #pizel * frame_rate^2

        self.mcnay = Mcnay()
        self.add_widget(self.mcnay)

        self.reset()
        self.bind(size=self.size_callback)

    def start(self):
        self.process = Clock.schedule_interval(self.update, 1.0/60.0)

    def reset(self):
        self.score = 0
        self.mcnay.reset()
        for obstacle in self.obstacles:
            self.remove_obstacle()

    def remove_obstacle(self):
        self.remove_widget(self.obstacles[0])
        self.obstacles = self.obstacles[1:]

    def new_obstacle(self):
        new_obstacle = Obstacle(self.score)
        new_obstacle.x = self.width

        self.add_widget(new_obstacle)
        self.obstacles = self.obstacles + [new_obstacle]

    def size_callback(self, instance, value):
        for obstacle in self.obstacles:
            obstacle.height = value[1]
            obstacle.update_position()
        self.background.size = value
        self.background.update_position()

    def update(self, dt):
        self.mcnay.update(self.g_grav)
        self.background.update()
        # Loop through and update obstacles. Replace obstacles which went off the screen.
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.x < self.mcnay.x and not obstacle.marked:
                obstacle.marked = True

        if len(self.obstacles) == 0:
            self.new_obstacle()
        elif self.obstacles[-1].x < Window.size[0]*0.7:
            if uniform(0, 1.) > 0.99:
                self.new_obstacle()

        if self.obstacles[0].x < 0:
            self.remove_obstacle()

        # See if the player collides with any obstacles
        for obstacle in self.obstacles:
            if self.mcnay.collide_widget(Widget(pos=(obstacle.x+0.05*obstacle.width, obstacle.base), size=(obstacle.width*0.9, obstacle.height))):
                self.process.cancel()

                if os.path.isfile('data/score_history.pickle'):
                    score_history = pickle.load(open('data/score_history.pickle', 'rb'))
                else:
                    score_history = []
                    if not os.path.isdir('data'):
                        os.mkdir('data')

                score_history += [self.score]
                pickle.dump(score_history, open('data/score_history.pickle', 'wb'))


                popup = endGamePopup()
                popup.open()

        self.score += 0.02

class JumpyKittenPage(Screen):
    def __init__(self, **kwargs):
        super(JumpyKittenPage, self).__init__(**kwargs)
        self.game = JumpyKittenGame()
        self.add_widget(self.game)

    def on_enter(self):
        self.game.start()

    def on_leave(self):
        self.game.reset()
