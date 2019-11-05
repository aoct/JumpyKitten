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
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.utils import platform
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout

from components.background import Background

from os.path import join

import plyer

kittenColor = 'Pink'
best_score = 0
kittenOwned = ['Pink']

kittenValue = {'Pink': 0, 'Beige': 50,'Brown': 100, 'Gray': 250, 'Gold': 500}
kittenScore = {'Pink': 0, 'Beige': 200, 'Brown': 500, 'Gray': 1000, 'Gold': 2000}
kittenPrice = {'Pink': 0, 'Beige': 100, 'Brown': 200, 'Gray': 400, 'Gold': 800}

class kittenPage(Screen):
	background = ObjectProperty(Background())
	collected_coins = NumericProperty(0)
	def __init__(self, **kwargs):
		super(kittenPage, self).__init__(**kwargs)
		self.background.remove_clouds()

		self.master_grid = GridLayout(cols=2,
									   size_hint=(0.95,.9),
									   pos_hint={'x':0.02, 'y':.05},
									   spacing=10
									   )

		if platform == 'ios':
			self.user_data_dir = App.get_running_app().user_data_dir
		else:
			self.user_data_dir = 'data'

		filename_color = join(self.user_data_dir, 'kittenColor.pickle')
		filename_score = join(self.user_data_dir, 'score_history.pickle')
		if os.path.isfile(filename_color):
			global kittenColor
			kittenColor = pickle.load(open(filename_color, 'rb'))
			global best_score
			best_score = max(pickle.load(open(filename_score, 'rb')))

		self.kitten_preview = GridLayout(cols=1, size_hint_x=.8)
		self.image = Image(source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor), size_hint_x=0.4)
		self.kitten_preview.add_widget(self.image)
		self.master_grid.add_widget(self.kitten_preview)


		self.kittensLayout = AnchorLayout(anchor_x = 'center', anchor_y = 'center')
		self.kittenLayoutImage = Image(source = 'images/box.png', allow_stretch=True, keep_ratio = False, size_hint_x = 0.92, size_hint_y = 1.02)

		self.scrollKittens = ScrollView(size=(.3,.9))
		self.kittensLayout.add_widget(self.kittenLayoutImage)
		self.kittensLayout.add_widget(self.scrollKittens)
		self.master_grid.add_widget(self.kittensLayout)

		self.bind(size=self.size_callback)

		self.add_widget(self.master_grid)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

	def addKittensToScroll(self, color):
		row = self.kittenRowLayout(color)
		self.kittens.add_widget(row)

	def kittenRowLayout(self, color):
		a = AnchorLayout(anchor_x = 'center', anchor_y = 'center')
		i = Image(source ="images/smallBox.png", size_hint_x = 0.9, keep_ratio = False, allow_stretch=True)
		row = GridLayout(cols=2, size_hint_y=0.8, size_hint_x = 0.8)
		box = BoxLayout(orientation = 'horizontal')

		if best_score < kittenScore[color]:

			img = Image(source='images/cats/CAT_FRAME_LOCKED_HD.png',
									 size_hint_x=0.5, size_hint_y=0.75,
									 allow_stretch=True
									)
			row.add_widget(img)

			l = Label(text='Unlock at\nscore {}'.format(kittenScore[color]), size_hint_x=0.5, size_hint_y = 0.5,
	        		  halign='center', valign='center',
				      font_size=50,
					  bold=True)
			row.add_widget(l)

		elif best_score >= kittenScore[color]:

			img = Image(source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(color),
									 size_hint_x=0.5, size_hint_y=0.75,
									 allow_stretch=True
									)
			row.add_widget(img)

			if color in kittenOwned:
				button = ToggleButton(text='Select', size_hint_x = 0.5, group='cat_select')
				button.bind(on_release=lambda kittenButton: self.setColor(color))
				global kittenColor
				if color == kittenColor:
					button.state ='down'
					button.text = 'Selected'
			else:
				button = Button(text='Buy', size_hint_x = 0.5, background_color=(0, 0, 0, .0))
				button.associatedKittenColor = color
				button.bind(on_release=lambda kittenButton: self.openBuyCatPopup(color))

			row.add_widget(button)


		a.add_widget(i)
		a.add_widget(row)
		return a

	def setColor(self, color):
		#this function will open the txt file and save the current cat color
		global kittenColor
		oldColor = kittenColor
		kittenColor = color
		filename = join(self.user_data_dir, 'kittenColor.pickle')
		pickle.dump(color, open(filename, 'wb'))

		self.image.source='images/cats/base{0}Cat_aoct/CAT_FRAME_0_HD.png'.format(kittenColor)
		self.image.reload()

		for i in self.kittens.children:
			if i.children[0].children[0].__class__ == ToggleButton:
				if i.children[0].children[0].state == 'down': i.children[0].children[0].text = 'Selected'
				else: i.children[0].children[0].text = 'Select'

	def openBuyCatPopup(self, color):
		self.buyCatPopup = BuyKittenPopup(color, self.collected_coins)
		self.buyCatPopup.open()

	def buyCat(self, color):
		self.collected_coins -= kittenPrice[color]
		filename = join(self.user_data_dir, 'collected_coins.pickle')
		pickle.dump(self.collected_coins, open(filename, 'wb'))

		global kittenOwned
		kittenOwned += [color]
		filename = join(self.user_data_dir, 'owned_kitten.pickle')
		pickle.dump(kittenOwned, open(filename, 'wb'))

		for i in self.kittens.children:
			b = i.children[0].children[0]
			row = i.children[0]
			if b.__class__ == Button:
				if b.associatedKittenColor == color:
					row.remove_widget(b)
					button = ToggleButton(text='Select', size_hint_x = 0.5, group='cat_select')
					button.bind(on_release=lambda kittenButton: self.setColor(color))
					row.add_widget(button)

		self.buyCatPopup.dismiss()

	def on_enter(self):
		filename = join(self.user_data_dir, 'collected_coins.pickle')
		if os.path.isfile(filename):
			self.collected_coins = pickle.load(open(filename, 'rb'))

		filename_score = join(self.user_data_dir, 'score_history.pickle')
		if os.path.isfile(filename_score):
			global best_score
			best_score = max(pickle.load(open(filename_score, 'rb')))

		filename = join(self.user_data_dir, 'owned_kitten.pickle')
		if os.path.isfile(filename):
			global kittenOwned
			kittenOwned = pickle.load(open(filename, 'rb'))
		else:
			kittenOwned = ['Pink']
			pickle.dump(kittenOwned, open(filename, 'wb'))


		self.scrollKittens.clear_widgets()
		self.kittens = GridLayout(cols=1, spacing=0.02*Window.size[1], size_hint_y=None, row_force_default=False, row_default_height=0.3*Window.size[1])
		self.kittens.bind(minimum_height=self.kittens.setter('height'))

		for c in ['Pink', 'Beige','Brown', 'Gray', 'Gold']:
			self.addKittensToScroll(c)

		self.scrollKittens.add_widget(self.kittens)


