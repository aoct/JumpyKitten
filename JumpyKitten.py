import kivy
kivy.require("1.8.0")

from random import randint
import sys
import pickle, os
import numpy as np
from math import log

from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.utils import platform

from commercial.kivmob import KivMob, TestIds

from components.background import Background
from components.mcnay import Mcnay
from components.obstacles import Obstacle

from random import uniform

from os.path import join


class endGamePopup(Popup):
    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)


class JumpyKittenGame(Widget):
    background = ObjectProperty(Background())
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(JumpyKittenGame, self).__init__(**kwargs)

        self.g_grav = -0.5 #pizel * frame_rate^2
        self.obstacles = []
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
            self.remove_obstacle(obstacle)

    def remove_obstacle(self, ob):
        self.remove_widget(ob)
        self.obstacles.remove(ob)

    def new_obstacle(self):
        new_obstacle = Obstacle(self.score)
        new_obstacle.x = self.width

        self.add_widget(new_obstacle)
        self.obstacles = self.obstacles + [new_obstacle]

    def size_callback(self, instance, value):
        self.background.size = value
        self.background.update_position()

    def update(self, dt):
        self.mcnay.update(self.g_grav)
        self.background.update()
        # Loop through and update obstacles. Replace obstacles which went off the screen.
        for o in self.obstacles:
            o.update()
            if o.x + o.width < 0:
                self.remove_obstacle(o)

        furtherst_obstacle = np.max(list(map(lambda x: x.x, self.obstacles)))
        if len(self.obstacles) == 0:
            self.new_obstacle()
        elif furtherst_obstacle < Window.size[0]*0.7:
            if uniform(0, 1 + log(1. + self.score*1e-5)) > 0.995:
                self.new_obstacle()

        # See if the player collides with any obstacles
        for obstacle in self.obstacles:
            # if self.mcnay.collide_widget(Widget(pos=(obstacle.x+0.05*obstacle.width, obstacle.obstacle_base), size=(obstacle.width*0.9, obstacle.height*0.80))): #Old collision Function, was a kivy built in widget function
            if self.mcnay.collision_with_obstacle(obstacle.width, obstacle.height, obstacle.pos[0], obstacle.pos[1]):
                self.process.cancel()
                
                #This was the old code that worked also on android, it does not work for iOS case on iOS there is a specific folder where you have to save data for a game.
                #Check whether the current version also works for android.
                if platform == 'ios':
                    user_data_dir = App.get_running_app().user_data_dir
                    filename = join(user_data_dir, "score_history.pickle")
                else:
                    user_data_dir = 'data'
                    filename = 'data/score_history.pickle'

                try:
                    if os.path.isfile(filename) :
                        score_history = pickle.load(open(filename, 'rb'))
                    else:
                        score_history = []
                        if not os.path.isdir(user_data_dir):
                            os.mkdir(user_data_dir)

                    score_history += [self.score]
                    pickle.dump(score_history, open(filename, 'wb'))
                except:
                    Logger.exception("Problem saving file")

                popup = endGamePopup(auto_dismiss=False)
                popup.open()

        self.score += 0.02

class JumpyKittenPage(Screen):
    def __init__(self, **kwargs):
        super(JumpyKittenPage, self).__init__(**kwargs)
        self.game = JumpyKittenGame()
        self.add_widget(self.game)

        if platform != 'ios':
            # self.ads = KivMob(TestIds.APP)
            self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
            # self.ads.new_banner(TestIds.BANNER)
            self.ads.new_banner('ca-app-pub-8564280870740386/2464625123')


    def on_enter(self):
        self.game.reset()

        if platform != 'ios':
            self.ads.request_banner()
            self.ads.show_banner()
        self.game.start()

    def on_leave(self):
        if platform != 'ios':
            self.ads.hide_banner()
            self.ads.destroy_banner()
        self.game.reset()
