from kivy.app import App
from kivy.utils import platform
from kivy.metrics import sp, dp

from os.path import join

import os, pickle, time

def font_scaling(num, scale=1):
	return  num*scale

def scaling(screen_size):
	computer_size = [1170., 540.] #label.text_size[0] on my macbook pro
	phone_size = screen_size #label.text_size[0] on my handheld device
	x_scale = phone_size[0]/computer_size[0]
	y_scale = phone_size[1]/computer_size[1]
	print('[DEBUG]: x_scale: {:.1f}/{:.1f} = {:.1f}'.format(phone_size[0], computer_size[0], x_scale))
	print('[DEBUG]: y_scale: {:.1f}/{:.1f} = {:.1f}'.format(phone_size[1], computer_size[1], x_scale))

	if platform == 'ios': user_data_dir = App.get_running_app().user_data_dir
	else: user_data_dir = 'data'

	filename = join(user_data_dir, 'fontScaling.pickle')
	l = [x_scale, y_scale]
	pickle.dump(l, open(filename, 'wb'))
