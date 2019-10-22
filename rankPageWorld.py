import os, pickle, time

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

gs_scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
username = None
best_score = 0

class rankPageWorld(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(rankPageWorld, self).__init__(**kwargs)

		self.background.remove_clouds()

		self.master_grid = GridLayout(cols=1,
									   size_hint=(1.,.8),
									   pos_hint={'x':0., 'y':.05},
									   spacing=10
									   )

		self.world_ranking = GridLayout(cols=1, size_hint_x=1.)#, size_hint_y= None)#, spacing = 10, row_force_default=True, row_default_height=60)
		self.world_ranking.add_widget(Label(text='World Ranking', bold=True, font_size=90, size_hint_y=0.25))
		row = GridLayout(cols=3, size_hint_y=0.25)
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

		self.userDevice_ID = '{}'.format(plyer.uniqueid.id)
		print('Device ID:', self.userDevice_ID)

		self.bind(size=self.size_callback)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

	def addUserToScroll(self, rank, uname, score, itsMe=False):
		row = GridLayout(cols=3)
		row.add_widget(Label(text=rank, bold=itsMe, halign='center', valign='center', font_size=60))
		row.add_widget(Label(text=uname, bold=itsMe, halign='left', valign='center', font_size=60))
		row.add_widget(Label(text=score, bold=itsMe, halign='right', valign='center', font_size=60))
		self.onlineUsers.add_widget(row)

	def lounch_usernamePopup(self, instance=None, may_exist=True):
		username = 'Not set'
		if may_exist:
			sheet = self.get_gsheet()
			if not sheet == None:
				for i_row, (deviceID, uname, score) in enumerate(sheet.get_all_values(), 1):
					if i_row == 1: continue
					if deviceID == self.userDevice_ID:
						username = uname


		popup = UsernamePopup(auto_dismiss=True, uname=username)
		popup.open()
		popup.bind(on_dismiss=self.reset_ranking)

	def on_enter(self):
		if platform == 'ios':
			user_data_dir = App.get_running_app().user_data_dir
		else:
			user_data_dir = 'data'
		score_history_filename = join(user_data_dir, 'score_history.pickle')

		if os.path.isfile(score_history_filename) :
			global best_score
			best_score = max(pickle.load(open(score_history_filename, 'rb')))


		sheet = self.get_gsheet()
		if not sheet == None:
			device_already_present = False
			for i_row, (deviceID, uname, score) in enumerate(sheet.get_all_values(), 1):
				if i_row == 1: continue
				if deviceID == self.userDevice_ID:
					device_already_present = True
					if float(score) < best_score:
						sheet.update_cell(i_row, 3, '{:.0f}'.format(best_score))
						score = best_score

			if not device_already_present:
				self.lounch_usernamePopup(may_exist=False)

		self.reset_ranking(None)

	def get_gsheet(self):
		try:
			print('[DEBUG] Retrieving credentials')
			credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials/worldRanking_private.json', gs_scope)
			print('[DEBUG] Getting the file')
			file = gspread.authorize(credentials)
			print('[DEBUG] Fetching content')
			sheet = file.open('JumpyKitten_Ranking').sheet1
		except:
			print('[Warning] Cannot load the google sheet')
			return None
		else:
			return sheet

	def on_leave(self):
		self.onlineUsers.clear_widgets()

	def reset_ranking(self, instance):
		if self.onlineUsers.children:
			self.onlineUsers.clear_widgets()

		sheet = self.get_gsheet()
		if sheet == None:
			return

		users = []
		my_uname = None
		for i_row, (deviceID, uname, score) in enumerate(sheet.get_all_values(), 1):
			if i_row == 1: continue
			users.append([uname, int(score)])
			if deviceID == self.userDevice_ID:
				my_uname = uname

		users.sort(reverse=True, key=lambda x: x[1])

		self_present = False
		for i_rank, (uname, score) in enumerate(users, 1):
			if uname == my_uname:
				self_present == True
				self.addUserToScroll(str(i_rank), uname, str(score), itsMe=True)
			else:
				self.addUserToScroll(str(i_rank), uname, str(score))
			if i_rank == 10:
				break
		self.addUserToScroll(3*'-', 40*'-', 3*'-')
		if not self_present:
			for i_rank, (uname, score) in enumerate(users, 1):
				if uname == my_uname:
					self.addUserToScroll(str(i_rank), uname, str(score), itsMe=True)
					break




class UsernamePopup(Popup):
	def __init__(self, uname='Not set', **kwargs):
		super(Popup, self).__init__(**kwargs)

		self.userDevice_ID = '{}'.format(plyer.uniqueid.id)

		self.master = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')

		self.current_uname_label = Label(text='Current username: ' + uname, bold=True, halign='left')
		self.master.add_widget(self.current_uname_label)

		addBox = GridLayout(cols=2, size_hint = (1., 0.4))
		self.input = TextInput(text='', hint_text='(new username)', multiline=False, size_hint_x=0.6)
		addBox.add_widget(self.input)

		self.set_button = Button(text='Enter', size_hint_x=0.2)
		self.set_button.bind(on_release=self.set_username)
		addBox.add_widget(self.set_button)
		self.master.add_widget(addBox)

		self.add_widget(self.master)

	def check_availability(self, sheet):
		desired_uname = self.input.text
		print('desired_uname='+desired_uname)
		isAvailable = True
		for deviceID, uname, _ in sheet.get_all_values():
			print(uname)
			if uname == desired_uname:
				isAvailable = False
				break

		if isAvailable:
			print('[DEBUG]: Username available')
			self.pause_popup.dismiss()
			return True
		else:
			print('[DEBUG]: Username unvailable')
			self.pause_popup.dismiss()
			self.input.text = ''
			self.failure_popup = LabelPopup('Username unavailable', auto_dismiss=True)
			self.failure_popup.open()
			return False

	def set_username(self, instance):
		print('[DEBUG]: Contacting the server')
		self.pause_popup = LabelPopup('Checking checking username availability', auto_dismiss=False)
		self.pause_popup.open()
		try:
			credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials/worldRanking_private.json', gs_scope)
			file = gspread.authorize(credentials)
			sheet = file.open('JumpyKitten_Ranking').sheet1
			isAvailable = self.check_availability(sheet)
		except:
			self.pause_popup.dismiss()
			self.input.text = ''
			self.failure_popup = LabelPopup('Unable to set username', auto_dismiss=True)
			return

		if not isAvailable:
			return

		new_uname = self.input.text
		print('[DEBUG]: Setting username:'+new_uname)
		set_popup = LabelPopup('Setting username', auto_dismiss=False)
		set_popup.open()
		preExisting = False
		for i_row, (deviceID, uname, _) in enumerate(sheet.get_all_values()):
			if deviceID == self.userDevice_ID:
				preExisting = True
				break
		i_row += 1

		if not preExisting:
			i_row += 1
			sheet.update_cell(i_row, 1, self.userDevice_ID)
			sheet.update_cell(i_row, 3, '{:.0f}'.format(best_score))
		sheet.update_cell(i_row, 2, new_uname)

		global username
		username = new_uname

		self.current_uname_label.text = 'Current username: ' + new_uname
		self.input.text = ''
		set_popup.dismiss()

		self.done_popup = LabelPopup('New username set', auto_dismiss=True)
		self.done_popup.open()


class LabelPopup(Popup):
	def __init__(self, text, **kwargs):
		super(Popup, self).__init__(**kwargs)

		l = Label(text=text)
		self.add_widget(l)


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
    	text: ''
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
    	text: ''
    	size_hint: (.1, .1)
		pos_hint: {'x':0.89, 'y':.89}
        background_color: 0, 0, 0, .0
		on_release: root.lounch_usernamePopup()
		Image:
            source: "images/icons/settings.png"
            y: self.parent.y
            x: self.parent.x
            size: self.parent.size
            allow_stretch: True

<UsernamePopup>:
	title: 'Leaderboard Username'
	size_hint: (0.36, 0.5)
	pos_hint: {'x': 0.32, 'y': 0.45}
    background_color: 0, 0, 0, .0
	separator_color: 0x77 / 255., 0x6e / 255., 0x65 / 255., 1.
	title_size: '20sp'

<LabelPopup>:
	title: ''
	size_hint: (0.36, 0.4)
	pos_hint: {'x': 0.32, 'y': 0.55}
	separator_color: 0x77 / 255., 0x6e / 255., 0x65 / 255., 1.
	title_size: '20sp'
""")
