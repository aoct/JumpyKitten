from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

class mainPage(Screen):
	pass

Builder.load_string("""
<mainPage>:
    name: 'MainPage'
    Label:
        text: 'MainPage'
    Button:
        text: "Start"
		size_hint: (.3, .3)
		pos_hint: {'x':.35, 'y':.35}
        on_release: app.sm.current = 'GamePage'
""")
