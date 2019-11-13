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
from kivy.uix.floatlayout import FloatLayout

from commercial.kivmob import KivMob, TestIds

from components.background import Background
from components.mcnay import Mcnay
from components.coin import Coin
from components.obstacles.rock import Rock
from components.obstacles.bird import Bird
from components.obstacles.log import Log

from random import uniform

from os.path import join

import time

reviveCoinsPrice = 25

class endGamePopup(Popup):
    score = NumericProperty()
    def __init__(self, score, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.score = score

class JumpyKittenPage(Screen):
    background = ObjectProperty(Background())
    score = NumericProperty(0)
    collected_coins = NumericProperty(0)

    def __init__(self, **kwargs):
        super(JumpyKittenPage, self).__init__(**kwargs)

        self.g_grav = -0.5 #pizel * frame_rate^2
        self.obstacles = []
        self.coins = []
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
            # self.ads = KivMob(TestIds.APP)
            # self.ads.new_banner(TestIds.BANNER)
            # self.ads.new_interstitial(TestIds.INTERSTITIAL)
            self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
            self.ads.new_banner('ca-app-pub-8564280870740386/2464625123')
            self.ads.new_interstitial('ca-app-pub-8564280870740386/8985921895')

        if platform == 'ios':
            self.user_data_dir = App.get_running_app().user_data_dir
        else:
            self.user_data_dir = 'data'

        self.reset()

    def on_enter(self):
        self.reset()
        self.start()

    def on_leave(self):
        self.reset()

    def start(self):
        if platform == 'android':
            print('Requesting banner')
            self.ads.request_banner()
            self.ads.request_interstitial()
            self.ads.show_banner()
        self.hasRevived = False
        self.endgamePopup = endGamePopup(self.score, auto_dismiss=False)
        self.process = Clock.schedule_interval(self.update, 1.0/60.0)

    def reset(self):
        if hasattr(self, 'process'):
            self.process.cancel()
        self.updates = 0
        self.score = 0
        self.mcnay.reset()
        for obstacle in self.obstacles:
            self.remove_widget(obstacle)
        self.obstacles = []

        for coin in self.coins:
            self.remove_widget(coin)
        self.coins = []

        self.collected_coins = 0
        filename = join(self.user_data_dir, 'collected_coins.pickle')
        if os.path.isfile(filename):
            self.collected_coins = pickle.load(open(filename, 'rb'))

    def new_obstacle(self):
        if self.score > 100 and uniform(0, 1 + log(1. + self.score*1e-5)) > 0.7:
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
        idx_to_pop = None
        for i, o in enumerate(self.obstacles):
            o.update(self.score)
            if o.type == 'ground steady' and o.x > furtherst_obstacle:
                furtherst_obstacle = o.x
            if o.x + o.width < 0:
                self.remove_widget(o)
                idx_to_pop = i
            else:
                if self.mcnay.collision_with_obstacle(o):
                    self.i_obstacle_collided = i
                    self.obstacle_collision()
        if not idx_to_pop is None:
            self.obstacles.pop(idx_to_pop)

        if len(self.obstacles) == 0:
            self.new_obstacle()
        elif furtherst_obstacle < Window.size[0]*0.65:
            if uniform(0, 1 + log(1. + self.score*1e-5)) > 0.995:
                self.new_obstacle()

        idx_to_pop = None
        for i, c in enumerate(self.coins):
            c.update(self.score)
            if c.x + c.width < 0:
                self.remove_widget(c)
                idx_to_pop = i
            elif self.mcnay.collision_with_obstacle(c):
                self.remove_widget(c)
                idx_to_pop = i
                self.collected_coins += 1
        if not idx_to_pop is None:
            self.coins.pop(idx_to_pop)

        if self.score%10 == 0 and uniform(0,1) > 0.6:
            min_y = 0.1*Window.size[1]
            last_o = self.obstacles[-1]
            if last_o.type == 'ground steady' and last_o.x+last_o.width > 0.9*Window.size[0]:
                min_y = last_o.y+1.2*last_o.height
            c = Coin(self.score)
            c.x = self.width
            self.add_widget(c)
            self.coins.append(c)

        self.updates += 1
        self.score = self.updates/20.

    def update_death(self, dt):
        self.mcnay.update_after_death(self.g_grav)
        if self.mcnay.velocity[0] <= 1 and self.mcnay.pos[1] == self.mcnay.ground_dead:
            self.process.cancel()
            if len(self.score_history) == 1 or self.score > max(self.score_history[:-1]):
                App.get_running_app().rankPageWorld.reset_ranking()

        if platform == 'ios' and not self.interstitial_ad.is_showing() :
            if self.score > 30 and uniform(0,1) < 0.5:
                self.interstitial_ad.show_ads()

    def obstacle_collision(self, cancel_process=True):
        if cancel_process:
            self.process.cancel()
        self.mcnay.death()
        self.remove_widget(self.mcnay)
        self.add_widget(self.mcnay)
        if platform == 'ios':
            self.banner_ad.hide_ads()
        if platform == 'android':
            self.ads.hide_banner()
            self.ads.destroy_banner()
            if self.score > 30 and uniform(0,1) < 0.5:
                self.ads.show_interstitial()

        self.process = Clock.schedule_interval(self.update_death, 1.0/60.0)

        filename = join(self.user_data_dir, 'score_history.pickle')
        if os.path.isfile(filename) :
            self.score_history = pickle.load(open(filename, 'rb'))
        else:
            self.score_history = []
            if not os.path.isdir(self.user_data_dir):
                os.mkdir(self.user_data_dir)

        self.score_history += [self.score]
        pickle.dump(self.score_history, open(filename, 'wb'))

        filename = join(self.user_data_dir, 'collected_coins.pickle')
        pickle.dump(self.collected_coins, open(filename, 'wb'))

        self.endgamePopup.score = self.score
        if not self.hasRevived and self.collected_coins >= reviveCoinsPrice:
            self.endgamePopup.reviveBotton.disabled = False
            self.endgamePopup.reviveBotton.image.source = "images/icons/revive.png"
        else:
            self.endgamePopup.reviveBotton.disabled = True
            self.endgamePopup.reviveBotton.image.source = "images/icons/revive_disable.png"
        self.endgamePopup.open()

    def revive(self):
        self.hasRevived = True
        i_ob = self.i_obstacle_collided
        obstacle = self.obstacles[i_ob]
        self.remove_widget(obstacle)
        self.obstacles.pop(i_ob)

        self.collected_coins -= reviveCoinsPrice
        filename = join(self.user_data_dir, 'collected_coins.pickle')
        pickle.dump(self.collected_coins, open(filename, 'wb'))

        self.mcnay.reset()
        self.process.cancel()
        self.process = Clock.schedule_interval(self.update, 1.0/60.0)



# class JumpyKittenPage(Screen):

#     def __init__(self, **kwargs):
#         super(JumpyKittenPage, self).__init__(**kwargs)
#         self.game = JumpyKittenGame()
#         self.add_widget(self.game)

    # def on_enter(self):
    #     self.game.reset()
    #     self.game.start()

    # def on_leave(self):
    #     self.game.reset()
