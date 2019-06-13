from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

class infoPage(Screen):
	pass

Builder.load_string("""
<infoPage>:
	name: 'InfoPage'
	Label:
		text: 'InfoPage'
	Button:
		text: 'Back'
		size_hint: (.1, .1)
		pos_hint: {'x':0, 'y':.9}
		on_release: app.sm.current = 'MainPage'
""")


"""
InfoPage / In app purchases page (not sure if we want to include this in the first version)


"""