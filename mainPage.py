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

from commercial.kivmob import KivMob, TestIds, RewardedListenerInterface
from commercial.kivmob27 import KivMob27

from components.background import Background

from os.path import join

kittenColor = 'Pink'

class mainPage(Screen):
    background = ObjectProperty(Background())
    collected_coins = NumericProperty(0)

    def __init__(self, **kwargs):
        super(mainPage, self).__init__(**kwargs)

        if platform == 'android':
            self.ads = KivMob(TestIds.APP)
            self.ads.new_interstitial(TestIds.INTERSTITIAL)
            self.ads.new_banner(TestIds.BANNER)
            self.ads.new_banner(TestIds.BANNER)
            # self.ads.set_rewarded_ad_listener(RewardedListenerInterface())
            # self.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)
            # self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
            # self.ads.new_interstitial('ca-app-pub-8564280870740386/9108176670')
            # self.ads.new_banner('ca-app-pub-8564280870740386/9108176670')
            # self.ads.set_rewarded_ad_listener(RewardedListenerInterface())
            # self.ads.load_rewarded_ad('ca-app-pub-8564280870740386/3839785853')

            self.ads27 = KivMob27(TestIds.APP)
            self.ads27.new_rewarded(TestIds.REWARDED_VIDEO)
            self.ads27.request_rewarded()

            self.ads.request_interstitial()
            self.ads.request_banner()

        elif platform == 'ios':
            from pyobjus import autoclass
            self.banner_ad = autoclass('adSwitchBanner').alloc().init()
            # self.interstitial_ad = autoclass('adSwitchInterstitial').alloc().init()

        self.bind(size=self.size_callback)

        if platform == 'ios':
            self.user_data_dir = App.get_running_app().user_data_dir
        else:
            self.user_data_dir = 'data'

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
            self.ads.show_banner()

        filename = join(self.user_data_dir, 'kittenColor.pickle')
        if os.path.isfile(filename):
            global kittenColor
            kittenColor = pickle.load(open(filename, 'rb'))

        self.mcnay_image.source = 'images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor)

        filename = join(self.user_data_dir, 'collected_coins.pickle')
        if os.path.isfile(filename):
            self.collected_coins = pickle.load(open(filename, 'rb'))

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
            # hasShown = self.ads.show_rewarded_ad()
            self.ads27.show_rewarded_ad(reward_type='test reward type')
        #     print('[DEBUG]: hasShown =',hasShown)
        #     if hasShown:
        #         self.popup = LabelPopup('You earned earned 25 coins', auto_dismiss=True)
        #         self.popup.open()
        #         filename = join(self.user_data_dir, 'collected_coins.pickle')
        #         if os.path.isfile(filename):
        #             collected_coins = pickle.load(open(filename, 'rb'))
        #         else:
        #             collected_coins = 0
        #         collected_coins += 25
        #         pickle.dump(collected_coins, open(filename, 'wb'))
        #     else:
        #         self.popup = LabelPopup('Reward video not available now. Retray later', auto_dismiss=True)
        #         self.popup.open()
        # else:
        #     self.popup = LabelPopup('Reward video not available', auto_dismiss=True)
        #     self.popup.open()

    def on_resume(self):
        res = self.ads27.get_reward_type()
        print(res)
        if res != "No reward":
            #Give reward based on reward_type
            self.reward(res)

    def reward(self, reward_type):
        #reward the player
        self.ads27.playerRewarded() #reset the reward so it is not triggered again

class LabelPopup(Popup):
	def __init__(self, text, **kwargs):
		super(Popup, self).__init__(**kwargs)

		l = Label(text=text)
		self.add_widget(l)

Builder.load_string("""
#:import Window kivy.core.window.Window
<mainPage>:
    background: background
    mcnay_image: image
    Background:
        id: background
        pos: root.pos
    Button:
        on_release: app.sm.current = 'GamePage'
        size_hint: (.3, .3)
        pos_hint: {'x':.35, 'y':.35}
        background_color: 0, 0, 0, .0
        Image:
            id: image
            # source: "images/cats/basePinkCat_aoct/CAT_FRAME_0_HD.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    Label:
        text: "Press to Start"
        pos_hint: {'x':.35, 'y':.25}
        size_hint: (0.3, 0.1)
        halign: 'center'
        valign: 'center'
        font_size: 60
        color: [226/255.0, 158/255.0, 163/255.0, 1]
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
        Image:
            source: "images/pinkBox.png"
            height: 0.035*Window.size[0]
            width: 0.13*Window.size[0]
            x: 0.065*Window.size[0]
            center_y: 0.8*Window.size[1]
        Image:
            source: "images/coin_HD.png"
            height: 0.03*Window.size[0]
            width: 0.03*Window.size[0]
            center_y: 0.8*Window.size[1]
            right: 0.12*Window.size[0]
        Label:
            font_size: 60
            x: 0.125*Window.size[0]
            center_y: 0.8*Window.size[1]
            markup: True
            bold: True
            text: '[color=e29ea3]: {:.0f}[/color]'.format(root.collected_coins)

<LabelPopup>:
	# title: ''
	size_hint: (0.36, 0.5)
	pos_hint: {'x': 0.32, 'y': 0.45}
	# separator_color: 0x77 / 255., 0x6e / 255., 0x65 / 255., 1.
	# title_size: '20sp'
""")
