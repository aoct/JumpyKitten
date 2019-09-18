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
		self.score_report = GridLayout(cols=1,
									   size_hint=(1.,.5),
									   pos_hint={'x':0., 'y':.3}
									   )
		self.score_report.add_widget(Label(text='Your scores', font_size=90))
		self.score_report.add_widget(Label(text='Best: 0', font_size=60))
		self.score_report.add_widget(Label(text='Last: 0', font_size=60))
		self.score_report.add_widget(Label(text='Number of games: 0', font_size=60))

		self.score_report.add_widget(Label(text='World ranking', font_size=90))

		self.onlineUsers = GridLayout(cols=1, spacing=10, size_hint_y=None, row_force_default=True, row_default_height=40)
		self.onlineUsers.bind(minimum_height=self.onlineUsers.setter('height'))

		self.scrollOnlineUsers = ScrollView()
		self.scrollOnlineUsers.add_widget(self.onlineUsers)
		self.score_report.add_widget(self.scrollOnlineUsers)

		self.add_widget(self.score_report)

		self.userDevice_ID = '{} ({})'.format(getpass.getuser().capitalize()[:10], socket.gethostname()[:10])
		print('Username for the ranking', self.userDevice_ID)

		self.bind(size=self.size_callback)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

	def addUserToScroll(self, uname, score):
		row = GridLayout(cols=2)
		row.add_widget(Label(text=uname, halign='left', valign='center', font_size=50))
		row.add_widget(Label(text=score, halign='right', valign='center', font_size=50))
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

		#create a connection with googlesheets
		## We should put something such that if there is no internet connection it does not crush
		try:
			scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
			credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
			file = gspread.authorize(credentials)
			sheet = file.open('JumpyKitten_Ranking').sheet1
		except:
			Logger.exception("No Internet Connection")
		else:
			uname_already_present = False
			for i_row, (uname, score) in enumerate(sheet.get_all_values(), 1):
				print(i_row, uname, score)
				self.addUserToScroll(uname, score)
				if uname == self.userDevice_ID:
					uname_already_present = True
					if float(score) < best_score:
						sheet.update_cell(i_row, 2, str(best_score))
			if not uname_already_present:
				sheet.update_cell(i_row+1, 1, self.userDevice_ID)
				sheet.update_cell(i_row+1, 2, str(best_score))


		print(sheet.get_all_values())

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
