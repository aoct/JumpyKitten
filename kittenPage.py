import os, pickle, time

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.utils import platform
from kivy.uix.textinput import TextInput

from components.background import Background

from os.path import join

import plyer

kittenColor = 'Pink'

kittenValue = {'Pink': 0, 'Beige': 50,'Brown': 100, 'Gray': 250, 'Gold': 500}

class kittenPage(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(kittenPage, self).__init__(**kwargs)

		self.background.remove_clouds()

		self.master_grid = GridLayout(cols=2,
									   size_hint=(0.95,.8),
									   pos_hint={'x':0.02, 'y':.05},
									   spacing=10
									   )

		if platform == 'ios':
			self.user_data_dir = App.get_running_app().user_data_dir
		else:
			self.user_data_dir = 'data'

		filename = join(self.user_data_dir, 'kittenColor.pickle')
		if os.path.isfile(filename):
			global kittenColor
			kittenColor = pickle.load(open(filename, 'rb'))

		self.kitten_preview = GridLayout(cols=1, size_hint_x=.7)
		self.image = Image(source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor))
		self.kitten_preview.add_widget(self.image)
		self.master_grid.add_widget(self.kitten_preview)

		self.kittens = GridLayout(cols=1, spacing=0.02*Window.size[1], size_hint_y=None, row_force_default=False, row_default_height=0.2*Window.size[1])
		self.kittens.bind(minimum_height=self.kittens.setter('height'))

		for c in ['Pink', 'Beige','Brown', 'Gray', 'Gold']:
			self.addKittensToScroll(c)

		self.scrollKittens = ScrollView(size=(.3,.9))
		self.scrollKittens.add_widget(self.kittens)
		self.master_grid.add_widget(self.scrollKittens)

		self.bind(size=self.size_callback)

		self.add_widget(self.master_grid)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

	def addKittensToScroll(self, color):
		row = GridLayout(cols=3, size_hint_y=0.35*Window.size[1], col_default_width=0.175*Window.size[0])
		box = GridLayout(cols=2, col_default_width=0.1*Window.size[0], col_force_default=True)
		coins = Image(source="images/coin_HD.png", size=(0.01*Window.size[0], 0.01*Window.size[0]), allow_stretch = True)
		l = Label(text='{}x'.format(kittenValue[color]), size_hint_x=0.2,
        		  halign='left', valign='center',
			      font_size=40,
			      color=[226/255.0, 158/255.0, 163/255.0, 1], bold=True)
		box.add_widget(l)
		box.add_widget(coins)
		row.add_widget(box)

		self.kittenImage = Image(source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(color), size_hint_x = 0.3)
		row.add_widget(self.kittenImage)
		self.kittenButton = ToggleButton(text='Select', size_hint_x = 0.05*Window.size[0], size_hint_y = 0.05*Window.size[1], group='cat_select')
		self.kittenButton.bind(on_press=lambda kittenButton: self.setColor(color))
		row.add_widget(self.kittenButton)
		self.kittens.add_widget(row)

	def setColor(self, color):
		#this function will open the txt file and save the current cat color		
		global kittenColor
		oldColor = kittenColor
		kittenColor = color
		filename = join(self.user_data_dir, 'kittenColor.pickle')
		pickle.dump(color, open(filename, 'wb'))

		self.image.source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor)
		self.image.reload()

		for i in App.get_running_app().kittenPage.kittens.children:
			if i.children[0].state == 'down': i.children[0].text = 'Selected'
			else: i.children[0].text = 'Select'


	def on_enter(self):
		pass


Builder.load_string("""
<kittenPage>:
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
