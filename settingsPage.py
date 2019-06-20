from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from components.background import Background

class settingsPage(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(settingsPage, self).__init__(**kwargs)
		self.bind(size=self.size_callback)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()

Builder.load_string("""
<SettingsPage>:
	background: background
    Background:
        id: background
        pos: root.pos
	Label:
		text: 'Coming soon...'
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
The settings page will contains features as:
- push notifications on/off
- music while playing on/off
- remove ads (for cost)
- vibrations on/off
- screen orientation
"""
