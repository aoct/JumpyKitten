from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

class mainPage(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.layout = FloatLayout(size=(300, 300))

		startButton = Button(text='Start', size_hint=(.5, .5), pos_hint={'x':.25, 'y':.25})
		startButton.bind(on_release=self.startButton_func)
		self.layout.add_widget(startButton)


	def startButton_func(self):
		self.manager.current = 'GamePage'
