import os, sys
__version__ = "1.1.0"
import kivy
kivy.require("1.10.0")
from kivy.utils import platform

if platform != 'ios' and platform != 'android':
	print('Showing a smartphone-like screen')
	from kivy.config import Config
	# screen_ratio = 18./9.0 #Mot one
	screen_ratio = 19.5/9 #iPhoneX
	x = 540
	print('Screen size: {} : {:.0f}'.format(screen_ratio*x, x))
	Config.set('graphics', 'width', str(int(x*screen_ratio)))
	Config.set('graphics', 'height', str(x))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window

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

from font_scale import scaling

class JumpyKittenApp(App):
	def build(self):
		self.sm = ScreenManager(transition = NoTransition())

		scaling(Window.size)

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
