from BlinkyTape import BlinkyTape
import time
from random import randint

bb   = BlinkyTape()

led_count     = 60
rgb_max       = 100
pixel_half_on = [100, 100, 100]
pixel_off     = [0, 0, 0]

def shuttle_extend(n=1):
	for i in range(n):
		bb.clear_all()
		for s in range(led_count):
			pixel_random_on = [randint(0,rgb_max), randint(0,rgb_max), randint(0,rgb_max)]
			for t in range(s+1):
				pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
				bb.send_list(pixel_list)
			for t in range(s, -1, -1):
				pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
				bb.send_list(pixel_list)
	bb.clear_all()

def kitt_eye_pixel(x,w,s):
	return pixel_half_on if (x>=s and x<(s+w)) else pixel_off

def kitt_eye(w=5):
	bb.clear_all()
	for s in range(led_count-w):
		pixel_list = map(lambda x: kitt_eye_pixel(x,w,s), range(led_count))
		bb.send_list(pixel_list)

	for s in range(led_count-w, -1, -1):
		pixel_list = map(lambda x: kitt_eye_pixel(x,w,s), range(led_count))
		bb.send_list(pixel_list)
	bb.clear_all()

def kitt_eye_sequence():
	for s in range(led_count -1):
		kitt_eye(led_count - s)

	for s in range(led_count -1, -1, -1):
		kitt_eye(led_count - s)

def impulse(max_loops=2000):
	bb.clear_all()
	v0 = 0.5 # keep v < 1.0
	h0 = 0
	max_h = 60
	g  = -0.0025
	cor = 0.99

	loop = 0
	v=v0
	h=h0
	while loop<=max_loops:
		loop += 1
		h = h + v
		v = v + g
		if h<0:
			v = -v * cor
			h = h + v
			v = v + g
		elif v>max_h:
			h=max_h
			v=0

		pixel_list = map(lambda x: pixel_half_on if (led_count-int(h))==x else pixel_off, range(led_count))
		bb.send_list(pixel_list)

def multiple_impulses(max_loops=2000, num_particles=5):
	bb.clear_all()
	v0 = 0.5 # keep v < 1.0
	h0 = 0
	max_h = 60
	g  = -0.0025
	cor = 0.99	
	line = 	[None] * led_count # [ None, None, [vel, height], None, None, [vel, height], ...]

	for x in range(num_particles): # prime it with particles
		h = randint(0,max_h-1)
		line[h] = [0,h]

	loop = 0
	skip_next = False
	while loop <= max_loops:
		loop += 1
		for i in range(len(line)):
			if line[i] is None or skip_next:
				skip_next = False
			else:
				v = line[i][0]
				h = line[i][1]
				h = h + v
				v = v + g
				if h<0:
					v = -v * cor
					h = h + v
					v = v + g
				elif h>max_h:
					v = 0
					h = max_h
				elif (int(h) != i) and (line[int(h)] is not None):
					# is a collsion
					other_i = int(h)
					h = line[i][1] # remove prev vel contrib to ensure stay in same pixel
					v = line[i][0] 
					# swap vels
					v, line[other_i][0] = line[other_i][0] * cor, v * cor

				vh = [v,h]
				if int(h) == i:
					line[i] = vh
				elif int(h) < i:
					line[i-1] = vh
					line[i] = None
				else:
					line[i+1] = vh
					line[i] = None
					skip_next = True
		pixel_list = map(lambda x: pixel_half_on if (x is not None) else pixel_off, reversed(line))
		bb.send_list(pixel_list)
			
while True:
	impulse()
	shuttle_extend()
	multiple_impulses()
	kitt_eye_sequence()