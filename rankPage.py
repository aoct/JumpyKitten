import os, pickle
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class rankPage(Screen):
	def __init__(self, **kwargs):
		super(rankPage, self).__init__(**kwargs)
		self.score_report = GridLayout(cols=1,
									   size_hint=(1.,.5),
									   pos_hint={'x':0., 'y':.3}
									   )
		self.score_report.add_widget(Label(text='Your scores', font_size=50))
		self.score_report.add_widget(Label(text='Best: 0', font_size=50))
		self.score_report.add_widget(Label(text='Avg: 0', font_size=50))

		self.add_widget(self.score_report)


	def on_enter(self):
		score_best = 0
		score_avg = 0
		if os.path.isfile('data/score_history.pickle'):
			score_history = pickle.load(open('data/score_history.pickle', 'rb'))

			score_best =  max(score_history)
			score_avg = sum(score_history)/float(len(score_history))

			self.score_report.children[1].text = 'Best: {:.1f}'.format(score_best)
			self.score_report.children[0].text = 'Average: {:.1f}'.format(score_avg)




Builder.load_string("""
<rankPage>:
	name: 'RankPage'
	Image:
        allow_stretch: True
        source: "images/background.png"
        pos: 0, 0
        size: root.height * self.image_ratio, root.height
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
