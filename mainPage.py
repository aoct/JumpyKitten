from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

from kivmob import KivMob, TestIds


class mainPage(Screen):

    def __init__(self, **kwargs):
        super(mainPage, self).__init__(**kwargs)

        # self.ads = KivMob(TestIds.APP)
        self.ads = KivMob('ca-app-pub-8564280870740386~8534172049')
        # self.ads.new_interstitial(TestIds.INTERSTITIAL)
        self.ads.new_interstitial('ca-app-pub-8564280870740386/9108176670')
        self.ads.request_interstitial()

Builder.load_string("""
<mainPage>:
    name: 'MainPage'
    Image:
        allow_stretch: True
        source: "images/background.png"
        pos: 0, 0
        size: root.height * self.image_ratio, root.height
    Button:
        text: "Start"
        on_release: app.sm.current = 'GamePage'
        size_hint: (.3, .15)
        pos_hint: {'x':.35, 'y':.35}
        background_color: 0, 0, 0, .0
        Image:
            source: "images/pixel_gray_base.png"
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
        on_release: root.ads.show_interstitial()
    Button:
    	text: 'Info'
    	size_hint: (.15, .1)
		pos_hint: {'x':.8, 'y':.3}
        on_release: app.sm.current = 'InfoPage'
""")
