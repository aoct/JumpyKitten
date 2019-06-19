from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

class settingsPage(Screen):
	pass

Builder.load_string("""
<SettingsPage>:
	name: 'SettingsPage'
	Image:
        allow_stretch: True
        source: "images/background.png"
        pos: 0, 0
        size: root.height * self.image_ratio, root.height
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
