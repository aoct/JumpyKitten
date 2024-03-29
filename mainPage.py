import os, pickle, time

from random import uniform

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.utils import platform
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import sp, dp
import webbrowser

from commercial.kivmob import KivMob, TestIds, RewardedListenerInterface
from components.background import Background

from os.path import join
import threading
from functools import partial

from font_scale import font_scaling, scaling

kittenColor = 'Pink'

class mainPage(Screen):
    background = ObjectProperty(Background())
    collected_coins = NumericProperty(0)
    font_scale = NumericProperty(1)

    def __init__(self, **kwargs):
        super(mainPage, self).__init__(**kwargs)

        if platform == 'ios': self.user_data_dir = App.get_running_app().user_data_dir
        else: self.user_data_dir = 'data'

        self.font_scale = pickle.load(open(join(self.user_data_dir, 'fontScaling.pickle'), 'rb'))[0]

        self.loadingPopup = LabelPopup('Loading...', self.font_scale, auto_dismiss=False)

        if platform == 'android':
            # self.ads = KivMob(TestIds.APP)
            # self.ads.new_interstitial(TestIds.INTERSTITIAL)
            # self.ads.new_banner(TestIds.BANNER)
            # self.ads_listener = RewardedListenerInterface()
            # self.ads.set_rewarded_ad_listener(self.ads_listener)
            # self.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)
            self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
            self.ads.new_interstitial('ca-app-pub-8564280870740386/9108176670')
            self.ads.new_banner('ca-app-pub-8564280870740386/9108176670')
            self.ads_listener = RewardedListenerInterface()
            self.ads.set_rewarded_ad_listener(self.ads_listener)
            self.ads.load_rewarded_ad('ca-app-pub-8564280870740386/3839785853')

            self.ads.request_interstitial()
            self.ads.request_banner()

        elif platform == 'ios':
            from pyobjus import autoclass
            self.banner_ad = autoclass('adSwitchBanner').alloc().init()
            # self.interstitial_ad = autoclass('adSwitchInterstitial').alloc().init()

        self.bind(size=self.size_callback)

        filename = join(self.user_data_dir, 'kittenColor.pickle')
        if os.path.isfile(filename):
            global kittenColor
            kittenColor = pickle.load(open(filename, 'rb'))

        self.mcnay_image.source = 'images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor)
        self.collected_coins = 0



    def size_callback(self, instance, value):
        self.background.size = value
        self.background.update_position()

    def on_enter(self):
        if platform == 'ios':
            from pyobjus import autoclass
            self.interstitial_ad = autoclass('adSwitchInterstitial').alloc().init()
            if self.interstitial_ad.is_loaded():
                self.interstitial_ad.show_ads()
            self.banner_ad.show_ads()
        if platform == 'android':
            if uniform(0,1) < 0.5:
                self.ads.show_interstitial()
            else:
                # pass
                self.ads.show_banner()

        filename = join(self.user_data_dir, 'kittenColor.pickle')
        if os.path.isfile(filename):
            global kittenColor
            kittenColor = pickle.load(open(filename, 'rb'))

        self.mcnay_image.source = 'images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor)

        filename = join(self.user_data_dir, 'collected_coins.pickle')
        if os.path.isfile(filename):
            self.collected_coins = pickle.load(open(filename, 'rb'))

        filename = join(self.user_data_dir, 'review.pickle')
        if os.path.isfile(filename):
            reviewStatus = pickle.load(open(filename, 'rb'))
        else:
            reviewStatus = [0, 30]
        reviewStatus[0] += 1
        pickle.dump(reviewStatus, open(filename, 'wb'))
        if reviewStatus[0] == 5 or reviewStatus[0]%reviewStatus[1] == 0:
            self.reviewNotification = ReviewNotification(self.font_scale, auto_dismiss=True)

    def on_leave(self):
        if platform == 'ios':
            self.banner_ad.hide_ads()
            self.interstitial_ad.hide_ads()
        elif platform == 'android':
            self.ads.hide_banner()
            # self.ads.destroy_interstitial()
            self.ads.request_interstitial()

    def show_reward_video(self):
        if platform == 'android':
            self.loadingPopup.open()

            myThread = threading.Thread(target=self.ads.show_rewarded_ad)
            myThread.start()
            # self.ads.show_rewarded_ad()
            for i in range(30):
                time.sleep(0.1)

            self.loadingPopup.dismiss()
            if self.ads_listener.hasOpened:
                while not self.ads_listener.Closed:
                    time.sleep(0.1)
                self.ads_listener.Closed = False
                if self.ads_listener.giveReward:
                    self.ads_listener.giveReward = False
                    self.popup = LabelPopup('You earned 25 coins', self.font_scale, auto_dismiss=True)
                    self.popup.open()
                    filename = join(self.user_data_dir, 'collected_coins.pickle')
                    if os.path.isfile(filename):
                        self.collected_coins = pickle.load(open(filename, 'rb'))
                    else:
                        self.collected_coins = 0
                    self.collected_coins += 25
                    pickle.dump(self.collected_coins, open(filename, 'wb'))
                else:
                    self.popup = LabelPopup('No coins earned', self.font_scale, auto_dismiss=True)
                    self.popup.open()
                self.ads_listener.hasOpened = False
            else:
                self.popup = LabelPopup('Reward video not available', self.font_scale, auto_dismiss=True)
                self.popup.open()
        else:
            self.popup = LabelPopup('Reward video not available', self.font_scale, auto_dismiss=True)
            self.popup.open()

