from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivmob import KivMob, TestIds

from components.background import Background

class mainPage(Screen):
    background = ObjectProperty(Background())

    def __init__(self, **kwargs):
        super(mainPage, self).__init__(**kwargs)

        self.ads = KivMob(TestIds.APP)
        # self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
        self.ads.new_interstitial(TestIds.INTERSTITIAL)
        # self.ads.new_interstitial('ca-app-pub-8564280870740386/9108176670')

        self.bind(size=self.size_callback)

    def size_callback(self, instance, value):
        self.background.size = value
        self.background.update_position()

Builder.load_string("""
<mainPage>:
    background: background
    Background:
        id: background
        pos: root.pos
    Button:
        text: " "
        on_release: app.sm.current = 'GamePage'
        size_hint: (.2, .2)
        pos_hint: {'x':.4, 'y':.4}
        background_color: 0, 0, 0, .0
        Image:
            source: "images/cats/pink_nyan/frame_5_delay-0.07s.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    Button:
    	text: 'Settings'
    	size_hint: (.15, .1)
		pos_hint: {'x':.05, 'y':.45}
        on_release: app.sm.current = 'SettingsPage'
    Button:
    	text: 'Rank'
    	size_hint: (.15, .1)
		pos_hint: {'x':.8, 'y':.6}
        on_release: app.sm.current = 'RankPage'
    Button:
    	text: 'Ads'
    	size_hint: (.15, .1)
		pos_hint: {'x':.8, 'y':.45}
        on_release:
            root.ads.request_interstitial()
            root.ads.show_interstitial()
    Button:
    	text: 'Info'
    	size_hint: (.15, .1)
		pos_hint: {'x':.8, 'y':.3}
        on_release: app.sm.current = 'InfoPage'
""")
