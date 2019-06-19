from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class infoPage(Screen):
	pass

Builder.load_string("""
<infoPage>:
	name: 'InfoPage'
	Image:
        allow_stretch: True
        source: "images/background.png"
        pos: 0, 0
        size: root.height * self.image_ratio, root.height
	Label:
		font_size: 20
		text: 'Jumpy Kitten game developed by Cerri O. & Tamborini A.'
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
InfoPage / In app purchases page (not sure if we want to include this in the first version)


"""
