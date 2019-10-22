import kivy
kivy.require("1.8.0")

from random import randint
import sys
import pickle, os
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
from components.obstacles.rock import Rock
from components.obstacles.bird import Bird
from components.obstacles.log import Log

from random import uniform

from os.path import join

import time


class endGamePopup(Popup):
    score = NumericProperty()
    def __init__(self, score, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.score = score

class JumpyKittenGame(Widget):
    background = ObjectProperty(Background())
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(JumpyKittenGame, self).__init__(**kwargs)

        self.g_grav = -0.5 #pizel * frame_rate^2
        self.obstacles = []
        self.mcnay = Mcnay()
        self.add_widget(self.mcnay)
        self.bind(size=self.size_callback) # for bkg sizing

        if platform == 'ios':
            print('requesting banner')
            from pyobjus import autoclass
            self.banner_ad = autoclass('adSwitchBanner').alloc().init()
            self.banner_ad.show_ads()
            self.interstitial_ad = autoclass('adSwitchInterstitial').alloc().init()
        if platform == 'android':
            self.ads = KivMob(TestIds.APP)
            self.ads.new_banner(TestIds.BANNER)
            self.ads.new_interstitial(TestIds.INTERSTITIAL)
            # self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
            # self.ads.new_banner('ca-app-pub-8564280870740386/2464625123')
            # slef.ads.new_interstial('ca-app-pub-8564280870740386/8985921895')

        self.reset()

    def start(self):
        if platform == 'android':
            print('Requesting banner')
            self.ads.request_banner()
            self.ads.request_interstitial()
            self.ads.show_banner()
        self.process = Clock.schedule_interval(self.update, 1.0/60.0)

    def reset(self):
        if hasattr(self, 'process'):
            self.process.cancel()
        self.score = 0
        self.mcnay.reset()
        for obstacle in self.obstacles:
            self.remove_widget(obstacle)
        self.obstacles = []

        if platform == 'android':
            self.ads.destroy_interstitial()

    def new_obstacle(self):
        if self.score > 30 and uniform(0, 1 + log(1. + self.score*1e-5)) > 0.7:
            new_obstacle = Bird(self.score)
        else:
            if uniform(0,1) > 0.8:
                new_obstacle = Rock(self.score)
            else:
                new_obstacle = Log(self.score)
        new_obstacle.x = self.width

        self.add_widget(new_obstacle)
        self.obstacles.append(new_obstacle)

    def size_callback(self, instance, value):
        self.background.size = value
        self.background.update_position()

    def update(self, dt):
        self.mcnay.update(self.g_grav)
        self.background.update(self.score)
        # Loop through and update obstacles. Replace obstacles which went off the screen.
        furtherst_obstacle = -999999.
        for o in self.obstacles:
            o.update()
            if o.type == 'ground steady' and o.x > furtherst_obstacle:
                furtherst_obstacle = o.x
            if o.x + o.width < 0:
                self.remove_widget(o)
                self.obstacles.remove(o)
            else:
                if self.mcnay.collision_with_obstacle(o):
                    self.obstacle_collision()

        if len(self.obstacles) == 0:
            self.new_obstacle()
        elif furtherst_obstacle < Window.size[0]*0.65:
            if uniform(0, 1 + log(1. + self.score*1e-5)) > 0.995:
                self.new_obstacle()

        if platform == 'ios' and self.banner_ad.hidden_ad() == 0:
            self.banner_ad.show_ads()

        self.score += 0.05


    def update_death(self, dt):
        self.mcnay.update_after_death(self.g_grav)
        if self.mcnay.velocity[0] == 0 and self.mcnay.pos[1] == self.mcnay.ground:
            self.process.cancel()

        if platform == 'ios' and not self.interstitial_ad.is_showing() :
            print('showing')
            self.interstitial_ad.show_ads()


    def obstacle_collision(self):
        self.process.cancel()
        self.mcnay.death()
        if platform == 'ios':
            self.banner_ad.hide_ads()
        if platform == 'android':
            self.ads.hide_banner()
            self.ads.destroy_banner()
            self.ads.show_interstitial()

        self.process = Clock.schedule_interval(self.update_death, 1.0/60.0)

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
        popup = endGamePopup(self.score, auto_dismiss=False)
        popup.open()




class JumpyKittenPage(Screen):
    def __init__(self, **kwargs):
        super(JumpyKittenPage, self).__init__(**kwargs)
        self.game = JumpyKittenGame()
        self.add_widget(self.game)

    def on_enter(self):
        self.game.reset()
        self.game.start()

    def on_leave(self):
        self.game.reset()
