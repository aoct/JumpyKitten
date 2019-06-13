from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

from kivmob import KivMob, TestIds


class mainPage(Screen):

    def __init__(self, **kwargs):
        super(mainPage, self).__init__(**kwargs)

        self.ads = KivMob(TestIds.APP)
        self.ads.new_interstitial(TestIds.INTERSTITIAL)
        self.ads.request_interstitial()

Builder.load_string("""
<mainPage>:
    name: 'MainPage'
    Label:
        text: 'MainPage'
    Button:
        text: "Start"
		size_hint: (.3, .15)
		pos_hint: {'x':.35, 'y':.65}
        on_release: app.sm.current = 'GamePage'
    Button:
    	text: 'Ranking'
    	size_hint: (.3, .15)
		pos_hint: {'x':.35, 'y':.50}
        on_release: app.sm.current = 'RankPage'
    Button:
    	text: 'Ads'
    	size_hint: (.3, .15)
		pos_hint: {'x':.35, 'y':.35}
        on_release: root.ads.show_interstitial()
    Button:
    	text: 'Settings'
    	size_hint: (.3, .15)
		pos_hint: {'x':.35, 'y':.2}
        on_release: app.sm.current = 'SettingsPage'
""")
