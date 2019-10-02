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

class rankPage(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(rankPage, self).__init__(**kwargs)
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

		self.world_ranking = GridLayout(cols=1, size_hint=(1.,.7))
		self.world_ranking.add_widget(Label(text='World ranking', font_size=90))
		row = GridLayout(cols=3)
		row.add_widget(Label(text='Rank', halign='center', valign='center', font_size=60))
		row.add_widget(Label(text='Username', halign='left', valign='center', font_size=60))
		row.add_widget(Label(text='Score', halign='right', valign='center', font_size=60))
		self.world_ranking.add_widget(row)
		self.onlineUsers = GridLayout(cols=1, spacing=15, size_hint_y=None, row_force_default=True, row_default_height=60)
		self.onlineUsers.bind(minimum_height=self.onlineUsers.setter('height'))

		self.scrollOnlineUsers = ScrollView(size_hint=(1.,.9))
		self.scrollOnlineUsers.add_widget(self.onlineUsers)
		self.world_ranking.add_widget(self.scrollOnlineUsers)
		self.master_grid.add_widget(self.world_ranking)

		self.add_widget(self.master_grid)

		self.userDevice_ID = '{} ({})'.format(getpass.getuser().capitalize()[:10], socket.gethostname()[:10])
		print('Username for the ranking', self.userDevice_ID)

		self.bind(size=self.size_callback)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

	def addUserToScroll(self, rank, uname, score):
		row = GridLayout(cols=3)
		row.add_widget(Label(text=rank, halign='center', valign='center', font_size=60))
		row.add_widget(Label(text=uname, halign='left', valign='center', font_size=60))
		row.add_widget(Label(text=score, halign='right', valign='center', font_size=60))
		self.onlineUsers.add_widget(row)

	def on_enter(self):
		if platform == 'ios':
			filename = join(App.get_running_app().user_data_dir, "score_history.pickle")
		else:
			filename = 'data/score_history.pickle'

		best_score = 0
		if os.path.getsize(filename) > 0 and os.path.isfile(filename) :
			score_history = pickle.load(open(filename, 'rb'))

			best_score = max(score_history)
			self.score_report.children[2].text = 'Best: {:.0f}'.format(best_score)
			self.score_report.children[1].text = 'Last: {:.0f}'.format(score_history[-1])
			self.score_report.children[0].text = 'Number of Games: {:.0f}'.format(len(score_history))

		try:
			scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
			credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
			file = gspread.authorize(credentials)
			sheet = file.open('JumpyKitten_Ranking').sheet1
		except:
			print('[Warning] No Internet Connection. Ranking will not be loaded')
		else:
			uname_already_present = False
			users = []
			for i_row, (uname, score) in enumerate(sheet.get_all_values(), 1):
				if i_row == 1: continue
				users.append([uname, int(score)])
			users.sort(reverse=True, key=lambda x: x[1])
			for rank, (uname, score) in enumerate(users, 1):
				self.addUserToScroll(str(rank), uname, str(score))
				if uname == self.userDevice_ID:
					uname_already_present = True
					if float(score) < best_score:
						sheet.update_cell(i_row, 2, '{:.0f}'.format(best_score))
			if not uname_already_present:
				sheet.update_cell(i_row+1, 1, self.userDevice_ID)
				sheet.update_cell(i_row+1, 2, str(best_score))

Builder.load_string("""
<rankPage>:
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
""")


"""
Ranking Page will be a page where the user see's two things:
1. his overall ranking compared to other players
2. the achievements he accomplished during the game (ex. average score, etc)
		--> the more achievements a player accomplishes the more stuff he unlocks
"""
