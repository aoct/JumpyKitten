import os, sys
__version__ = "1.0.0"
import kivy
kivy.require("1.10.0")
from kivy.utils import platform

if platform != 'ios' and platform != 'android':
	print('Showing a smartphone-like screen')
	from kivy.config import Config
	Config.set('graphics', 'width', '1140')
	Config.set('graphics', 'height', '540')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

sys.path.append(".")
if platform == 'ios':
	sys.path.append("_applibs")
	sys.path.append("iOS_libraries")

from JumpyKitten import JumpyKittenPage
from mainPage import mainPage
from infoPage import infoPage
from settingsPage import settingsPage
from rankPageUser import rankPageUser
from rankPageWorld import rankPageWorld
from kittenPage import kittenPage

class JumpyKittenApp(App):
	def build(self):
		self.sm = ScreenManager(transition = NoTransition())

		self.mainPage = mainPage(name = 'MainPage')
		self.sm.add_widget(self.mainPage)

		self.gamePage = JumpyKittenPage(name='GamePage')
		self.sm.add_widget(self.gamePage)

		self.infoPage = infoPage(name = 'InfoPage')
		self.sm.add_widget(self.infoPage)

		self.settingsPage = settingsPage(name='SettingsPage')
		self.sm.add_widget(self.settingsPage)

		self.rankPageUser = rankPageUser(name='RankPageUser')
		self.sm.add_widget(self.rankPageUser)

		self.rankPageWorld = rankPageWorld(name='RankPageWorld')
		self.sm.add_widget(self.rankPageWorld)

		self.kittenPage = kittenPage(name='KittenPage')
		self.sm.add_widget(self.kittenPage)

		return self.sm


if __name__ =="__main__":
	game = JumpyKittenApp()
	game.run()
