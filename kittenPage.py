import os, pickle, time

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
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

if platform == 'ios':
	user_data_dir = App.get_running_app().user_data_dir
else:
	user_data_dir = 'data'

class kittenPage(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(kittenPage, self).__init__(**kwargs)

		self.background.remove_clouds()

		self.master_grid = GridLayout(cols=2,
									   size_hint=(1.,.8),
									   pos_hint={'x':0., 'y':.05},
									   spacing=10
									   )

		filename = join(user_data_dir, 'kittenColor.pickle')
		if os.path.isfile(filename):
			global kittenColor
			kittenColor = pickle.load(open(filename, 'rb'))

		self.kitten_preview = GridLayout(cols=1, size_hint_x=.7)
		self.image = Image(source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor))
		self.kitten_preview.add_widget(self.image)
		self.master_grid.add_widget(self.kitten_preview)

		self.kittens = GridLayout(cols=1, spacing=0.02*Window.size[1], size_hint_y=None, row_force_default=False, row_default_height=0.2*Window.size[1])
		self.kittens.bind(minimum_height=self.kittens.setter('height'))
		colors = ['Beige','Brown', 'Gold', 'Gray','Pink', 'Beige','Brown', 'Gold', 'Gray','Pink']
		for c in colors:
			self.addKittensToScroll(c)
		
		self.scrollKittens = ScrollView(size=(.9,.9))
		self.scrollKittens.add_widget(self.kittens)
		self.master_grid.add_widget(self.scrollKittens)

		self.bind(size=self.size_callback)

		self.add_widget(self.master_grid)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

	def addKittensToScroll(self, color):
		row = GridLayout(cols=1)
		kittenButton = Button(background_normal='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(color))
		kittenButton.bind(on_release=self.setColor)
		row.add_widget(kittenButton)
		self.kittens.add_widget(row)

	def setColor(self, instance):
		#this function will open the txt file and save the current cat color
		color = (instance.background_normal.split('/')[2])

		## hardcoded solution for now --> needs to become more modular once I implement classes for each cat
		color = color.split('C')[0][4:]

		global kittenColor
		kittenColor = color
		filename = join(user_data_dir, 'kittenColor.pickle')
		pickle.dump(color, open(filename, 'wb'))

		self.image.source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor)
		self.image.reload()

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
