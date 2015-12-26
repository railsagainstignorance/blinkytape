from BlinkyTape import BlinkyTape
import time

#bb = BlinkyTape('/dev/ttyACM0')
bb = BlinkyTape('COM5')

while True:
	for x in range(60):
		bb.sendPixel(0, 0, 0)
	bb.show()

	for s in range(60):
		for x in range(s):
			bb.sendPixel(100, 100, 100)
		bb.show()
		time.sleep(.5)

	for x in range(60):
		bb.sendPixel(0, 0, 0)
	bb.show()

	time.sleep(.5)
