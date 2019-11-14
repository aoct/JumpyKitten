from kivy.utils import platform
from kivy.metrics import sp, dp

def font_scaling(num):
	# text_size = label_instance.text_size 
	if platform == 'ios' or platform == 'android': scale = 52.0 /84.0 #from my phone to computer the scale is this one, if this is not constant amongst devices we need to call instance 
	else: scale = 1
	return sp(num*scale)
