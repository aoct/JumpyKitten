import time

from random import uniform

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.utils import platform
from kivy.logger import Logger

from commercial.kivmob import KivMob, TestIds

from components.background import Background

class mainPage(Screen):
    background = ObjectProperty(Background())

    def __init__(self, **kwargs):
        super(mainPage, self).__init__(**kwargs)

        if platform == 'android':
            # self.ads = KivMob(TestIds.APP)
            # self.ads.new_interstitial(TestIds.INTERSTITIAL)
            # self.ads.new_banner(TestIds.BANNER)
            self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
            self.ads.new_interstitial('ca-app-pub-8564280870740386/9108176670')
            self.ads.new_banner('ca-app-pub-8564280870740386/9108176670')

            self.ads.request_interstitial()
            self.ads.request_banner()

        elif platform == 'ios':
            from pyobjus import autoclass
            self.banner_ad = autoclass('adSwitchBanner').alloc().init()
            self.interstitial_ad = autoclass('adSwitchInterstitial').alloc().init()

        self.bind(size=self.size_callback)

    def size_callback(self, instance, value):
        self.background.size = value
        self.background.update_position()

    def on_enter(self):
        if platform == 'ios':
            # if self.interstitial_ad.is_loaded():
            if platform == 'ios' and not self.interstitial_ad.is_showing() :
                if uniform(0,1) < 0.5:
                    self.interstitial_ad.show_ads()
            self.banner_ad.show_ads()
        if platform == 'android':
            if uniform(0,1) < 0.5:
                self.ads.show_interstitial()
            self.ads.show_banner()

    def on_leave(self):
        if platform == 'ios':
            self.banner_ad.hide_ads()
            self.interstitial_ad.hide_ads()
        elif platform == 'android':
            self.ads.hide_banner()
            # self.ads.destroy_interstitial()
            self.ads.request_interstitial()


Builder.load_string("""
<mainPage>:
    background: background
    Background:
        id: background
        pos: root.pos
    Button:
        on_release: app.sm.current = 'GamePage'
        size_hint: (.3, .3)
        pos_hint: {'x':.35, 'y':.35}
        background_color: 0, 0, 0, .0
        Image:
            source: "images/cats/basePinkCat_aoct/CAT_FRAME_0_HD.png"
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


  #   Button:
  #   	size_hint: (.1, .1)
		# pos_hint: {'x':.85, 'y':.45}
  #       on_release: app.sm.current = 'SettingsPage'
  #       background_color: 0, 0, 0, .0
  #       Image:
  #           source: "images/icons/settings.png"
  #           y: self.parent.y
  #           x: self.parent.x
  #           size: self.parent.size
  #           allow_stretch: True
    Button:
    	size_hint: (.2, .2)
		pos_hint: {'x':.02, 'y':.4}
        on_release: app.sm.current = 'RankPageUser'
        background_color: 0, 0, 0, .0
        Image:
            source: "images/icons/ranking.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
  #   Button:
  #   	size_hint: (.1, .1)
		# pos_hint: {'x':.85, 'y':.45}
  #       background_color: 0, 0, 0, .0
  #       on_release:
  #           root.ads.request_interstitial()
  #           root.ads.show_interstitial()
  #       Image:
  #           source: "images/icons/noads.png"
  #           y: self.parent.y
  #           x: self.parent.x
  #           size: self.parent.size
  #           allow_stretch: True
    Button:
    	size_hint: (.2, .2)
		pos_hint: {'x':.78, 'y':.4}
        on_release: app.sm.current = 'InfoPage'
        background_color: 0, 0, 0, .0
        Image:
            source: "images/icons/info.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
""")
