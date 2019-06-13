from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

class rankPage(Screen):
	pass


Builder.load_string("""
<rankPage>:
	name: 'RankPage'
	Label:
		text:'Ranking'
	Button:
		text: 'Back'
		size_hint: (.1, .1)
		pos_hint: {'x':0, 'y':.9}
		on_release: app.sm.current = 'MainPage'
""")


"""
Ranking Page will be a page where the user see's two things:
1. his overall ranking compared to other players
2. the achievements he accomplished during the game (ex. average score, etc)
		--> the more achievements a player accomplishes the more stuff he unlocks

"""