import os, pickle
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.utils import platform

from components.background import Background

from os.path import join


class rankPage(Screen):
	background = ObjectProperty(Background())
	def __init__(self, **kwargs):
		super(rankPage, self).__init__(**kwargs)
		self.score_report = GridLayout(cols=1,
									   size_hint=(1.,.5),
									   pos_hint={'x':0., 'y':.3}
									   )
		self.score_report.add_widget(Label(text='Your scores', font_size=90))
		self.score_report.add_widget(Label(text='Best: 0', font_size=70))
		self.score_report.add_widget(Label(text='Last: 0', font_size=70))
		self.score_report.add_widget(Label(text='Number of games: 0', font_size=70))

		self.add_widget(self.score_report)
		self.bind(size=self.size_callback)

	def size_callback(self, instance, value):
	    self.background.size = value
	    self.background.update_position()


	def on_enter(self):
		if platform == 'ios':
			filename = join(App.get_running_app().user_data_dir, "score_history.pickle")
		else:
			filename = 'data/score_history.pickle'

		if os.path.getsize(filename) > 0 and os.path.isfile(filename) :
			score_history = pickle.load(open(filename, 'rb'))

			self.score_report.children[2].text = 'Best: {:.0f}'.format(max(score_history))
			self.score_report.children[1].text = 'Last: {:.0f}'.format(score_history[-1])
			self.score_report.children[0].text = 'Number of Games: {:.0f}'.format(len(score_history))


Builder.load_string("""
<rankPage>:
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


"""
Ranking Page will be a page where the user see's two things:
1. his overall ranking compared to other players
2. the achievements he accomplished during the game (ex. average score, etc)
		--> the more achievements a player accomplishes the more stuff he unlocks

"""
