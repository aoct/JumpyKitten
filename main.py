import os, sys

import kivy
kivy.require("1.10.0")

if os.name == 'posix':
	print('Showing a smartphone-like screen')
	from kivy.config import Config
	Config.set('graphics', 'width', '960')
	Config.set('graphics', 'height', '540')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform

if platform == 'ios':
	sys.path.append("_applibs")
sys.path.append(".")
sys.path.append("iOS_libraries")

from JumpyKitten import JumpyKittenPage
from mainPage import mainPage
from infoPage import infoPage
from rankPage import rankPage
from settingsPage import settingsPage
from rankPageUser import rankPageUser
from rankPageWorld import rankPageWorld

class JumpyKittenApp(App):
	def build(self):
		print('Building the main App')
		self.sm = ScreenManager()

		self.mainPage = mainPage(name = 'MainPage')
		self.sm.add_widget(self.mainPage)

		self.gamePage = JumpyKittenPage(name='GamePage')
		self.sm.add_widget(self.gamePage)

		self.infoPage = infoPage(name = 'InfoPage')
		self.sm.add_widget(self.infoPage)

		self.rankPage = rankPage(name='RankPage')
		self.sm.add_widget(self.rankPage)

		self.settingsPage = settingsPage(name='SettingsPage')
		self.sm.add_widget(self.settingsPage)

		self.rankPageUser = rankPageUser(name='RankPageUser')
		self.sm.add_widget(self.rankPageUser)

		self.rankPageWorld = rankPageWorld(name='RankPageWorld')
		self.sm.add_widget(self.rankPageWorld)

		return self.sm


if __name__ =="__main__":
	game = JumpyKittenApp()
	game.run()
