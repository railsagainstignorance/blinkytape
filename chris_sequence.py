from BlinkyTape import BlinkyTape
import time
import os.path
from random import randint

linux_port   = '/dev/ttyACM0'
windows_port = 'COM5'

port = linux_port if os.path.exists( linux_port ) else windows_port
bb   = BlinkyTape(port)

led_count     = 60
rgb_max       = 100
pixel_half_on = [100, 100, 100]
pixel_off     = [0, 0, 0]

def clear_all():
	for x in range(60):
		bb.sendPixel(0, 0, 0)
	bb.show()

def shuttle_extend(n=1):
	for i in range(n):
		clear_all()
		for s in range(led_count):
			pixel_random_on = [randint(0,rgb_max), randint(0,rgb_max), randint(0,rgb_max)]
			for t in range(s+1):
				pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
				bb.send_list(pixel_list)

	#		pixel_random_on = [randint(0,rgb_max), randint(0,rgb_max), randint(0,rgb_max)]
			for t in range(s, -1, -1):
				pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
				bb.send_list(pixel_list)
	clear_all()

def kitt_eye_pixel(x,w,s):
	return pixel_half_on if (x>=s and x<(s+w)) else pixel_off

def kitt_eye(w=5):
	clear_all()
	for s in range(led_count-w):
		pixel_list = map(lambda x: kitt_eye_pixel(x,w,s), range(led_count))
		bb.send_list(pixel_list)

	for s in range(led_count-w, -1, -1):
		pixel_list = map(lambda x: kitt_eye_pixel(x,w,s), range(led_count))
		bb.send_list(pixel_list)
	clear_all()

def kitt_eye_sequence():
	for s in range(led_count -1):
		kitt_eye(led_count - s)

	for s in range(led_count -1, -1, -1):
		kitt_eye(led_count - s)

while True:
	shuttle_extend()
	kitt_eye_sequence()