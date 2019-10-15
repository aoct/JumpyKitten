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

if platform == 'android':
	from android_libraries import gs_android
	# from android_libraries.gplay import GoogleClient

from kivy.uix.popup import Popup
class GooglePlayPopup(Popup):
	pass

class JumpyKittenApp(App):
	def build_config(self, config):
		if platform == 'android':
			config.setdefaults('play', {'use_google_play': '0'})

	def build(self):
		# global app
		# app = self
		#
		self.leaderboard_topscore = 'CgkI8dS1q5oFEAIQAA'

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

		if platform == 'android':
			self.use_google_play = self.config.getint('play', 'use_google_play')
			if self.use_google_play:
			    gs_android.setup(self)
				# self.gs_android = GoogleClient()
			else:
			    Clock.schedule_once(self.ask_google_play, .5)

		return self.sm

	def create_gs(self):
		self.gs_android = GoogleClient()
		self.gs_android.connect()
		print('gs_android connected:', self.gs_android.is_connected())

	def gs_score(self, score):
		print('[DEBUG]: if on android send scores to google play')
		if platform == 'android' and self.use_google_play:
			gs_android.leaderboard(self.leaderboard_topscore, score)
			# self.gs_android.submit_score('top_score', score)

	def gs_show_leaderboard(self):
		print('[DEBUG]: Showing leaderboard')
		if platform == 'android':
			if self.use_google_play:
				gs_android.show_leaderboard(leaderboard_highscore)
				# self.gs_android.show_leaderboard('top_score')
		else:
			self.ask_google_play()

	def ask_google_play(self, *args):
		popup = GooglePlayPopup()
		popup.open()

	def activate_google_play(self):
		if platform == 'android':
			self.config.set('play', 'use_google_play', '1')
			self.config.write()
			self.use_google_play = 1
			gs_android.setup(self)
			# self.create_gs()
		else:
			print("[DEBUG]: Google play only available on android")


if __name__ =="__main__":
	game = JumpyKittenApp()
	game.run()
