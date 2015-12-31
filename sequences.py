from BlinkyTape import BlinkyTape
import time
from random import randint

bb   = BlinkyTape()

led_count     = 60
rgb_max       = 100
pixel_half_on = [rgb_max, rgb_max, rgb_max]
pixel_off     = [0, 0, 0]

def shuttle_extend(n=1,step=2):
	for i in range(n):
		bb.clear_all()
		for s in range(0,led_count,step):
			pixel_random_on = [randint(0,rgb_max), randint(0,rgb_max), randint(0,rgb_max)]
			for t in range(s+1):
				pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
				bb.send_list(pixel_list)
			for t in range(s, -1, -1):
				pixel_list = map(lambda x: pixel_random_on if x<=t else pixel_off, range(led_count))
				bb.send_list(pixel_list)
	bb.clear_all()

def kitt_eye_pixel(x,w,s): # kitt's eye is w pixels wide and starts at position s
	return pixel_half_on if (x>=s and x<(s+w)) else pixel_off

def kitt_eye(w=5): # kitt's eye is w pixels wide
	bb.clear_all()
	for s in range(led_count-w):
		pixel_list = map(lambda x: kitt_eye_pixel(x,w,s), range(led_count))
		bb.send_list(pixel_list)

	for s in range(led_count-w, -1, -1):
		pixel_list = map(lambda x: kitt_eye_pixel(x,w,s), range(led_count))
		bb.send_list(pixel_list)
	bb.clear_all()

def kitt_eye_sequence(step=2):
	for s in range(0, led_count -1, step):
		kitt_eye(led_count - s)

	for s in range(led_count -1, -1, - step):
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
	line = 	[None] * led_count # to hold all the particles and empty spaces: [ None, None, [vel, height], None, ..., None, [vel, height], ...]

	for x in range(num_particles): # prime it with particles, each with [velocity,height]
		h = randint(0,max_h-1)
		line[h] = [0,h]

	loop = 0
	skip_next = False
	while loop <= max_loops:  
		loop += 1
		for i in range(len(line)): # scan from low to high, adjusting one pixel at a time.
			if line[i] is None or skip_next:
				skip_next = False
			else:
				v = line[i][0]
				h = line[i][1]
				h = h + v
				v = v + g
				if h<0: # bounce off bottom
					v = -v * cor
					h = h + v
					v = v + g
				elif h>max_h: # stop at top
					v = 0
					h = max_h
				elif (int(h) != i) and (line[int(h)] is not None): # is a collsion
					other_i = int(h)
					h = line[i][1] # remove prev vel contrib to ensure stay in same pixel
					v = line[i][0] 
					# swap vels (simple physics of direct elastic collision between two identical objects)
					v, line[other_i][0] = line[other_i][0] * cor, v * cor

				vh = [v,h]
				if int(h) == i: # stays in same pixel
					line[i] = vh
				elif int(h) < i: # moves down
					line[i-1] = vh
					line[i] = None
				else:             # moves up
					line[i+1] = vh
					line[i] = None
					skip_next = True # don't recalc its position in this sweep
		pixel_list = map(lambda x: pixel_half_on if (x is not None) else pixel_off, reversed(line))
		bb.send_list(pixel_list)
			
while True:
	impulse()
	shuttle_extend()
	multiple_impulses()
	kitt_eye_sequence()