from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

class settingsPage(Screen):
	pass

Builder.load_string("""
<SettingsPage>:
	name: 'SettingsPage'
	Label:
		text: 'SettingsPage'
	Button:
		text: 'Back'
		size_hint: (.1, .1)
		pos_hint: {'x':0, 'y':.9}
		on_release: app.sm.current = 'MainPage'
""")



"""
The settings page will contains features as:
- push notifications on/off
- music while playing on/off
- remove ads (for cost)
- vibrations on/off
- screen orientation 
"""
