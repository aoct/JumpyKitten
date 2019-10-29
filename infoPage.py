from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from components.background import Background


class infoPage(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(infoPage, self).__init__(**kwargs)
		self.bind(size=self.size_callback)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

Builder.load_string("""
<infoPage>:
	background: background
    Background:
        id: background
        pos: root.pos
	Image:
        source: "images/logo.png"
		size_hint: (.8, .8)
		pos_hint: {'x':0.1, 'y':0.15}
	Label:
		font_size: 60
		bold: True
		text: 'Jumpy Kitten game developed by AOCTdev'
		center_y: -0.25*Window.size[1]
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