class LabelPopup(Popup):
    def __init__(self, text, font_scale, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.title = ''
        self.size_hint = (0.4, 0.35)
        self.pos_hint = {'x': 0.3, 'y': 0.4}
        self.separator_height = 0
        self.title_size = font_scaling(0, font_scale)
        l = Label(text=text, font_size = font_scaling(30, font_scale), valign='center', halign='center')
        l.text_size = (0.4*Window.size[0], 0.35*Window.size[1])
        self.add_widget(l)

class ReviewNotification(Popup):
    def __init__(self, font_scale, **kwargs):
        super(Popup, self).__init__(**kwargs)

        self.title = 'Are you enjoying the game?\nGive us a feedback'
        self.title_size = font_scaling(50, font_scale)
        self.title_align = 'center'
        self.separator_height = 0
        general_layout = GridLayout(cols = 1, spacing= [10,10])

        reviewButton = Button(text = 'Leave a review now', bold=True, font_size=font_scaling(35, font_scale))
        reviewButton.background_color = 0, 0, 0, 1.
        reviewButton.bind(on_release = self.reviewGame)

        cancelButton = Button(text = 'Ask me again later', bold=True, font_size=font_scaling(35, font_scale))
        cancelButton.background_color = 0, 0, 0, 1.
        cancelButton.bind(on_release = self.dismiss)

        neverButton = Button(text = 'Do not ask again', bold=True, font_size=font_scaling(35, font_scale))
        neverButton.background_color = 0, 0, 0, 1.
        neverButton.bind(on_release = self.doNotShowAgain)

        general_layout.add_widget(reviewButton)
        general_layout.add_widget(cancelButton)
        general_layout.add_widget(neverButton)
        self.add_widget(general_layout)
        self.size_hint = (0.5, 0.7)
        self.open()

        if platform == 'ios': self.user_data_dir = App.get_running_app().user_data_dir
        else: self.user_data_dir = 'data'
        self.reviewStatus = pickle.load(open(join(self.user_data_dir, 'review.pickle'), 'rb'))


    def doNotShowAgain(self, instance):
        self.reviewStatus[1] *= 3
        filename = join(self.user_data_dir, 'review.pickle')
        pickle.dump(self.reviewStatus, open(filename, 'wb'))
        self.dismiss()

    def reviewGame(self, instance):
        reviewStatus = [0, 500]
        filename = join(self.user_data_dir, 'review.pickle')
        pickle.dump(reviewStatus, open(filename, 'wb'))
        self.dismiss()
        webbrowser.open('https://play.google.com/store/apps/details?id=org.aoct.jumpykitten.jumpykitten')


Builder.load_string("""
#:import Window kivy.core.window.Window
#:import font_scaling font_scale.font_scaling

<mainPage>:
    background: background
    mcnay_image: image
    Background:
        id: background
        pos: root.pos
    Button:
        on_release: app.sm.current = 'GamePage'
        size_hint: (.6, .8)
        pos_hint: {'x':.2, 'y':.1}
        background_color: 0, 0, 0, .0
        # Image:
        #     size: self.parent.size
        #     pos: self.parent.pos
        #     source: "images/cats/CAT_FRAME_0_HD_debug.png"
        #     allow_stretch: True
        #     keep_ratio: False
        # Image:
        #     source: "images/cats/CAT_FRAME_0_HD_debug.png"
        #     size: (0.15*Window.size[0], 0.23*Window.size[1])
        #     center_y: self.parent.center_y
        #     center_x: self.parent.center_x
        #     allow_stretch: True
        #     keep_ratio: False
        Image:
            id: image
            size: (0.15*Window.size[0], 0.23*Window.size[1])
            center_y: self.parent.center_y
            center_x: self.parent.center_x
            allow_stretch: True
            keep_ratio: True
    Label:
        text: "Touch kitten to start"
        pos_hint: {'x':.35, 'y':.65}
        size_hint: (0.3, 0.1)
        halign: 'center'
        valign: 'center'
        font_size: font_scaling(35, root.font_scale) #'35sp'
        color: [255/255.0, 255/255.0, 255/255.0, 1]
        markup: True
        bold: True
    Button:
    	size_hint: (.2, .2)
		pos_hint: {'x':.02, 'y':.25}
        on_release: app.sm.current = 'RankPageWorld'
        background_color: 0, 0, 0, .0
        Image:
            source: "images/icons/ranking.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    Button:
    	size_hint: (.2, .2)
		pos_hint: {'x':.78, 'y':.25}
        on_release: app.sm.current = 'InfoPage'
        background_color: 0, 0, 0, .0
        Image:
            source: "images/icons/info.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    Button:
    	size_hint: (.2, .2)
		pos_hint: {'x':.78, 'y':.55}
        on_release: root.show_reward_video()
        background_color: 0, 0, 0, .0
        Image:
            source: "images/icons/video.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    Button:
        size_hint: (.2, .2)
        pos_hint: {'x':.02, 'y':.55}
        on_release: app.sm.current = 'KittenPage'
        background_color: 0, 0, 0, .0
        Image:
            source: "images/icons/kittens.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    BackgroundFloatLayout:
        id: coinFloat
        background_color: 1,0.7,0.7,0.9
        size_hint: (.09, .065)
        y: 0.8*Window.size[1]
        x: 0.03*Window.size[0]
        GridLayout:
            cols:3
            pos_hint: {'x':0, 'y': 0}
            size_hint: (1., 1.)
            Label:
                text: ''
                size_hint_x: 0.02
            Image:
                source: "images/coin.png"
                size_hint: (.25, .95)
                pos_hint_x: 0.05
            Label:
                id: coinLabel
                size_hint: (.70, .9)
                font_size: font_scaling(35, root.font_scale) #'35sp'
                bold: True
                text: " {:03.0f} ".format(root.collected_coins)

# <LabelPopup>:
# 	title: ''
# 	size_hint: (0.4, 0.35)
# 	pos_hint: {'x': 0.3, 'y': 0.4}
# 	separator_height: 0
# 	title_size: '0sp'
""")