class BuyKittenPopup(Popup):
	def __init__(self, color, collected_coins, **kwargs):
		super(Popup, self).__init__(**kwargs)
		self.title = '{} cat cost: {} coins'.format(color, kittenPrice[color])
		self.color = color

		if collected_coins >= kittenPrice[color]:
			self.buyBotton.image.source ='images/icons/tick.png'
			self.buyBotton.disabled = False
			self.buyBotton.bind(on_release = lambda x: App.get_running_app().kittenPage.buyCat(color))


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
    BackgroundFloatLayout:
        id: coinFloat
        background_color: 1,0.7,0.7,0.9
        size_hint: (.09, .065)
        # width: 0.09*Window.size[0]
        # height: 0.1*Window.size[1]
        y: 0.8*Window.size[1]
        x: 0.03*Window.size[0]
        Image:
            source: "images/COIN_HD.png"
            height: 0.9*coinFloat.height
            width: 0.9*coinFloat.height
            y: coinFloat.y
            x: coinFloat.x - coinFloat.width*0.45 + 0.9*coinFloat.height/2
        Label:
            id: coinLabel
            font_size: 60
            bold: True
            text: "{:03.0f} ".format(root.collected_coins)
            size: self.texture_size
            x: coinFloat.x + coinFloat.width*0.5 - self.texture_size[0]*0.5
            y: coinFloat.y

<BuyKittenPopup>:
	title: 'Cost: '
	title_align: 'center'
	title_size: '30sp'
	size_hint: (0.4, 0.5)
	pos_hint: {'x': 0.3, 'y': 0.25}
	separator_height: 0
	buyBotton: buyBotton
	GridLayout:
		cols: 2
		Button:
			id: buyBotton
			image: image
	    	text: ''
	        background_color: 0, 0, 0, .0
			on_release: pass
			disabled: True
			Image:
				id: image
	            source: "images/icons/tick_transparent.png"
	            y: self.parent.y
	            x: self.parent.x
	            size: self.parent.size
	            allow_stretch: True
		Button:
	    	text: ''
	        background_color: 0, 0, 0, .0
			on_release: root.dismiss()
			Image:
	            source: "images/icons/close.png"
	            y: self.parent.y
	            x: self.parent.x
	            size: self.parent.size
	            allow_stretch: True
	""")
