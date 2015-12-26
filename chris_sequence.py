from BlinkyTape import BlinkyTape
import time

#bb = BlinkyTape('/dev/ttyACM0')
bb = BlinkyTape('COM5')
led_count = 60
pixel_full_on = [100, 100, 100]
pixel_off     = [0, 0, 0]

def clear_all():
	for x in range(60):
		bb.sendPixel(0, 0, 0)
	bb.show()

clear_all()
while True:

	for s in range(led_count):
		for t in range(s+1):
			pixel_list = map(lambda x: pixel_full_on if x<=t else pixel_off, range(led_count))
			bb.send_list(pixel_list)

		for t in range(s, -1, -1):
			pixel_list = map(lambda x: pixel_full_on if x<=t else pixel_off, range(led_count))
			bb.send_list(pixel_list)
