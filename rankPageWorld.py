import os, pickle

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.utils import platform
from kivy.uix.textinput import TextInput

from components.background import Background

from os.path import join

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import plyer

class rankPageWorld(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(rankPageWorld, self).__init__(**kwargs)
		self.master_grid = GridLayout(cols=1,
									   size_hint=(1.,.9),
									   pos_hint={'x':0., 'y':.05},
									   spacing=10
									   )

		self.world_ranking = GridLayout(cols=1, size_hint_x=1.)#, size_hint_y= None)#, spacing = 10, row_force_default=True, row_default_height=60)
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

		self.userDevice_ID = str(plyer.uniqueid.id)

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
			user_data_dir = App.get_running_app().user_data_dir
		else:
			user_data_dir = 'data'

		score_history_filename = join(user_data_dir, 'score_history.pickle')
		username_filename = join(user_data_dir, 'username.pickle')

		if not os.path.isfile(username_filename):
			popup = UsernamePopup(auto_dismiss=True)
			popup.open()


		best_score = 0
		if os.path.isfile(score_history_filename) :
			best_score = max(pickle.load(open(score_history_filename, 'rb')))

		try:
			scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
			print('[DEBUG] Retrieving credentials')
			credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials/ranking_private.json', scope)
			print('[DEBUG] Getting the file')
			file = gspread.authorize(credentials)
			print('[DEBUG] Fetching content')
			sheet = file.open('JumpyKitten_Ranking').sheet1
		except:
			print('[Warning] No Internet Connection. Ranking will not be loaded')
		else:
			device_already_present = False

			users = []
			for i_row, (deviceID, uname, score) in enumerate(sheet.get_all_values(), 1):
				if i_row == 1: continue
				if deviceID == self.userDevice_ID:
					device_already_present = True
					if float(score) < best_score:
						sheet.update_cell(i_row, 3, '{:.0f}'.format(best_score))
						score = best_score
				users.append([uname, int(score)])

			if not device_already_present:
				sheet.update_cell(i_row+1, 1, self.userDevice_ID)
				sheet.update_cell(i_row+1, 2, self.userDevice_ID)
				sheet.update_cell(i_row+1, 3, str(int(best_score)))

			users.sort(reverse=True, key=lambda x: x[1])

			if not self.onlineUsers.children:
				self.addUserToScroll('','------------------','')
				for rank, (uname, score) in enumerate(users, 1):
					self.addUserToScroll(str(rank), uname, str(score))

	def on_leave(self):
		self.onlineUsers.clear_widgets()


class UsernamePopup(Popup):
	def __init__(self, **kwargs):
		super(Popup, self).__init__(**kwargs)

		self.master = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')

		self.current_uname_label = Label(text='Current username: None', bold=True, halign='left')
		self.master.add_widget(self.current_uname_label)

		addBox = GridLayout(cols=3, size_hint = (1., 0.1))
		self.input = TextInput(text='', hint_text='(new username)', multiline=False, size_hint_x=0.6)
		addBox.add_widget(self.input)

		self.check_button = Button(text='check', size_hint_x=0.2)
		self.check_button.bind(on_release=self.check_availability)
		addBox.add_widget(self.check_button)
		self.set_button = Button(text='set', size_hint_x=0.2)
		self.set_button.bind(on_release=self.set_username)
		addBox.add_widget(self.set_button)
		self.master.add_widget(addBox)

		self.add_widget(self.master)

	def check_availability(self):
		print('[DEBUG]: Checking username availability')

	def set_username(self):
		print('[DEBUG]: Setting username')


Builder.load_string("""
<rankPageWorld>:
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
		on_release: app.sm.current = 'RankPageUser'
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
		# on_release: app.sm.current = 'RankPageWorld'
        background_color: 0, 0, 0, .0
		Image:
            source: "images/icons/rankingWorld.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True

<UsernamePopup>:
	size_hint: None, None
	title: 'Leaderboard username'
	size: '300dp', '300dp'
	separator_color: 0x77 / 255., 0x6e / 255., 0x65 / 255., 1.
	title_size: '20sp'

	# Button:
	# 	text: ''
	# 	size_hint: (.1, .1)
	# 	pos_hint: {'x':0.01, 'y':.95}
	# 	on_release: root.dismiss()
	# 	background_color: 0, 0, 0, .0
	# 	Image:
	# 		source: "images/icons/close.png"
	# 		y: self.parent.y
	# 		x: self.parent.x
	# 		size: self.parent.size
	# 		allow_stretch: True
""")
