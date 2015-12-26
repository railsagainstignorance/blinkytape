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
pixel_full_on = [100, 100, 100]
pixel_off     = [0, 0, 0]

def clear_all():
	for x in range(60):
		bb.sendPixel(0, 0, 0)
	bb.show()

clear_all()
while True:

	for s in range(led_count):
		pixel_random_on = [randint(0,rgb_max), randint(0,rgb_max), randint(0,rgb_max)]
		for t in range(s+1):
			pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
			bb.send_list(pixel_list)

		pixel_random_on = [randint(0,rgb_max), randint(0,rgb_max), randint(0,rgb_max)]
		for t in range(s, -1, -1):
			pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
			bb.send_list(pixel_list)
