import kivy
kivy.require("1.8.0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from JumpyKittenNewVersion import JumpyKittenPage
from mainPage import mainPage


class JumpyKittenApp(App):
	def build(self):
		self.sm = ScreenManager()

		self.mainPage = mainPage(name = 'MainPage')
		self.sm.add_widget(self.mainPage)

		self.gamePage = JumpyKittenPage(name='GamePage')
		self.sm.add_widget(self.gamePage)

		return self.sm


if __name__ =="__main__":
	game = JumpyKittenApp()
	game.run()