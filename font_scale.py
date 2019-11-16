from kivy.app import App
from kivy.utils import platform
from kivy.metrics import sp, dp

from os.path import join

import os, pickle, time

def font_scaling(num, scale=1):
	return  num*scale

def scaling(pixel_screen_width = 84.0):
	computer_size = 1170. #label.text_size[0] on my macbook pro
	phone_size = pixel_screen_width #label.text_size[0] on my handheld device
	calculated_scale = phone_size/computer_size
	print(computer_size, phone_size, calculated_scale)
	print('[DEBUG]: Font scaling: {:.1f}/{:.1f} = {:.1f}'.format(phone_size, computer_size, calculated_scale))

	if platform == 'ios': user_data_dir = App.get_running_app().user_data_dir
	else: user_data_dir = 'data'

	filename = join(user_data_dir, 'fontScaling.pickle')
	if os.path.isfile(filename):
		scale = pickle.load(open(filename, 'rb'))
		if scale != calculated_scale: pickle.dump(calculated_scale, open(filename, 'wb'))
	else:
		pickle.dump(calculated_scale, open(filename, 'wb'))
