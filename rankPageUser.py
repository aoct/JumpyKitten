import os, pickle, getpass, socket

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.utils import platform

from components.background import Background

from os.path import join

import gspread
from oauth2client.service_account import ServiceAccountCredentials

class rankPageUser(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(rankPageUser, self).__init__(**kwargs)
		self.master_grid = GridLayout(cols=1,
									   size_hint=(1.,.9),
									   pos_hint={'x':0., 'y':.05},
									   spacing=10
									   )
		self.score_report = GridLayout(cols=1, size_hint=(1.,.3))
		self.score_report.add_widget(Label(text='Your scores', font_size=90))
		self.score_report.add_widget(Label(text='Best: 0', font_size=60))
		self.score_report.add_widget(Label(text='Last: 0', font_size=60))
		self.score_report.add_widget(Label(text='Number of games: 0', font_size=60))
		self.master_grid.add_widget(self.score_report)

		self.userDevice_ID = '{} ({})'.format(getpass.getuser().capitalize()[:10], socket.gethostname()[:10])
		print('Username for the ranking', self.userDevice_ID)

		self.add_widget(self.master_grid)

		self.bind(size=self.size_callback)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

	def on_enter(self):
		if platform == 'ios':
			filename = join(App.get_running_app().user_data_dir, "score_history.pickle")
		else:
			filename = 'data/score_history.pickle'

		best_score = 0
		if os.path.isfile(filename) :
			score_history = pickle.load(open(filename, 'rb'))
			best_score = max(score_history)
			self.score_report.children[2].text = 'Best: {:.0f}'.format(best_score)
			self.score_report.children[1].text = 'Last: {:.0f}'.format(score_history[-1])
			self.score_report.children[0].text = 'Number of Games: {:.0f}'.format(len(score_history))



Builder.load_string("""
<rankPageUser>:
	background: background
    Background:
        id: background
        pos: root.pos
	Button:
		text: ''
		size_hint: (.1, .1)
		pos_hint: {'x':0.01, 'y':.89}
		on_release: app.sm.current = 'MainPage'
        background_color: 0, 0, 0, .0
		Image:
            source: "images/icons/home.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    Button:
    	text: 'User'
    	size_hint: (.1, .1)
		pos_hint: {'x':0.45, 'y':.89}
		# on_release: app.sm.current = 'RankPageUser'
        background_color: 0, 0, 0, .0
		Image:
            source: "images/icons/rankingUser.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
    Button:
    	text: 'World'
    	size_hint: (.1, .1)
		pos_hint: {'x':0.55, 'y':.89}
		on_release: app.sm.current = 'RankPageWorld'
        background_color: 0, 0, 0, .0
		Image:
            source: "images/icons/rankingWorld.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
""")


"""
Ranking Page will be a page where the user see's two things:
1. his overall ranking compared to other players
2. the achievements he accomplished during the game (ex. average score, etc)
		--> the more achievements a player accomplishes the more stuff he unlocks
"""
