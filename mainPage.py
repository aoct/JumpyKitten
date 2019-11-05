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
from kivy.clock import Clock

from commercial.kivmob import KivMob, TestIds, RewardedListenerInterface
from components.background import Background

from os.path import join

from plyer import notification

kittenColor = 'Pink'
reviewStatus = 'ToDo'

class mainPage(Screen):
    background = ObjectProperty(Background())
    collected_coins = NumericProperty(0)

    def __init__(self, **kwargs):
        super(mainPage, self).__init__(**kwargs)

        self.loadingPopup = LabelPopup('Loading...', auto_dismiss=False)

        if platform == 'android':
            self.ads = KivMob(TestIds.APP)
            self.ads.new_interstitial(TestIds.INTERSTITIAL)
            self.ads.new_banner(TestIds.BANNER)
            self.ads.new_banner(TestIds.BANNER)
            self.ads_listener = RewardedListenerInterface()
            self.ads.set_rewarded_ad_listener(self.ads_listener)
            self.ads.load_rewarded_ad(TestIds.REWARDED_VIDEO)
            # self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
            # self.ads.new_interstitial('ca-app-pub-8564280870740386/9108176670')
            # self.ads.new_banner('ca-app-pub-8564280870740386/9108176670')
            # self.ads.set_rewarded_ad_listener(RewardedListenerInterface())
            # self.ads.load_rewarded_ad('ca-app-pub-8564280870740386/3839785853')

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

        filename_review = join(self.user_data_dir, 'review.pickle')
        global reviewStatus
        if os.path.isfile(filename_review):
            reviewStatus = pickle.load(open(filename_review, 'rb'))
        else:
            pickle.dump(reviewStatus, open(filename_review, 'wb'))

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

        global reviewStatus
        if reviewStatus == 'ToDo': self.reviewNotification = ReviewNotification()

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
            self.ads.show_rewarded_ad()
            self.loadingPopup.open()
            for i in range(20):
                time.sleep(0.1)

            if self.ads_listener.hasOpened:
                while not self.ads_listener.Closed:
                    time.sleep(0.1)
                self.ads_listener.Closed = False
                self.loadingPopup.dismiss()
                if self.ads_listener.giveReward:
                    self.ads_listener.giveReward = False
                    self.popup = LabelPopup('You earned earned 25 coins', auto_dismiss=True)
                    self.popup.open()
                    filename = join(self.user_data_dir, 'collected_coins.pickle')
                    if os.path.isfile(filename):
                        self.collected_coins = pickle.load(open(filename, 'rb'))
                    else:
                        self.collected_coins = 0
                    self.collected_coins += 25
                    pickle.dump(self.collected_coins, open(filename, 'wb'))
                else:
                    self.popup = LabelPopup('No coins earned', auto_dismiss=True)
                    self.popup.open()
                self.ads_listener.hasOpened = False
            else:
                self.loadingPopup.dismiss()
                self.popup = LabelPopup('Reward video not available now.', auto_dismiss=True)
                self.popup.open()
        else:
            self.popup = LabelPopup('Reward video not available', auto_dismiss=True)
            self.popup.open()

class LabelPopup(Popup):
	def __init__(self, text, **kwargs):
		super(Popup, self).__init__(**kwargs)

		l = Label(text=text)
		self.add_widget(l)

class ReviewNotification(Popup):
    def __init__(self, **kwargs):
        super(Popup, self).__init__(**kwargs)

        self.title = 'Game Review'
        general_layout = GridLayout(cols = 1)
        text_label = Label(text = 'Did you enjoy the game?\nWrite an app review', font_size = 20)

        reviewButton = Button(text = 'review')
        reviewButton.bind(on_release = self.reviewGame)

        cancelButton = Button(text = 'Later')
        cancelButton.bind(on_release = self.dismiss)

        neverButton = Button(text = 'Do not show again')
        neverButton.bind(on_release = self.doNotShowAgain)

        general_layout.add_widget(text_label)
        general_layout.add_widget(reviewButton)
        general_layout.add_widget(cancelButton)
        general_layout.add_widget(neverButton)
        self.add_widget(general_layout)

        self.open()

        if platform == 'ios': self.user_data_dir = App.get_running_app().user_data_dir
        else: self.user_data_dir = 'data'


    def doNotShowAgain(self, instance):
        global reviewStatus
        reviewStatus = 'Never'
        filename_review = join(self.user_data_dir, 'review.pickle')
        if os.path.isfile(filename_review):
            reviewStatus = pickle.dump(reviewStatus, open(filename_review, 'wb'))
        self.dismiss()

    def reviewGame(self, instance):
        global reviewStatus
        reviewStatus = 'Reviewed'
        filename_review = join(self.user_data_dir, 'review.pickle')
        if os.path.isfile(filename_review):
            reviewStatus = pickle.dump(reviewStatus, open(filename_review, 'wb'))
        if platform == 'android':
            Wv()

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android.runnable import Runnable
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    activity = autoclass('org.renpy.android.PythonActivity').mActivity

    class Wv(Widget):
        def __init__(self, **kwargs):
            super(Wv, self).__init__(**kwargs)
            self.webview = WebView(activity)
            self.wvc = WebViewClient()
            Clock.schedule_once(self.create_webview, 0)

        @run_on_ui_thread
        def create_webview(self, *args):
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.setWebViewClient(self.wvc);
            activity.setContentView(self.webview)
            self.webview.loadUrl('http://www.google.com')



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
    BackgroundFloatLayout:
        id: coinFloat
        background_color: 1,0.7,0.7,0.9
        size_hint: (.09, .065)
        # width: 0.09*Window.size[0]
        # height: 0.1*Window.size[1]
        y: 0.8*Window.size[1]
        x: 0.03*Window.size[0]
        Image:
            source: "images/COIN_HD.png"
            height: 0.9*coinFloat.height
            width: 0.9*coinFloat.height
            y: coinFloat.y
            x: coinFloat.x - coinFloat.width*0.45 + 0.9*coinFloat.height/2
        Label:
            id: coinLabel
            font_size: 60
            bold: True
            text: "{:03.0f} ".format(root.collected_coins)
            size: self.texture_size
            x: coinFloat.x + coinFloat.width*0.5 - self.texture_size[0]*0.5
            y: coinFloat.y

<LabelPopup>:
	# title: ''
	size_hint: (0.36, 0.5)
	pos_hint: {'x': 0.32, 'y': 0.45}
	# separator_color: 0x77 / 255., 0x6e / 255., 0x65 / 255., 1.
	# title_size: '20sp'
""")
