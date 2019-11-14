from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import sp

from kivy.uix.anchorlayout import AnchorLayout

from components.background import Background

from font_scale import font_scaling

class infoPage(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(infoPage, self).__init__(**kwargs)
		self.bind(size=self.size_callback)

		self.master_grid = GridLayout(cols = 2, size_hint=(1., 0.7), pos_hint={'x':0., 'y':0.15})
		self.logo_grid = GridLayout(cols=1, size_hint=(.5, .7))
		self.logo_image = Image(source="images/logo.png", size_hint= (10, 10))
		self.logo_text = Label(text= '        Jumpy Kitten\ndeveloped by AOCTdev', bold= True, font_size= font_scaling(20))
		self.logo_grid.add_widget(self.logo_image)
		self.logo_grid.add_widget(self.logo_text)

		self.instructions_anchor = AnchorLayout(anchor_x = 'center', anchor_y = 'center', )
		self.LayoutImage = Image(source = 'images/box.png', allow_stretch=True, keep_ratio = False, size_hint_x = .85, size_hint_y = 1.)
		self.instructions_grid = GridLayout(cols=1, size_hint=(.5, .7))
		self.instruction_title = Label(text='Gaming Instructions\n', halign='center', valign='top', bold=True, font_size=font_scaling(50))
		self.instruction_layout = Label(text=' 1. Tap the screen to make Rose jump \n 2. Double tap to overcome hardest obstacles \n 3. Avoid obstacles (trees, rocks, birds) during run \n 4. Collect coins for extra lives \n 5. Achieve high scores to unlock new kittens \n 6. Use coins to buy new kittens \n 7. Watch reward videos to gain extra coins\n', valign='bottom', font_size= font_scaling(25))
		self.instructions_grid.add_widget(self.instruction_title)
		self.instructions_grid.add_widget(self.instruction_layout)
		self.instructions_anchor.add_widget(self.LayoutImage)
		self.instructions_anchor.add_widget(self.instructions_grid)

		self.master_grid.add_widget(self.logo_grid)
		self.master_grid.add_widget(self.instructions_anchor)
		self.add_widget(self.master_grid)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

Builder.load_string("""
<infoPage>:
	background: background
    Background:
        id: background
        pos: root.pos
	# Image:
 #        source: "images/logo.png"
	# 	size_hint: (.8, .8)
	# 	pos_hint: {'x':0.1, 'y':0.15}
	# Label:
	# 	font_size: 60
	# 	bold: True
	# 	text: 'Jumpy Kitten game developed by AOCTdev'
	# 	center_y: -0.25*Window.size[1]
	# Rate our app here: https://play.google.com/store/apps/details?id=org.aoct.jumpykitten.jumpykitten
	Button:
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
InfoPage / In app purchases page (not sure if we want to include this in the first version)


"""
