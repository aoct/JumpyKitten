import os, pickle, getpass, socket

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty
from kivy.app import App
from kivy.utils import platform
from kivy.metrics import sp

from components.background import Background

from os.path import join

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from font_scale import font_scaling

class rankPageUser(Screen):
	background = ObjectProperty(Background())
	font_scale = NumericProperty(1)
	def __init__(self, **kwargs):
		super(rankPageUser, self).__init__(**kwargs)

		self.background.remove_clouds()

		if platform == 'ios': self.user_data_dir = App.get_running_app().user_data_dir
		else: self.user_data_dir = 'data'

		filename_scale = join(self.user_data_dir, 'fontScaling.pickle')
		if os.path.isfile(filename_scale):
		    self.font_scale = pickle.load(open(filename_scale, 'rb'))

		self.master_grid = GridLayout(cols=1,
									   size_hint=(1.,.7),
									   pos_hint={'x':0., 'y':.15},
									   spacing=10
									   )
		self.score_report = GridLayout(cols=1, size_hint=(1.,.3))
		self.score_report.add_widget(Label(text='Your scores', bold=True, font_size=font_scaling(70, self.font_scale)))
		self.score_report.add_widget(Label(text='Best score: 0', font_size=font_scaling(50, self.font_scale)))
		self.score_report.add_widget(Label(text='Last score: 0', font_size=font_scaling(50, self.font_scale)))
		self.score_report.add_widget(Label(text='Games played: 0', font_size=font_scaling(50, self.font_scale)))
		self.master_grid.add_widget(self.score_report)

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
			best_score = int(max(score_history))
			self.score_report.children[2].text = 'Best score: {:.0f}'.format(best_score)
			self.score_report.children[1].text = 'Last score: {:.0f}'.format(int(score_history[-1]))
			self.score_report.children[0].text = 'Games played: {:.0f}'.format(len(score_history))



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
    	text: ''
    	size_hint: (.1, .1)
		pos_hint: {'x':0.45, 'y':.89}
		on_release: app.sm.current = 'RankPageWorld'
        background_color: 0, 0, 0, .0
		Image:
            source: "images/icons/rankingWorld.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True
""")
