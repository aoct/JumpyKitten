from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

class infoPage(Screen):
	pass

Builder.load_string("""
<infoPage>:
	name: 'InfoPage'
	Image:
        allow_stretch: True
        source: "images/background.png"
        pos: 0, 0
        size: root.height * self.image_ratio, root.height
	Label:
		text: 'Jumpy Kitten game developed by Cerri O. & Tamborini A.'
	Button:
		text: 'Back'
		size_hint: (.1, .1)
		pos_hint: {'x':0, 'y':.9}
		on_release: app.sm.current = 'MainPage'
""")


"""
InfoPage / In app purchases page (not sure if we want to include this in the first version)


"""
